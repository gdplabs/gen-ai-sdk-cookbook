class DataProcessor(Component):
    @main
    async def process(
        self,
        data: list[dict],
        limit: int = 100,
        **options,
    ) -> dict:
        """Process data with optional filters."""
        processed = data[:limit]
        return {
            "count": len(processed),
            "data": processed,
            "options": options,
        }
