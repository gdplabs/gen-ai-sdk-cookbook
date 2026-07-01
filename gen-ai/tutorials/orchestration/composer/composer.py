pipeline = (
    Pipeline()
    .composer
    .step(my_component, {"input": "query"}, "result")
    .log("Processing result: {result}")
    .transform(lambda data: data["result"].upper(), ["result"], "upper_result")
    .terminate()
    .done()
)
