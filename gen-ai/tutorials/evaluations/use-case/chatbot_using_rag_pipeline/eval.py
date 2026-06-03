"""Example script to evaluate a RAG pipeline using a mock pipeline.

Authors:
    Daniel Adi (daniel.adi@gdplabs.id)

References:
    [1] https://gdplabs.gitbook.io/sdk/how-to-guides/build-end-to-end-rag-pipeline/your-first-rag-pipeline
"""

import asyncio  # used by asyncio.run in __main__
import os

from dotenv import load_dotenv
from gllm_evals import LLMTestCase, evaluate
from gllm_evals.dataset.dict_dataset import DictDataset
from gllm_evals.evaluator.geval_generation_evaluator import GEvalGenerationEvaluator
from gllm_evals.experiment_tracker.csv_experiment_tracker import CSVExperimentTracker
from gllm_inference.lm_invoker import build_lm_invoker

load_dotenv()

# Step 2: Prepare Dataset
# Load from CSV — each row has "query" and "expected_output".
# actual_output and retrieved_context are provided by the mock pipeline below.
DATASET = DictDataset.from_csv("data/eval_dataset.csv").load()
OUTPUT_DIR = "results"

# Mock pipeline outputs keyed by query.
# These are the exact (actual_output, retrieved_context) pairs produced by the
# real RAG pipeline run. retrieved_context includes duplicate chunks as returned
# by the retriever (top_k=5 with duplication).
MOCK_PIPELINE_OUTPUTS: dict[str, tuple[str, str]] = {
    "Give me nocturnal creatures from the dataset": (
        "- Luminafox — a nocturnal creature in Nyxland's luminescent forests; "
        "fur glows softly, bioluminescent trails for navigation, feeds on nocturnal insects.\n"
        "- Dusk Panther — prowls the twilight forests of Shadowglade; fur darkens with night, "
        "stealthy hunter, often considered the guardian of secrets in folklore.",
        "The Luminafox is a nocturnal creature inhabiting the luminescent forests of "
        "Nyxland. With fur that glows softly in the dark, it navigates dense woods using "
        "bioluminescent trails. The Luminafox feeds on nocturnal insects attracted to its "
        "radiant fur, making it both predator and lure. Its large, iridescent eyes allow it "
        "to see in near-total darkness, and its bushy tail emits light patterns used for "
        "communication. Known for its elusive nature, the Luminafox is rarely seen by humans, "
        "adding to the mystique of Nyxland's woods. Legends say that glimpsing a Luminafox "
        "brings good fortune and guidance.\n"
        "The Luminafox is a nocturnal creature inhabiting the luminescent forests of "
        "Nyxland. With fur that glows softly in the dark, it navigates dense woods using "
        "bioluminescent trails. The Luminafox feeds on nocturnal insects attracted to its "
        "radiant fur, making it both predator and lure. Its large, iridescent eyes allow it "
        "to see in near-total darkness, and its bushy tail emits light patterns used for "
        "communication. Known for its elusive nature, the Luminafox is rarely seen by humans, "
        "adding to the mystique of Nyxland's woods. Legends say that glimpsing a Luminafox "
        "brings good fortune and guidance.\n"
        "The Luminafox is a nocturnal creature inhabiting the luminescent forests of "
        "Nyxland. With fur that glows softly in the dark, it navigates dense woods using "
        "bioluminescent trails. The Luminafox feeds on nocturnal insects attracted to its "
        "radiant fur, making it both predator and lure. Its large, iridescent eyes allow it "
        "to see in near-total darkness, and its bushy tail emits light patterns used for "
        "communication. Known for its elusive nature, the Luminafox is rarely seen by humans, "
        "adding to the mystique of Nyxland's woods. Legends say that glimpsing a Luminafox "
        "brings good fortune and guidance.\n"
        "The Dusk Panther prowls the twilight forests of Shadowglade. With fur that darkens "
        "as night approaches, it becomes nearly invisible in low light. Feeding on deer and "
        "wild boar, it is a stealthy and powerful hunter. Its eyes can adjust to varying light "
        "conditions swiftly, giving it an advantage over prey. The Dusk Panther is solitary "
        "and elusive, rarely seen by humans. It is often associated with mystery and is "
        "revered in local folklore as the guardian of secrets.\n"
        "The Dusk Panther prowls the twilight forests of Shadowglade. With fur that darkens "
        "as night approaches, it becomes nearly invisible in low light. Feeding on deer and "
        "wild boar, it is a stealthy and powerful hunter. Its eyes can adjust to varying light "
        "conditions swiftly, giving it an advantage over prey. The Dusk Panther is solitary "
        "and elusive, rarely seen by humans. It is often associated with mystery and is "
        "revered in local folklore as the guardian of secrets.",
    ),
    "Where does the Dreamwhale live and what does it eat?": (
        "- Habitat: The deepest oceans of the Reverie Sea.\n"
        "- Diet: Plankton and small fish, which it filters through baleen-like structures.",
        "The Dreamwhale is an enormous creature roaming the deepest oceans of the Reverie Sea. "
        "Emitting low-frequency sounds that induce vivid dreams in nearby marine life, it is "
        "shrouded in mystery. Feeding on plankton and small fish filtered through baleen-like "
        "structures, it sustains its massive size gracefully. Its skin shimmers with "
        "bioluminescent patterns corresponding to its sonic emissions. Sailors tell tales of "
        "encountering Dreamwhales and experiencing fantastical visions. Considered guardians "
        "of the ocean's secrets, Dreamwhales are a symbol of the unexplored depths and wonders "
        "of the sea.\n"
        "The Dreamwhale is an enormous creature roaming the deepest oceans of the Reverie Sea. "
        "Emitting low-frequency sounds that induce vivid dreams in nearby marine life, it is "
        "shrouded in mystery. Feeding on plankton and small fish filtered through baleen-like "
        "structures, it sustains its massive size gracefully. Its skin shimmers with "
        "bioluminescent patterns corresponding to its sonic emissions. Sailors tell tales of "
        "encountering Dreamwhales and experiencing fantastical visions. Considered guardians "
        "of the ocean's secrets, Dreamwhales are a symbol of the unexplored depths and wonders "
        "of the sea.\n"
        "The Dreamwhale is an enormous creature roaming the deepest oceans of the Reverie Sea. "
        "Emitting low-frequency sounds that induce vivid dreams in nearby marine life, it is "
        "shrouded in mystery. Feeding on plankton and small fish filtered through baleen-like "
        "structures, it sustains its massive size gracefully. Its skin shimmers with "
        "bioluminescent patterns corresponding to its sonic emissions. Sailors tell tales of "
        "encountering Dreamwhales and experiencing fantastical visions. Considered guardians "
        "of the ocean's secrets, Dreamwhales are a symbol of the unexplored depths and wonders "
        "of the sea.\n"
        "Inhabiting the swirling waters of Maelstrom Sea, the Whirlpool Serpent is an aquatic "
        "creature capable of generating whirlpools. With a long, flexible body and fins that "
        "can rotate rapidly, it stirs the ocean currents to trap schools of fish, its primary "
        "diet. Its scales reflect the colors of the deep sea, providing camouflage against "
        "predators. The Whirlpool Serpent communicates through pulsating light patterns along "
        "its body. Sailors regard sightings of this creature as omens of turbulent waters ahead "
        "and often navigate cautiously when it's near.\n"
        "Inhabiting the swirling waters of Maelstrom Sea, the Whirlpool Serpent is an aquatic "
        "creature capable of generating whirlpools. With a long, flexible body and fins that "
        "can rotate rapidly, it stirs the ocean currents to trap schools of fish, its primary "
        "diet. Its scales reflect the colors of the deep sea, providing camouflage against "
        "predators. The Whirlpool Serpent communicates through pulsating light patterns along "
        "its body. Sailors regard sightings of this creature as omens of turbulent waters ahead "
        "and often navigate cautiously when it's near.",
    ),
    "What special ability does the Thunderbeetle have?": (
        "The Thunderbeetle can store electrical energy from lightning in specialized organs, "
        "and during mating season its clusters release that stored electricity to create "
        "spectacular lightning displays. Its highly conductive exoskeleton leads locals to "
        "believe it can influence the weather.",
        "Native to the storm-ridden cliffs of Tempest Ridge, the Thunderbeetle stores "
        "electrical energy from lightning strikes in specialized organs. Feeding on mineral "
        "deposits exposed by erosion, it thrives in harsh conditions. During mating season, "
        "clusters release stored electricity, creating spectacular lightning displays. With "
        "highly conductive exoskeletons, Thunderbeetles are revered by locals who believe they "
        "can influence the weather. They play a pivotal role in the region's mythology and "
        "are often featured in Tempest Ridge art and stories.\n"
        "Native to the storm-ridden cliffs of Tempest Ridge, the Thunderbeetle stores "
        "electrical energy from lightning strikes in specialized organs. Feeding on mineral "
        "deposits exposed by erosion, it thrives in harsh conditions. During mating season, "
        "clusters release stored electricity, creating spectacular lightning displays. With "
        "highly conductive exoskeletons, Thunderbeetles are revered by locals who believe they "
        "can influence the weather. They play a pivotal role in the region's mythology and "
        "are often featured in Tempest Ridge art and stories.\n"
        "Native to the storm-ridden cliffs of Tempest Ridge, the Thunderbeetle stores "
        "electrical energy from lightning strikes in specialized organs. Feeding on mineral "
        "deposits exposed by erosion, it thrives in harsh conditions. During mating season, "
        "clusters release stored electricity, creating spectacular lightning displays. With "
        "highly conductive exoskeletons, Thunderbeetles are revered by locals who believe they "
        "can influence the weather. They play a pivotal role in the region's mythology and "
        "are often featured in Tempest Ridge art and stories.\n"
        "The Stormhorn Beetle is native to the wind-swept plateaus of Gale Heights. Featuring "
        "two prominent horns that conduct electricity, it harnesses energy from frequent "
        "thunderstorms. Feeding on electrically charged plants, it stores energy to ward off "
        "predators. The beetle emits sparks when threatened, deterring attackers. Its exoskeleton "
        "is studied for its unique conductive properties. The Stormhorn Beetle is considered a "
        "herald of storms and is respected for its resilience in harsh weather.\n"
        "The Stormhorn Beetle is native to the wind-swept plateaus of Gale Heights. Featuring "
        "two prominent horns that conduct electricity, it harnesses energy from frequent "
        "thunderstorms. Feeding on electrically charged plants, it stores energy to ward off "
        "predators. The beetle emits sparks when threatened, deterring attackers. Its exoskeleton "
        "is studied for its unique conductive properties. The Stormhorn Beetle is considered a "
        "herald of storms and is respected for its resilience in harsh weather.",
    ),
}

def run_pipeline(query: str) -> tuple[str, str]:
    """Return mock pipeline output for a query.

    Returns:
        (actual_output, retrieved_context)
    """
    return MOCK_PIPELINE_OUTPUTS[query]


async def main():
    # Step 4: Run the pipeline for every case
    pipeline_results = [run_pipeline(row["query"]) for row in DATASET]

    # Build LLMTestCase list — CSV provides input/expected_output,
    # pipeline provides actual_output/retrieved_context
    data = [
        LLMTestCase(
            input=row["query"],
            actual_output=actual_output,
            expected_output=row["expected_output"],
            retrieved_context=retrieved_context,  # required for groundedness
        )
        for row, (actual_output, retrieved_context) in zip(DATASET, pipeline_results)
    ]

    judge_model = build_lm_invoker(
        model_id="google/gemini-3-flash-preview",
        credentials=os.getenv("GOOGLE_API_KEY"),
    )
    tracker = CSVExperimentTracker(
        project_name="rag-chatbot-eval",
        output_dir=OUTPUT_DIR,
        include_eval_result=True,
    )
    experiment_result = await evaluate(
        data=data,
        evaluators=[GEvalGenerationEvaluator(models=judge_model)],
        experiment_tracker=tracker,
    )
    print(experiment_result)


if __name__ == "__main__":
    asyncio.run(main())
