from gllm_core.schema import Tool


lc_tool = ...  # Some LangChain tool
mcp_tool = Tool.from_langchain(lc_tool)


google_decl = ...  # Google ADK function declaration
mcp_tool_2 = Tool.from_google_adk(google_decl)
