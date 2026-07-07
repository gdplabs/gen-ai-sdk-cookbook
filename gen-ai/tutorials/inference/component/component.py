from gllm_inference.component import LMComponent, LMComponentSlot
from gllm_core.schema import main


class MapReduceComponent(LMComponent):
    lm_slots = {
        "map": LMComponentSlot(
            prompt_vars={"context", "query"},
            default_system_template="Map the context for query: {query}",
            default_user_template="{context}",
        ),
        "reduce": LMComponentSlot(
            prompt_vars={"context", "query"},
            default_system_template="Reduce the mapped context for query: {query}",
            default_user_template="{context}",
        ),
    }

    @main
    async def summarize(self, context: str, query: str) -> str:
        mapped = await self._invoke_lm(slot="map", context=context, query=query)
        reduced = await self._invoke_lm(slot="reduce", context=mapped.text, query=query)
        return reduced.text
