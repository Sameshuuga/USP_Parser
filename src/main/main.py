#!/usr/bin/env /home/sameshuuga/Projects/USP_Parser/.venv/bin/python3

import sys, logging
from pathlib import Path

import settings, ui
import usp_parser as upar
import llm_handler as llm
import excel_writer as ew

logger = logging.getLogger(__name__)
logging.basicConfig(filename=settings.log_file, level=logging.INFO)


def print_steps(steps: dict):
    for key, step in steps.items():
        print(f"\n{key}:\n{step}")


def generate_steps(monograph: dict, test: str):
    raw_llm_output = llm.BaseLLM().call_llm(monograph.get(test))
    instructions = raw_llm_output.solutions_dict
    print_steps(instructions)
    return instructions


def main():
    while True:
        args = ui.build_parser().parse_args()
        monograph: dict = upar.usp_parser(ui.file_menu(args.input))
        test = ui.section_menu(monograph)
        generate_steps(monograph, test)


if __name__ == "__main__":
    # sys.exit(main())
    pdf = (
        settings.root_dir
        / "data/input/USP-NF Amoxicillin and Clavulanate Potassium Tablets.pdf"
    )
    print_steps(upar.break_into_sections(upar.pdf_to_text(pdf)))
