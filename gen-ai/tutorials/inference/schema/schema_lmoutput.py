output = asyncio.run(lm_invoker.invoke("Hello!"))

output.text                 # str — first text response
output.texts                # list[str] — all text responses
output.structured_output    # dict | BaseModel | None — first structured output
output.tool_calls           # list[ToolCall]
output.attachments          # list[Attachment]
output.thinkings            # list[Thinking]
output.token_usage          # TokenUsage | None
output.duration             # float | None — invocation time in seconds
