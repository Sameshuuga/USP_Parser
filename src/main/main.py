import os
from pathlib import Path

import settings
import usp_parser as upar
import llm_handler as llm

root_dir = settings.root_dir
data_dir = root_dir / "data/"
monograph = "USP-NF Ketamine Hydrochloride"
document = data_dir / f"input/pdfs/{monograph}.pdf"
LLM = llm.BaseLLM()


def generate_steps(monograph_pdf_Path, test: str):
    monograph: dict = upar.usp_parser(monograph_pdf_Path)
    raw_llm_output = LLM.call_llm(monograph.get(test))
    instructions = raw_llm_output.solutions_dict
    print(instructions)
    pass


if __name__ == "__main__":
    generate_steps(document, "ASSAY")
