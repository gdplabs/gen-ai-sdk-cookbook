requests = {
    "request_1": "What color is the sky?",
    "request_2": "What color is the grass?",
}
batch_id = await lm_invoker.batch.create(requests)
