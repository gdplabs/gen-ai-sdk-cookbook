"""Example of basic CRUD operations and query methods with gllm-datastore.

References:
    [1] https://gdplabs.gitbook.io/sdk/tutorials/data-store/basic-crud-and-methods
"""

from gllm_core.schema import Chunk
from gllm_datastore.core.filters import QueryOptions, filter as F

chunk = Chunk(
    id="note-1",
    content="Order 938 is ready for pickup",
    metadata={"store": "jakarta", "status": "ready"},
)
