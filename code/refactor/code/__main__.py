import os
import ctypes

from application.anomynisation.anonymiser import Anonymiser
from application.configuration.app_config import AppConfig

if __name__ != "__main__":
    exit(1)

# manual load of libSkiaSharp.ddl from spire.pdf to work
dll_path = os.path.abspath("venv/lib/site-packages/spire/pdf/lib/libSkiaSharp.dll")
ctypes.windll.LoadLibrary(dll_path)

# load app configuration
app_config = AppConfig.load_from_yaml(
    application_root_path= os.getcwd(),
    config_file_path= "/secure-storage/env.yaml"
)

result_pdf = Anonymiser.anonymise_pdf(pdf_file_path= "secure-storage/test-pdf.pdf")
result_pdf.SaveToFile("./secure-storage/result.pdf")
result_pdf.Close()