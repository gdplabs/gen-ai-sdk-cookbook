class AdvancedProcessor(BaseProcessor):
    """Processor with additional parameters."""

    async def process(self, data: str) -> str:
        # This implements the abstract method
        return self._transform(data)

    @main
    async def transform(self, data: str, mode: str = "upper") -> str:
        """Transform with configurable mode."""
        if mode == "upper":
            return data.upper()
        elif mode == "lower":
            return data.lower()
        else:
            return data

    def _transform(self, data: str) -> str:
        return data.upper()


# The subclass uses its own @main method
processor = AdvancedProcessor()
result = await processor.run(data="hello", mode="lower")  # Returns "hello"

# The input_params reflects the new signature
ParamsModel = processor.input_params
assert "mode" in ParamsModel.model_fields
