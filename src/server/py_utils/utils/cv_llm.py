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

import requests
import PyPDF2
from io import BytesIO



dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def read_text_from_url(url):
  """Reads all the text from a file at the specified URL.

  Args:
    url: The URL of the file to read.

  Returns:
    A Python string containing the text of the file.
  """

  import requests
  import io

  response = requests.get(url)
  if response.status_code != 200:
    raise ValueError(f"Could not read file from URL: {url}")

  file_content = response.content

  if file_content.startswith(b"%PDF"):
    # The file is a PDF.
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
    text = ""
    for page in pdf_reader.pages:
      text += page.extract_text()
  elif file_content.startswith(b"<html"):
    # The file is a HTML document.
    text = b"".join(response.text.split(b"\n"))
  else:
    # The file is a text file.
    text = file_content.decode("utf-8")

  return text

def read_pdf(url):
     response = requests.get(url)
    
     if response.status_code == 200:
        pdf_data = BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_data)
        
        all_text = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            all_text.append(text)
        
        return '\n'.join(all_text)
     

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

              Based on this, Score the {field} out of 10. 
              DO NOT BE LENIENT with the scoring, You are free to give a low score if you feel like the provided {field} is not good.
              If the field has been listed as null, give the score as 0
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
          element_wise_score = {}
          
          for score, element in zip(results,elements_dict.keys()):
              element_wise_score[element] = score

          sum_score = sum(results)
          return  sum_score, elements_dict, element_wise_score

class CVranker:
     def __init__(self, cv_links_list: list, job_title: str, job_description: str) -> None:
          self.cvs = [read_pdf(link) for link in cv_links_list]
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
          return score, elements_dict['Contact Information']
     
     async def async_generate_reviews(self, review_llm, inputs):
          resp = await review_llm.arun(inputs)
          return resp

     async def generate_rankings(self):
          review_tasks = []
          scores_contacts = []
          if self.cvs:
               for cv in self.cvs:  # Changed from self.cv to self.cvs
                    cv_score_llm = BaseCVLLM(job_title=self.job_title,
                                             job_description=self.job_description,
                                             cv=cv)
                    review_llm = self.build_review_llm()
                    score, elem_dict, element_wise_score= await cv_score_llm.generate_concurrently()

                    scores_contacts.append((score, elem_dict['Contact Information'], element_wise_score))
                    review_tasks.append(self.async_generate_reviews(review_llm,
                                                                      {"cv": cv}))
          else:
               print(self.cvs, "no cv")

          summaries = await asyncio.gather(*review_tasks)

          cv_rankings = []
          for num, result in enumerate(scores_contacts):
               cv_info = {}
               cv_info['score'] = result[0]
               cv_info['contact_info'] = result[1]
               cv_info['element_wise_score'] = result[2]
               cv_info['short_summary'] = summaries[num]
               cv_rankings.append(cv_info)

          cv_rankings.sort(key=self.sort_func, reverse=True)
          return cv_rankings
     
cvr = CVranker(
    job_title = "bank manager",
    job_description= """

Position: Bank Manager
Department: Branch Operations
Location: Bangalore, India
Reports To: Regional Manager or Area Director

Job Summary:
The Bank Manager is responsible for overseeing the daily operations of a bank branch, ensuring exceptional customer service, effective financial management, and compliance with regulatory standards. They lead a team of banking professionals, drive business growth, and maintain a positive branch image within the community.

Key Responsibilities:

Team Leadership:
Lead, mentor, and manage a team of banking staff, including tellers, customer service representatives, loan officers, and other roles.
Provide guidance, training, and performance evaluations to ensure staff's professional development and efficient operation of the branch.
Customer Service:
Ensure exceptional customer service by setting high service standards for the branch.
Address customer inquiries, complaints, and concerns, striving to resolve issues promptly and satisfactorily.
Financial Management:
Monitor and manage branch financial performance, including deposits, loans, profitability, and cost control.
Develop strategies to meet branch-specific targets for deposits, loans, and revenue generation.
Sales and Business Development:
Identify business growth opportunities within the branch's market and develop strategies to attract new customers and increase existing customer engagement.
Cross-sell banking products and services, such as loans, credit cards, investment products, and insurance.
Operational Compliance:
Ensure that the branch operates in compliance with all regulatory and internal policies and procedures.
Conduct regular audits to assess and address any operational risks and maintain accurate records.
Risk Management:
Assess and manage risks associated with the branch's operations, including credit risk, fraud prevention, and security measures.
Implement security protocols to safeguard both physical assets and digital information.
Community Engagement:
Foster positive relationships within the local community to enhance the bank's reputation and visibility.
Represent the bank at community events, seminars, and networking opportunities.
Performance Reporting:
Prepare and present regular reports on branch performance, including financial metrics, customer satisfaction, and business growth.
Staff Development:
Identify training needs within the team and provide ongoing training to enhance employees' skills and knowledge.
Facilitate team-building activities and encourage a positive work environment.
Qualifications:

Bachelor's degree in finance, business administration, or a related field (Master's degree preferred).
Several years of progressive experience in banking, including roles in customer service, sales, and leadership.
Strong knowledge of banking products, services, regulations, and industry trends.
Excellent communication, interpersonal, and problem-solving skills.
Proven leadership abilities with a track record of managing and motivating teams.
Attention to detail, analytical thinking, and ability to make sound financial decisions.
Proficiency in using banking software and technology for operations and reporting.
Working Conditions:

The Bank Manager primarily works in a professional office environment within a bank branch. They may also need to attend off-site meetings, community events, and training sessions. The role typically involves working during regular business hours, but may require occasional overtime based on operational needs.

Note: The above job description is a general overview of the responsibilities and qualifications expected of a Bank Manager. Actual job descriptions may vary based on the specific bank, location, and organizational structur
""",
cv_links_list=["https://uploadthing.com/f/0b9ba010-d81d-48ff-9097-ed604685e6c7_bankmanager1.pdf","https://uploadthing.com/f/9a128f8b-0b49-4f61-8999-ef8cbd20addc_bankmanager2.pdf","https://uploadthing.com/f/4db20476-e3a4-4dc3-a6af-b86a0240ee04_bankmanager3.pdf","https://uploadthing.com/f/6887fc9e-b4b8-41d7-9824-63f8edb39229_bankmanager4.pdf","https://uploadthing.com/f/2ae46f6b-5e0c-4b5b-be3c-f0d5c73fcb35_bankmanager6.pdf","https://uploadthing.com/f/55aea82e-c77f-4eba-ae58-a5616921c8a5_bankmanager7.pdf"
]
)

print(asyncio.run(cvr.generate_rankings()))
          