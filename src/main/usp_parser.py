from pypdf import PdfReader
import re


## ------------------------ pdf_to_text -------------------------------- ##
def pdf_to_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text


##-----------------------------------------------------------------------##
## ------------------------ break_into_sections ------------------------ ##
def break_into_sections(text: str) -> dict[str, list[str]]:
    headers = [
        "DEFINITION",
        "IDENTIFICATION",
        "ASSAY",
        "IMPURITIES",
        "PERFORMANCE TESTS",
        "SPECIFIC TESTS",
        "ADDITIONAL REQUIREMENTS",
    ]
    sections: list[list[str]] = []
    chunk: list[str] = []
    lines = text.splitlines()
    for line in lines:
        if line in headers:
            sections.append(chunk)
            chunk = []
        chunk.append(line)
    if chunk:
        sections.append(chunk)
    if len(sections) <= 1:
        raise ValueError("No USP sections detected.")

    result: dict[str, list[str]] = {}
    for section in sections:
        if not section:
            continue
        key, rest = section[0], section[1:]
        result[key] = rest
    return result


##-----------------------------------------------------------------------##
## ------------------------ parse Assay -------------------------------- ##
def extract_assay_preps(section: list[str]) -> list[str]:

    return preps


##-----------------------------------------------------------------------##


def extract_preps(sections: list[list[str]]) -> dict:
    pass


def usp_parser(monograph_paths: list[str]):
    processed_monographs = []

    for monograph in monograph_paths:
        processed_monograph = pdf_to_text(monograph)
        processed_monographs.append(processed_monograph)

    return processed_monographs
