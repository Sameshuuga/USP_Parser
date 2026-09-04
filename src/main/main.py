import os
from pathlib import Path

import settings
import usp_parser as upar

root_dir = settings.root_dir
data_dir = root_dir / "data/"


def write_sections(sections: dict[str, list[str]], target_dir: Path):
    """Write each section to its own file in target_dir."""
    os.makedirs(target_dir, exist_ok=True)
    for section_name, lines in sections.items():
        file_path = target_dir / f"{section_name}.txt"
        with open(file_path, "w") as f:
            f.write(f"{section_name}\n")
            for line in lines:
                f.write(f"{line}\n")


def print_to_file(thing_to_print: str, output_path: Path):
    with open(output_path, "w") as f:
        f.write(thing_to_print)
    print(f"file wrote to {output_path}")


def print_sections(sections: dict[str, list[str]]) -> None:
    for header, lines in sections.items():
        print(header)
        for line in lines:
            print(line)
        print()


if __name__ == "__main__":
    monograph = "USP-NF Ketamine Hydrochloride"
    document = data_dir / f"input/pdfs/{monograph}.pdf"
    output = data_dir / f"output/{monograph}"
    text = upar.pdf_to_text(document)
    sections = upar.break_into_sections(text)
    print_sections(sections)
    # print_to_file(text, output)
    write_sections(sections, output)
