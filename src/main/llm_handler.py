import json, logging
from pydantic import BaseModel, Field, field_validator
from openai import OpenAI
from main.settings import LLM_API_KEY, DEFAULT_LLM, root_dir

logger = logging.getLogger(__name__)


class LLMInput(BaseModel):
    model: str = DEFAULT_LLM
    prompt: str = Field(
        ..., min_length=1, description="Raw USP Assay test text to parse."
    )
    instructions: str = (
        "Parse the solution preparation steps from the provided USP Assay test. "
        "For each solution, return a Python dict entry of the form "
        "{solution_name: list_of_steps}. Each step should be a complete, "
        "self-contained instruction — do not omit reagents, quantities, "
        "concentrations, or conditions. Do not abbreviate or minimize the steps."
    )
    # reasoning_effort: Literal["minimal", "low", "medium", "high"] = "minimal"
    max_output_tokens: int = Field(default=5000, gt=0, le=10000)
    temperature: float = Field(default=1.0, ge=0.0, le=2.0)
    top_p: float = Field(default=1.0, gt=0.0, le=1.0)
    stream: bool = False
    background: bool = False

    @field_validator("prompt")
    @classmethod
    def prompt_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("prompt must not be blank or whitespace-only")
        return v


class LLMOutput(BaseModel):
    class Solution(BaseModel):
        solution_name: str
        steps: list[str]

    generated_text: str
    solutions: list[Solution]

    @property
    def solutions_dict(self) -> dict[str, str]:
        return {s.solution_name: "\n".join(s.steps) for s in self.solutions}


class BaseLLM:
    """pydantic schema input ---> LLM ---> pydantic schema output
    Provide: API key, llm_model"""

    def __init__(self, api_key=LLM_API_KEY, llm_model=DEFAULT_LLM):
        self.client = OpenAI(api_key=api_key)

    def call_llm(
        self, prompt: str, output: type[LLMOutput] = LLMOutput
    ) -> LLMOutput | None:
        user_input = LLMInput(prompt=prompt)
        response = self.client.responses.parse(
            **user_input.model_dump(exclude={"prompt"}),
            input=[{"role": "user", "content": user_input.prompt}],
            text_format=output,
        )
        parsed: LLMOutput | None = response.output_parsed
        return parsed


if __name__ == "__main__":
    pass
