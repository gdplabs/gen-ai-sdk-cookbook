from gllm_docproc.loader.pdf import PyMuPDFLoader

source = "pdf-example.pdf"


# load source
from gllm_docproc.loader.pdf import PDFPlumberLoader, PyMuPDFLoader
from gllm_docproc.loader.pipeline_loader import PipelineLoader

pipeline_loader = PipelineLoader()
pipeline_loader.add_loader(PyMuPDFLoader())
pipeline_loader.add_loader(PDFPlumberLoader())

loaded_elements = loader.load(source)

# parse
from gllm_docproc.parser.document import PDFParser
from gllm_docproc.parser.table import TableCaptionParser
from gllm_docproc.parser.pipeline_parser import PipelineParser

pipeline = PipelineParser()
pipeline.add_parser(PDFParser())
pipeline.add_parser(TableCaptionParser())

parsed_elements = parser.parse(loaded_elements)

# chunk
from gllm_docproc.chunker.structured_element import StructuredElementChunker
chunker = StructuredElementChunker()
chunked_elements = chunker.chunk(parsed_elements)

# index to vector database
from gllm_docproc.indexer.vector.vector_db_indexer import VectorDBIndexer
indexer = VectorDBIndexer()

result = indexer.index(
    elements=chunked_elements,
    file_id="file_001",
    vectorizer_kwargs={
        "model": "openai/text-embedding-3-small",  # Format: "provider/model_name"
        "api_key": "<OPENAI_API_KEY>",
    },
    db_engine="elasticsearch",  # Supported: "chroma", "elasticsearch", "opensearch"
    db_config={
        "url": "http://localhost:9200", # change to your Elasticsearch URL
        "index_name": "my_index", # change to your index name
    },
)
