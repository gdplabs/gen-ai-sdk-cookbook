import json

with open("path/to/lm_invoker_catalog.json") as f:
    records = json.load(f)

catalog = LMInvokerCatalog.from_records(records=records)
query_transformer = catalog.query_transformer
