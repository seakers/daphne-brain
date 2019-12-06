import os
import urllib.parse


def list_procedure_steps(procedure):
    step_list = ["Step 1", "Step 2", "Step 3"]
    step_id = [1, 2, 3]
    steps = {}
    steps["text"] = step_list
    steps["id"] = step_id
    results = [steps]
    return results


def procedure_pdf_name(procedure):
    procedure_pdfs = os.listdir('C:/Users/Michael/Documents/repos/daphne_brain/AT/Databases/procedures')
    pdf_name = procedure_pdfs[int(procedure)-1]
    return urllib.parse.urlencode({"filename": pdf_name})