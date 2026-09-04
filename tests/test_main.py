import pytest
from pathlib import Path

from main import settings


def test_root():
    assert settings.root_dir == Path(__file__).resolve().parent.parent
