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
          self.llm = OpenAI(temperature=0.6)

          with open("src/server/py_utils/elements.txt") as elements_file:
               self.elements = elements_file.read()

     def build_chains(self):
          prompt1 = """
          Given a Job description for the Job title: {job_title},
          Analyse the description and identify these elements:

         {elements}

          Scan the description for the presence of each of these elements, Shorten the identified segment.
          ONLY Return a dictionary where the key of dictionary is name of the name of the element and the value is the shortened segment.
          If you can't identify the segment then just fill the value as None
    
          -----
          Job description :
          {job_description}


          Make sure to return only the raw dictionary, not code
          """

          prompt1_template = PromptTemplate(
               input_variables=["job_title" ,"job_description", "elements"],
               template= prompt1
          )

          chain1 = LLMChain(llm = self.llm, prompt=prompt1_template, 
                            output_key="dictionary"
                        )
          

          
     
          
          prompt2_template = PromptTemplate(
               input_variables=["dictionary", "elements", "job_title"],
               template = """
              Your boss has written a job description to hire employees. You have been 
              asked to evaluate the job description

              Given a dictionary that contains these fields:
              {elements}


              Analyse The fields for the given job: {job_title} and give it a 
              score on how well it has been written with regard to the job title.
              This score has to be out of 10, You are allowed to use decimal values
              Return ONLY a new dictionary that contains the name of the field and the score for that field.
              ---
              {dictionary}
               """
          )


          chain2 = LLMChain(llm = self.llm, prompt= prompt2_template,
                            output_key= "score_dict")
          
          prompt3_template = PromptTemplate(
               input_variables=["score_dict"],
               template = """
              Given a dictionary, calculate the total sum of all the values, only return the sum
              {score_dict}

              make sure to return only the integer without any text
               """
          )

          chain3 = LLMChain(llm = self.llm, prompt= prompt3_template,
                            output_key= "sum")

          

          
          overall_chain =SequentialChain(
               chains = [chain1, chain2, chain3],
               input_variables = ["job_title", "job_description", "elements"],
               output_variables = ["dictionary", "score_dict", "sum"],
               verbose = True

          )

          sum = overall_chain({"job_title": self.job_title,
                  "job_description": self.job_description,
                  "elements": self.elements})


          
          return sum # output not parsed yet, to be done soon  
      
jdl = JobDescLLM("Bank manager",
                 """
Job Summary:
We're looking for someone to fill the role of Bank Manager. The Bank Manager will be responsible for whatever happens at the branch, including dealing with customers, telling employees what to do sometimes, and making sure things are okay, I guess.

Responsibilities:

Do stuff that a manager does, like managing things.
Handle customers when they complain or something.
Tell employees to do their job, maybe.
Make sure the branch doesn't fall apart, hopefully.

Qualifications:

You need to have some sort of degree, I guess.
Maybe a few years of experience in banking or something, but if not, it's fine.
Just be good at talking to people, or whatever.
You should probably know how to use a computer, but we won't provide training.
Be okay with taking the blame if things go wrong, even if it's not your fault.
""")
print(jdl.build_chains())     




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
     
    








