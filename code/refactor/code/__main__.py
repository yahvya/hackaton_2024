import os

from anonymisation.pdf_treatment.pdf_parser import PDFParser
from anonymisation.recognition.text.text_recognizer import TextRecognizer
from configuration.app_config import AppConfig

if __name__ != "__main__":
    exit(1)

# load configuration
app_config = AppConfig.load_from_yaml(
    application_root_path= os.getcwd(),
    config_file_path= "/secure-storage/env.yaml"
)

"""
PDFParser(pdf_file_path= "secure-storage/test-pdf.pdf").parse_content(
    todo_during_parsing= lambda page_text,page_images,page_text_replacer,page_image_helper : None
)
"""

analyze_results = TextRecognizer(ignore_labels=["O","MISC"]).analyze(text= """
Bonjour, je m'appelle Jean Dupont et je travaille chez TechCorp International. Mon numéro de téléphone est le +33 6 12 34 56 78 et mon adresse email est jean.dupont@techcorp.com. J'habite au 25 rue des Lilas, 75000 Paris, France.

Voici quelques informations supplémentaires :

Numéro de carte bancaire : 1234 5678 9012 3456, date d'expiration : 12/26, code CVC : 789.
Compte bancaire IBAN : FR76 3000 6000 0112 3456 7890 189, BIC : BNPAFRPPXXX.
Mon adresse IP récente : 192.168.1.1.
URL de mon site web : https://www.jeandupont-tech.fr.
De plus, j'ai récemment visité New York le 15 août 2023 pour un séminaire médical où j'ai présenté mon numéro de licence médicale : ML-987654321.

Si vous avez besoin de me joindre rapidement, vous pouvez m'écrire à contact@jeandupont.fr ou m'appeler sur mon téléphone professionnel : +33 1 23 45 67 89.

Cordialement,
Jean Dupont
""")
for result in analyze_results:
    print(result)