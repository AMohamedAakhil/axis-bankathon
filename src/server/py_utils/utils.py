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
          self.llm = OpenAI(temperature=0.2)
     def build_chains(self):
          prompt1 = """
          Given a Job description for the Job title: {job_title},
          Analyse the description and identify these elements:

          Summary/objective, Essential functions,
          Competency, Supervisory responsibilities, 
          Work environment, Physical demands, 
          Position type, Travel, Required education, 
          Preferred education, Additional eligibility

          Scan the description for the presence of each of these elements,
          ONLY Return a dictionary where the key of dictionary is name of the element and
          the value of this is 0 or 10. 
          0 indicates the absence of the element and 10 indicates the presence.
          -----
          Job description :
          {job_description}


          Make sure to return only the raw dictionary, not code
          """

          prompt1_template = PromptTemplate(
               input_variables=["job_title", "job_description"],
               template= prompt1
          )

          chain1 = LLMChain(llm = self.llm, prompt=prompt1_template, 
                            output_key="dictionary"
                        )
          
          
          prompt2_template = PromptTemplate(
               input_variables=["dictionary"],
               template = """
              Given a dictionary, calculate the total sum of all the values, only return the sum
              {dictionary}

              make sure to return only the integer without any
               """
          )

          chain2 = LLMChain(llm = self.llm, prompt= prompt2_template,
                            output_key= "sum")
          
          overall_chain =SequentialChain(
               chains = [chain1, chain2],
               input_variables = ["job_title", "job_description"],
               output_variables = ["dictionary", "sum"],
               verbose = True

          )

          sum = overall_chain({"job_title": self.job_title,
                  "job_description": self.job_description})
          
          return sum # output not parsed yet, to be done soon  
          
          
    

def cv_score(list_cv_texts, job_title):
        llm = OpenAI(temperature=0)
        prompt  = PromptTemplate(
                                input_variables= ['list_cv_texts','job_title'],
                                template= """
                                Based on the list of CVs given to you, compare them
                                and rank the CVs on how suited they are for the given job title: {job_title}

                                List of CVs:
                                {list_cv_texts}


                                """
                            )
            
        chain = LLMChain(llm=llm, prompt=prompt )
        ret  = chain.run(list_cv_texts=list_cv_texts, job_title = job_title)
        return ret
     
    

def job_desc_score(job_title, job_description):
        llm = OpenAI(temperature=0)
        prompt  = PromptTemplate(
                            input_variables= ['job_title', 'job_description'],
                            template= """
                            Based on the job title: {job_title}
                            Score this job description out of 100:
                            '{job_description} '.
                            A Job description is supposed to consist of these : 
                            Classification, Salary grade, Reports to, Date, Summary/objective, Essential functions, Competency, Supervisory responsibilities, Work environment, Physical demands, Position type, Travel, Required education, Preferred education, Additional eligibility
                            For each available point, you score it 10 points.
                            
                            ONLY Return a nicely formatted string where the first element is just the final score out of 100 and the second element is a string which contains the potential enhancements of the description provided. If there are no enhacements just mention it. 
                            """
                        )
        
        chain = LLMChain(llm=llm, prompt=prompt )
        ret  = chain.run(job_title = job_title, job_description= job_description)
        return ret






def job_desc_score(job_title, job_description):
        llm = OpenAI(temperature=0)
        prompt  = PromptTemplate(
                            input_variables= ['job_title', 'job_description'],
                            template= """
                            Based on the job title: {job_title}
                            Score this job description out of 100:
                            '{job_description} '.

                            Return a list where the first element is just the score out of 100 and the second element is a string which contains the potential enhancements of the description provided


                            """
                        )
        
        chain = LLMChain(llm=llm, prompt=prompt )
        ret  = chain.run(job_title = job_title, job_description= job_description)
        return ret
        



