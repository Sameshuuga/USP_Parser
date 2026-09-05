import pytest

from main import usp_parser as upar


class TestBreakIntoSections:
    def test_single_section(self):
        text = "DEFINITION\nSome definition text.\nMore text."
        result = upar.break_into_sections(text)
        assert result == {"DEFINITION": "Some definition text.\nMore text."}

    def test_multiple_sections(self):
        text = (
            "DEFINITION\n"
            "Def line 1.\n"
            "ASSAY\n"
            "Assay line 1.\n"
            "Assay line 2.\n"
            "IMPURITIES\n"
            "Impurities line 1."
        )
        result = upar.break_into_sections(text)
        assert result == {
            "DEFINITION": "Def line 1.",
            "ASSAY": "Assay line 1.\nAssay line 2.",
            "IMPURITIES": "Impurities line 1.",
        }

    def test_all_known_headers(self):
        headers = [
            "DEFINITION",
            "IDENTIFICATION",
            "ASSAY",
            "IMPURITIES",
            "PERFORMANCE TESTS",
            "SPECIFIC TESTS",
            "ADDITIONAL REQUIREMENTS",
        ]
        text = "\n".join(f"{h}\nbody for {h}" for h in headers)
        result = upar.break_into_sections(text)
        assert set(result.keys()) == set(headers)
        for h in headers:
            assert result[h] == f"body for {h}"

    def test_section_with_no_body_lines(self):
        text = "DEFINITION\nASSAY\nAssay text."
        result = upar.break_into_sections(text)
        assert result == {
            "DEFINITION": "",
            "ASSAY": "Assay text.",
        }

    def test_no_headers_raises(self):
        text = "just some text\nwith no headers at all"
        with pytest.raises(ValueError, match="No USP sections detected."):
            upar.break_into_sections(text)

    def test_empty_string_raises(self):
        with pytest.raises(ValueError, match="No USP sections detected."):
            upar.break_into_sections("")

    def test_repeated_header_overwrites_earlier_entry(self):
        # Current implementation builds a dict, so a header appearing twice
        # means the second occurrence's body silently overwrites the first
        # in the result. This test documents that behavior.
        text = "ASSAY\nfirst body\nASSAY\nsecond body"
        result = upar.break_into_sections(text)
        assert result == {"ASSAY": "second body"}
