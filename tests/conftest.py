# ical2jcal
# Copyright (C) 2026  Nicco Kunzmann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
