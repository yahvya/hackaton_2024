import os

from anonymisation.pdf_treatment.pdf_parser import PDFParser
from configuration.app_config import AppConfig

if __name__ != "__main__":
    exit(1)

# load configuration
app_config = AppConfig.load_from_yaml(application_root_path= os.getcwd(),config_file_path= "/secure-storage/env.yaml")

PDFParser(pdf_file_path= "secure-storage/test-pdf.pdf").parse_content(
    todo_during_parsing= lambda page_text,page_images,page_text_replacer,page_image_helper : None
)