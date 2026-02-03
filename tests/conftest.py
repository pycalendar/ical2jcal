from pathlib import Path
from typing import NamedTuple

from icalendar import Calendar
import pytest

HERE = Path(__file__).parent
CALENDARS = HERE / "calendars"


class TestFile(NamedTuple):
    path: Path
    calendar: Calendar


@pytest.fixture
def calendars() -> dict[str, TestFile]:
    result = {}
    for path in CALENDARS.iterdir():
        if path.name.endswith(".ics"):
            calendar = Calendar.from_ical(path.read_text(), multiple=True)[0]
        else:
            calendar = Calendar.from_jcal(path.read_text())
        result[path.name] = TestFile(path, calendar)
    return result


@pytest.fixture
def output_file(tmp_path: Path) -> Path:
    return tmp_path / "output"
