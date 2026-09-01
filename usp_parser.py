from pypdf import PdfReader
import re


def pdf_to_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text


def break_into_sections(text: str) -> list[str]:
    # TODO: add error catching for if the text does not contain any of the headers.

    headers = [
        "DEFINITION",
        "IDENTIFICATION",
        "ASSAY",
        "IMPURITIES",
        "PERFORMANCE TESTS",
        "SPECIFIC TESTS",
        "ADDITIONAL REQUIREMENTS",
    ]
    sections, chunk = [], []
    lines = text.splitlines()
    for line in lines:
        if line in headers:
            sections.append(chunk)
            chunk = []
        chunk.append(line)
    if chunk:
        sections.append(chunk)
    return sections


def print_to_file(thing_to_print: str, output_path: str):
    with open(output_path, "w") as f:
        f.write(thing_to_print)
    print(f"file wrote to {output_path}")


def print_loop(thing: list):
    for x in thing:
        print(x)


if __name__ == "__main__":
    document = "/home/sameshuuga/Documents/USP-NF Amoxicillin and Clavulanate Potassium Tablets.pdf"
    output = "/home/sameshuuga/temp/usp-output.text"
    text = pdf_to_text(document)
    sections = break_into_sections(text)
    print_loop(sections)
    print_to_file(text, output)
