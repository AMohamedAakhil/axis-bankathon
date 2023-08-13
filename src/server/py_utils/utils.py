from pypdf import PdfReader
import os
import requests
from langchain.chains import LLMChain, SequentialChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent
from langchain.agents import AgentType
import asyncio
import json




os.environ["OPENAI_API_KEY"] = ""

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
    
class JobDescLLM:
     def __init__(self, job_title, job_description) -> None:
          self.job_title = job_title
          self.job_description = job_description
          self.llm = OpenAI(temperature=0.6)

          with open("src/server/py_utils/elements.json") as elements_file:
               self.elements = json.load(elements_file)




     async def build_dict(self):
          prompt1 = """
          Given a Job description for the Job title: {job_title},
          Analyse the description and identify the following component:

         {field}: {field_info}

          Scan the description for the presence of this field, Identify the segment.
          ONLY Return a json formatted string where the property name is {field} and value is the identied segment
          If you cannot identify the segment, The value of the property should be null.
          -----
          Job description :
          {job_description}


          Make sure to RETURN ONLY JSON, not code or any other text. 
          """

          prompt1_template = PromptTemplate(
               input_variables=["job_title" ,"job_description", "field", "field_info"],
               template= prompt1
          )

          chain1 = LLMChain(llm = self.llm, prompt=prompt1_template, 
                            output_key="dictionary"
                        )
          
          dict_chain = SequentialChain(
               chains = [chain1],
               input_variables = ["job_title", "job_description", "field", "field_info"],
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
               "job_description": self.job_description
               }

               tasks.append(self.async_generate(dict_chain, inputs))
          results = await asyncio.gather(*tasks)

          elements_dict = {}
          
          for json_stuff in results:
               temp_ = json.loads(json_stuff)
               name_ = list(temp_.keys())[0]
               
               elements_dict[name_] = temp_[name_]
          return elements_dict

     
     async def async_generate(self, sqc, inputs):
          resp = await sqc.arun(inputs)
          return resp
     
     
     async def generate_score_concurrently(self):

          
          pt = PromptTemplate(
               input_variables=["job_title", "field", "field_info", "field_val"],
               template = """
              Your company is recruting employees for the job, {job_title}. Your boss 
              has written the {field} for this job, Your job is to evaluate on How 
              well he has written it. See if the given {field} is actually relevant for 
              the job and whether or not it accurately describes the {field} REQUIRED.
              FOR SOMEBODY TO FUNCTION EFFECTIVELY AS A {job_title}. Based on this, Score the
              {field} out of 10. If the field has been listed as null, give the score as 0
              You are allowed to use decimal values, Return ONLY THE SCORE AND NO OTHER TEXT.

              {field} = {field_info}. 
              ---
              This is what your boss has written:

              {field_val}
              ---
              
          """
          )
          chain = LLMChain(llm = self.llm,
                           prompt=pt,
                           output_key="score")
          
          sqc = SequentialChain(
               chains = [chain],
               input_variables = ["job_title", "field", "field_info", "field_val"],
               output_variables = ["score"],
               verbose = False
          )

          elements_dict = await self.build_dict() 
          #print("ELEM DICT:", elements_dict)
          tasks = []

          for field in elements_dict.keys():
               field_info = self.elements[field]
               field_val = elements_dict[field]
               inputs = {
               "job_title": self.job_title,
               "field": field,
               "field_info": field_info,
               "field_val": field_val
               }

               tasks.append(self.async_generate(sqc, inputs))

          results = await asyncio.gather(*tasks)
          sum_score = sum([float(i) for  i in results])
          return sum_score
          

 
      
jdl = JobDescLLM("Bank manager",
                 """
We are seeking an experienced and dynamic individual to fill the role of Bank Manager at our reputable financial institution. The Bank Manager will be responsible for overseeing the daily operations of the branch, ensuring excellent customer service, managing a team of dedicated professionals, and achieving financial targets. The successful candidate will demonstrate strong leadership skills, a deep understanding of banking products and services, and the ability to foster a positive and collaborative work environment. 
Responsibilities:

Lead, mentor, and motivate a team of banking professionals to provide exceptional customer service and meet performance goals.
Manage branch operations, including transaction processing, account management, and compliance with regulatory guidelines.
Develop and execute strategies to attract and retain customers while promoting a range of banking products and services.
Collaborate with regional management to set and achieve branch-specific financial targets and operational objectives.
Monitor and maintain compliance with industry regulations and internal policies to ensure a secure and efficient banking environment.
Build and maintain strong relationships with customers, local businesses, and community organizations to enhance the bank's reputation and market presence.
Analyze financial reports and market trends to make informed decisions that optimize branch performance and profitability.
Implement training programs to enhance employee skills and knowledge, ensuring the delivery of accurate and up-to-date information to customers.
Handle escalated customer inquiries and resolve complex issues in a timely and professional manner.
Prepare and present regular reports on branch performance, operational metrics, and customer feedback to senior management.

Qualifications:

Bachelor's degree in Finance, Business Administration, or related field (Master's degree preferred).
Minimum of 5 years of progressive experience in banking, including roles in customer service, operations, and leadership.
Strong understanding of financial products, regulations, and industry trends.
Excellent interpersonal, communication, and leadership skills.
Proven track record of achieving and exceeding financial targets.
Ability to make informed decisions under pressure and adapt to a rapidly changing banking landscape.
Proficiency in banking software and systems.
Exceptional problem-solving and decision-making abilities.
Strong commitment to ethical conduct and integrity.

""")
asyncio.run(jdl.generate_score_concurrently())   


     
    








