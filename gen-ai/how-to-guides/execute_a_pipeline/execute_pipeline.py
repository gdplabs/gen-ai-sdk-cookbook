# Initialize the pipeline
pipeline = step_1 | step_2 | step_3  # or replace it with your prebuilt pipeline

# Prepare initial state
initial_state = {
    "user_query": "What is machine learning?",
    "history": "",
    "context": ""
}

# Execute the pipeline
final_state = await pipeline.invoke(initial_state)

# Access the results
response = final_state["response"]
references = final_state["references"]
