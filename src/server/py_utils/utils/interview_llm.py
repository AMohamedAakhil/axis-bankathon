from pypdf import PdfReader
import os
import requests
from langchain.chains import LLMChain, SequentialChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import asyncio
import json
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


class InterviewLLM:
     def __init__(self, job_title, job_description, cv) -> None:
          self.job_title = job_title
          self.job_description = job_description
          self.cv = cv
          self.llm = OpenAI(temperature=0.6, max_tokens=-1, openai_api_key=OPENAI_API_KEY)

     def generate_questions(self):
          prompt1 = """
          You are a recruiter for a company. You are recruiting for the role of {job_title}. 
          The description of the role is as follows: {job_description}
          The applicant's CV is as follows: {CV}

          You have to generate questions for the applicant based on the CV and the job description.
          Make sure to RETURN ONLY JSON, not code or any other text. 
          """

          prompt1_template = PromptTemplate(
               input_variables=["job_title" ,"job_description", "CV"],
               template= prompt1
          )

          chain1 = LLMChain(llm = self.llm, prompt=prompt1_template, 
                            output_key="dictionary"
                        )
          return chain1.run(job_title=self.job_title, job_description=self.job_description, CV=self.cv)
     


