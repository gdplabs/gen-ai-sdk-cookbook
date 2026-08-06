output = await self._invoke_lm(query="Summarize this.")
structured = self._parse_structured_output(output)

if structured:
    print(structured["summary"])
