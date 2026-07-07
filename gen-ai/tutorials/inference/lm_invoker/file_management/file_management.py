files = await lm_invoker.file.list()

if not files:
    print("No files found.")

for file in files:
    print(f" - {file}")
