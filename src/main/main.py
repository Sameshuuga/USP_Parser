#!/usr/bin/env /home/sameshuuga/Projects/USP_Parser/.venv/bin/python3

import sys, logging
from pathlib import Path

import main.settings as settings
import main.ui as ui
import main.usp_parser as upar
import main.llm_handler as llm
import main.excel_writer as ew

logger = logging.getLogger(__name__)
logging.basicConfig(filename=settings.log_file, level=logging.INFO)


def print_steps(steps: dict):
    for key, step in steps.items():
        print(f"\n{key}:\n{step}")


def transmute(flat_list: list) -> list:
    """Convert a flat list into a column: [1,2,3] -> [[1],[2],[3]]"""
    return [[v] for v in flat_list]


def make_step_list(steps: dict) -> list:
    step_list = []
    for i, (key, step) in enumerate(steps.items()):
        if i > 0:
            step_list.append("")
        step_list.append(key)
        step_list.extend(step.splitlines())
    return transmute(step_list)


def generate_steps(monograph: dict, test: str) -> dict:
    raw_llm_output = llm.BaseLLM().call_llm(monograph.get(test))
    instructions = raw_llm_output.solutions_dict
    print_steps(instructions)
    return instructions


def run_pipeline(pdf):
    monograph = upar.usp_parser(Path(pdf))
    steps = generate_steps(monograph, "ASSAY")
    output_path = settings.default_output_dir / "result.xlsx"
    ew.copy_templet(settings.templet_file, output_path)
    result = ew.inject_xlsx(output_path, make_step_list(steps))
    return result


def main():
    while True:
        args = ui.build_parser().parse_args()
        monograph: dict = upar.usp_parser(ui.file_menu(args.input))
        test = ui.section_menu(monograph)
        generate_steps(monograph, test)


if __name__ == "__main__":
    sys.exit(main())
