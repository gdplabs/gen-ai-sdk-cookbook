import json
from gllm_docproc.loader.docx import PythonDOCXLoader

source = "docx-example.docx"

# initialize DOCX Loader
loader = PythonDOCXLoader()

# load source
loaded_elements = loader.load(source)

print(json.dumps(loaded_elements, indent=4))
