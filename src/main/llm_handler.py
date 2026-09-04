import os, json
from typing import Optional
from pydantic import BaseModel
from openai import OpenAI
from settings import LLM_API_KEY, DEFAULT_LLM, root_dir


class BaseLLM:
    """pydantic schema input ---> LLM ---> pydantic schema output
    Provide: API key, llm_model
    Useage: calling OpenAI LLM models"""

    def __init__(self, api_key=LLM_API_KEY, llm_model=DEFAULT_LLM):
        self.client = OpenAI(api_key=api_key)
        self.default_output_file = root_dir / "data/output/llm.json"

    def call_llm(self, user_input, output=None, output_file=None):
        """method to call the llm, send input, return response"""
        if output is None:
            output = LLMOutput
        if output_file is None:
            output_file = self.default_output_file

        response = self.client.responses.parse(
            **user_input.model_dump(exclude={"prompt"}),
            input=[{"role": "user", "content": user_input.prompt}],
            text_format=output,
        )

        with open(f"{output_file}", "w") as f:
            json.dump(response.model_dump(), f, indent=2, default=str)
        return response


class LLMInput(BaseModel):
    model: str = DEFAULT_LLM
    prompt: str
    instructions: str = ""
    # reasoning: dict = {"effort": "minimal"}
    max_output_tokens: Optional[int] = 5000
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0
    stream: Optional[bool] = False
    background: Optional[bool] = False


class Solution(BaseModel):
    solution_name: str
    steps: list[str]


class LLMOutput(BaseModel):
    generated_text: str
    solutions: list[Solution]

    @property
    def solutions_dict(self) -> dict[str, list[str]]:
        """solution_name -> steps, derived from the structured list."""
        return {s.solution_name: s.steps for s in self.solutions}


# class LLMOutput(BaseModel):
#     generated_text: str
#     solution_name: str
#     prep_steps: list[str]


if __name__ == "__main__":
    llm = BaseLLM()
    with open(root_dir / "data/output/ASSAY.txt", "r") as f:
        prompt = f.read()
    user_input = LLMInput(
        prompt=prompt,
        instructions="parse the solution preps from the provided USP Assay test. For each solution return a python dict entry of form {Solution_name: List of steps}. Do not keep the steps minmal.",
    )
    response = llm.call_llm(user_input)
    print(response)
