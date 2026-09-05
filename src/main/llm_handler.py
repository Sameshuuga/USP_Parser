import json
from pydantic import BaseModel, Field, field_validator
from openai import OpenAI
from settings import LLM_API_KEY, DEFAULT_LLM, root_dir


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
    Provide: API key, llm_model
    Useage: calling OpenAI LLM models"""

    def __init__(self, api_key=LLM_API_KEY, llm_model=DEFAULT_LLM):
        self.client = OpenAI(api_key=api_key)

    def call_llm(self, prompt: str, output: LLMOutput = LLMOutput):
        user_input = LLMInput(prompt=prompt)
        response = self.client.responses.parse(
            **user_input.model_dump(exclude={"prompt"}),
            input=[{"role": "user", "content": user_input.prompt}],
            text_format=output,
        )
        parsed: LLMOutput = response.output_parsed
        return parsed


if __name__ == "__main__":
    llm = BaseLLM()
    output_file = root_dir / "data/output/llm.json"

    with open(root_dir / "data/output/ASSAY.txt", "r") as f:
        prompt = f.read()

    user_input = LLMInput(
        prompt=prompt,
        instructions="parse the solution preps from the provided USP Assay test. For each solution return a python dict entry of form {Solution_name: List of steps}. Do not keep the steps minmal.",
    )

    response = llm.call_llm(user_input)
    with open(f"{output_file}", "w") as f:
        json.dump(response.model_dump(), f, indent=2, default=str)
    print(response)
