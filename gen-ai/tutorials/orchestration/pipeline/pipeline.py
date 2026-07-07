import asyncio
from pydantic import BaseModel, Field, ValidationError
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps._func import transform

# Define your state as a Pydantic BaseModel for automatic validation
class ScoreState(BaseModel):
    score: int = Field(..., gt=0, description="Score must be positive")
    scaled_score: float = Field(default=0.0)
    message: str = Field(default="")

# Input schema (filter what's passed to the pipeline)
class ScoreInput(BaseModel):
    score: int = Field(..., gt=0, le=100, description="Input score between 1-100")

# Output schema (filters what's returned)
class ScoreOutput(BaseModel):
    scaled_score: float = Field(..., description="The scaled score value")
    message: str = Field(..., description="Notification message")

def scale_score(data: dict) -> float:
    return float(data["score"] * 1.5)

def create_message(data: dict) -> str:
    return f"Processed score: {data['scaled_score']}"

pipe = Pipeline(
    steps=[
        transform(scale_score, input_map=["score"], output_state="scaled_score"),
        transform(create_message, input_map=["scaled_score"], output_state="message"),
    ],
    state_type=ScoreState,    # LangGraph validates THIS during execution
    input_type=ScoreInput,    # Used for manual validation and tool conversion
    output_type=ScoreOutput,  # Filters the returned state
)

# Example 1: Manual validation using input schema before invoking
try:
    user_input = {"score": 10}
    validated_input = ScoreInput(**user_input)  # Validate manually

    # Create initial state from validated input
    initial_state = ScoreState(score=validated_input.score)
    result = asyncio.run(pipe.invoke(initial_state.model_dump()))
    print(result)
    # Only outputs: {'scaled_score': 15.0, 'message': 'Processed score: 15.0'}
except ValidationError as e:
    print(f"Input validation error: {e}")

# Example 2: State validation by LangGraph (score must be > 0)
try:
    # This will fail LangGraph's state validation (score not > 0)
    bad_state = ScoreState(score=-5)  # Pydantic validates immediately
    asyncio.run(pipe.invoke(bad_state.model_dump()))
except ValidationError as e:
    print(f"State validation error: {e}")

# Example 3: Input schema validates stricter constraints (score <= 100)
try:
    user_input = {"score": 150}  # Valid for state, but invalid for input
    validated_input = ScoreInput(**user_input)  # Fails: score > 100
except ValidationError as e:
    print(f"Input validation error: {e}")  # This will catch it
