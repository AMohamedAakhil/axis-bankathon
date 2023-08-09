from pypdf import PdfReader
import requests


class ReadPDF:
    def __init__(self, url):
        self.url = url
        self.response = requests.get(url)
        self.dir = 'temp/temp.pdf'

    def read(self):
        with open(self.dir, 'wb') as fd:
            fd.write(self.response.content)

        reader = PdfReader(self.dir)
        text_per_page = []

        for page in reader.pages:
            text_per_page.append(page.extract_text())
            
        return text_per_page


        




