from pypdf import PdfReader
import requests
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os


os.environ["OPENAI_API_KEY"] = "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"


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



        

    

    


