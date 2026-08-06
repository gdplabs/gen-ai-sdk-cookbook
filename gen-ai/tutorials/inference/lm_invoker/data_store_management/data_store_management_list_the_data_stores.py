stores = await lm_invoker.data_store.list()

if not stores:
    print("No stores found.")

for store in stores:
    print(f" - {store}")
