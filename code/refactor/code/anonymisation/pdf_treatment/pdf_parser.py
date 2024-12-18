from typing import Callable, List
from spire.pdf import PdfDocument,PdfTextExtractor,PdfTextExtractOptions,PdfImageHelper,PdfTextReplacer,Utilities_PdfImageInfo

class PDFParser:
    """
        application pdf parser
    """

    pdf_file_path: str

    """
        application configuration
    """

    def __init__(self, pdf_file_path: str):
        """
        :param pdf_file_path: pdf file to parse absolute path
        """
        self.pdf_file_path = pdf_file_path

    def parse_content(self,todo_during_parsing: Callable[[str,List[Utilities_PdfImageInfo],PdfTextReplacer,PdfImageHelper],None]) -> PdfDocument:
        """
        parse the pdf file
        :param todo_during_parsing: callable called during the parsing step
        :return:
        PdfDocument: parsing pdf document
        """
        try:
            # load pdf document
            pdf = PdfDocument()
            pdf.LoadFromFile(self.pdf_file_path)

            # define utils
            pdf_image_helper = PdfImageHelper()
            extraction_options = PdfTextExtractOptions()

            # parse pages
            for page_index in range(0,pdf.Pages.Count):
                page = pdf.Pages[page_index]
                page_text_replacer = PdfTextReplacer(page)

                # extract text and images
                page_text = PdfTextExtractor(page= page).ExtractText(options= extraction_options)
                page_images = pdf_image_helper.GetImagesInfo(page= page)

                todo_during_parsing(page_text,page_images,page_text_replacer,pdf_image_helper)

            return pdf
        except Exception as _:
            raise Exception("Fail to parse pdf file")