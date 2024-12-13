import json
import os
import sys
import traceback
from pdf_pseudo import PdfPseudo
from transform_recognizer import TransformerRecognizer

# render a response
def render_response(response):
    print(json.dumps(response))
    exit(1)

try:
    # load input and output path
    count_of_args = len(sys.argv)
    if count_of_args < 4:
        render_response(response={"success": False, "error": "Please provide valid arguments"})

    # load args and check action
    pdfs_input_path, results_output_path, action = sys.argv[1:4]
    pdfs_input_path = pdfs_input_path.split(",")
    results_output_path = results_output_path.split(",")
    valid_actions = ["anonymise", "reconstruct"]
    reconstruct_entities_map = []

    if not action in valid_actions:
        render_response(response={"success": False, "error": "Invalid action"})

    if action == "reconstruct":
        if count_of_args < 5:
            render_response(response={"success": False, "error": "The entities map is expected"})
        else:
            with open(sys.argv[4],"rb") as f:
                reconstruct_entities_map = json.loads(f.read())
                f.close()

            os.remove(sys.argv[4])

    # apply action
    analyzer = TransformerRecognizer.build_analyser()
    result_map = {}

    for index in range(len(pdfs_input_path)):
        pdf_input_path = pdfs_input_path[index]
        result_output_path = results_output_path[index]

        pdf_pseudo = PdfPseudo(input_file_path=pdf_input_path,analyser=analyzer)

        if action == "anonymise":
            entities_map = pdf_pseudo.anonymise(output_file_path= result_output_path)
            result_map[pdf_input_path] = entities_map
        elif action == "reconstruct":
            pdf_pseudo.reconstruct(entities_map=json.loads(reconstruct_entities_map[index]))

        pdf_pseudo.save_result_in(output_file_path=result_output_path)
        pdf_pseudo.free_resources(output_file_path=result_output_path)

    render_response(response={"success": True, "entities_map": result_map})
except Exception as e:
    traceback.print_exc()
    print(e)
    render_response(response={"success": False, "error": "Unexpected error"})
