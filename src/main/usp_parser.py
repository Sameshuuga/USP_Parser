from pypdf import PdfReader
from pathlib import Path
import re, logging

logger = logging.getLogger(__name__)

_ORPHAN_LINE = re.compile(r"^[A-Za-z0-9]{1,2}(?:\s+[A-Za-z0-9]{1,2})*$")


## ------------------------ pdf_to_text -------------------------------- ##
def is_noise_line(line: str) -> bool:
    """True if a line is nothing but short (1-2 char) whitespace-separated
    tokens — the pattern typical of PDF-extraction artifacts."""
    return bool(_ORPHAN_LINE.match(line.strip()))


def clean(text: str) -> str:
    """Strip lines that look like PDF-extraction noise, keep the rest."""
    kept = [
        line for line in text.splitlines() if line.strip() and not is_noise_line(line)
    ]
    return "\n".join(kept)


def pdf_to_text(pdf: Path) -> str:
    reader = PdfReader(pdf)
    text = ""
    for page in reader.pages:
        extracted = clean(page.extract_text())
        if extracted:
            text += extracted
    return text


##-----------------------------------------------------------------------##
## ------------------------ break_into_sections ------------------------ ##
def break_into_sections(text: str) -> dict[str, str]:

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
        key, rest = section[0], "\n".join(section[1:])
        result[key] = rest
    return result


##-----------------------------------------------------------------------##
def usp_parser(monograph: Path) -> dict:
    logger.info("Parsing %s.", monograph.name)
    text = clean(pdf_to_text(monograph))
    result = break_into_sections(text)
    logger.info("Parsed %s.", monograph.name)
    return result
