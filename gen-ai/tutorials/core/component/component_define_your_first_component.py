from gllm_core.schema import Component, main


class TextFormatter(Component):
    @main
    async def format(self, text: str, uppercase: bool = False, repeat: int = 1) -> str:
        """Format text with options."""
        result = text.upper() if uppercase else text
        return result * repeat
