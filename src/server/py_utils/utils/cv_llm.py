import requests
from pypdf import PdfReader
import os
from langchain.chains import LLMChain, SequentialChain
from langchain.llms import OpenAI


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
    
class CVLLM:
    def __init__(self, CV_list, job_title, job_description) -> None:
        self.CV_list = CV_list
        self.job_title = job_title
        self.job_descripiton = job_description
        self.llm = OpenAI(temperature=0.6, max_tokens=-1, openai_api_key=OPENAI_API_KEY)

        with open("src/server/py_utils/elements.json") as elements_file:
               self.elements = json.load(elements_file)
    async def build_dict(self):
          prompt1 = """
          Given a CV and Job description for the Job title: {job_title},
          Analayse the CV and identify the follwing component:
        
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
