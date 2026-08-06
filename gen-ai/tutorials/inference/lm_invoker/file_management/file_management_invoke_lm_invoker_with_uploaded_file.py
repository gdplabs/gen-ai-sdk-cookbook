inputs = [uploaded_file, "Explain this file in a single sentence"]
output = await lm_invoker.invoke(inputs)
print(f"output:\n{output}")
