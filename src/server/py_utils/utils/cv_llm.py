import requests
from pypdf import PdfReader
from langchain.chains import LLMChain, SequentialChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv
import asyncio


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class ReadPDF:
    def __init__(self, url):
        self.url = url
        self.response = requests.get(url)
        self.dir = 'temp/temp.pdf'

    def read(self):
        with open(self.dir, 'wb') as fd:
            fd.write(self.response.content)

        reader = PdfReader(self.dir)
        all_text = ""

        for page in reader.pages:
            all_text += page.extract_text()
            
        return all_text
    
class BaseCVLLM:
    def __init__(self, cv, job_title, job_description) -> None:
        self.cv = cv
        self.job_title = job_title
        self.job_description = job_description
        self.llm = OpenAI(temperature=0.6, max_tokens=-1, 
                          openai_api_key=OPENAI_API_KEY,
                          #model="ada")
        )

        with open("src/server/py_utils/json_components/cv_elements.json") as elements_file:
               self.elements = json.load(elements_file)

    async def async_generate(self, sqc, inputs):
          resp = await sqc.arun(inputs)
          return resp
    
    async def build_dict(self):
          prompt1 = """
          Given a CV for the Job title: {job_title},
          Analayse the CV and identify the follwing component:
        
         {field}: {field_info}

          Scan the CV for the presence of this field, Identify the segment.
          ONLY Return a json formatted string where the property name is {field} and value is the identied segment
          If you cannot identify the segment, The value of the property should be null.
          -----
          CV:
          {cv}
          -----

          Make sure to RETURN ONLY JSON, not code or any other text. 
          """

          prompt1_template = PromptTemplate(
               input_variables=["job_title" ,"cv", "field", "field_info"],
               template= prompt1
          )

          chain1 = LLMChain(llm = self.llm, prompt=prompt1_template, 
                            output_key="dictionary"
                        )
          
          dict_chain = SequentialChain(
               chains = [chain1],
               input_variables = ["job_title", "cv", "field", "field_info"],
               output_variables = ["dictionary"],
               verbose = False
          )
          
          tasks = []
          for field in self.elements.keys():
               field_info = self.elements[field]
               inputs = {
               "job_title": self.job_title,
               "field": field,
               "field_info": field_info,
               "cv": self.cv
               }

               tasks.append(self.async_generate(dict_chain, inputs))
          results = await asyncio.gather(*tasks)

          elements_dict = {}
          
          for json_stuff in results:
               temp_ = json.loads(json_stuff)
               name_ = list(temp_.keys())[0]
               
               elements_dict[name_] = temp_[name_]
          return elements_dict
    
    async def generate_concurrently(self):
          pt = PromptTemplate(
               input_variables=["job_title", "field", "field_info", "field_val", "job_description"],
               template = """
              Your team is evaluating CVs. Your job is to evaluate the {field} in a given CV.
              See how well the provided {field} in this CV in this field is applicable for the job title {job_title}.
              The job description of this post will also be provided to you, Use it as a reference to score the provided field: {field}
              Based on this, Score the {field} out of 10. If the field has been listed as null, give the score as 0
              You are allowed to use decimal values, Return ONLY THE SCORE AND NO OTHER TEXT.

              {field} = {field_info}. 
              ---
              Job description:
              {job_description}
              ---
              This is what has been provided in the applicants CV:

              {field}:

              {field_val}
              ---         
          """
          )
          chain = LLMChain(llm = self.llm,
                           prompt=pt,
                           output_key="score")
          
          sqc = SequentialChain(
               chains = [chain],
               input_variables = ["job_title", "field", "field_info", "field_val", "job_description"],
               output_variables = ["score"],
               verbose = False
          )

          elements_dict = await self.build_dict() 
          tasks = []

          for field in elements_dict.keys():
               field_info = self.elements[field]
               field_val = elements_dict[field]
               inputs = {
               "job_title": self.job_title,
               "field": field,
               "field_info": field_info,
               "field_val": field_val,
               "job_description": self.job_description
               }

               tasks.append(self.async_generate(sqc, inputs))

          results = await asyncio.gather(*tasks)
          results  = [float(i) for  i in results]

          sum_score = sum(results)
          return  sum_score, elements_dict

class CVranker:
     def __init__(self, cv_list: list, job_title: str, job_description: str) -> None:
          self.cv_list = cv_list,
          self.job_title = job_title,
          self.job_description = job_description 
          self.review_llm = OpenAI(temperature=0.6, openai_api_key=OPENAI_API_KEY)

     def sort_func(self, cvs):
          return cvs['score']
     
     def build_review_llm(self):
          pt = PromptTemplate(
               input_variables=["cv"],
               template = """
                Summarise the CV in a short, clear and concise way. Make sure to retain all the important elements of the CV.
                DO NOT MAKE UP ANY INFORMATION. ONLY USE THE INFORMATION PROVIDED IN THE CV BELOW.
                ---
                CV:
                {cv}        
                ---
                Return ONLY the short summarized CV.
                """
          )

          llmchain = LLMChain(llm = self.review_llm,
                              prompt=pt,
                              output_key="review")
          
          review_llm = SequentialChain(
               chains = [llmchain],
               input_variables=["cv"],
               output_variables=["review"],
               verbose = False
          )

          return review_llm

     async def async_generate_scores(self, cv_llm):
          score, elements_dict = await cv_llm.generate_concurrently()
          return score, elements_dict['Contact information']
     
     async def async_generate_reviews(self, review_llm, inputs):
          resp = await review_llm.arun(inputs)
          return resp

     async def generate_rankings(self):
          review_tasks = []
          scores_contacts = []
          for cv in self.cv_list[0]:
               cv_score_llm  = BaseCVLLM(job_title=self.job_title,
                                        job_description=self.job_description,
                                        cv= cv)
               review_llm = self.build_review_llm()
               score, elem_dict = await cv_score_llm.generate_concurrently()
               
               scores_contacts.append((score,elem_dict['Contact information']))
               review_tasks.append(self.async_generate_reviews(review_llm, 
                                                              {"cv": cv}))
               
          summaries = await asyncio.gather(*review_tasks)

          cv_rankings = []
          for num, result in enumerate(scores_contacts):
               cv_info = {}
               cv_info['score'] = result[0]
               cv_info['contact_info'] = result[1]
               cv_info['short_summary'] = summaries[num]
               cv_rankings.append(cv_info)

          cv_rankings.sort(key=self.sort_func, reverse=True)
          return cv_rankings
          


          
               
               
            
          
