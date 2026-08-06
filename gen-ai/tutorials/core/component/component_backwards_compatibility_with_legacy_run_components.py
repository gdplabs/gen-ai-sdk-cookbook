class LegacyComponent(Component):
    async def _run(self, message: str, priority: int = 1) -> str:
        """Legacy component using _run."""
        return f"[P{priority}] {message}"
