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
import json

import pytest
from typer.testing import CliRunner

from ical2jcal.cli import ical2jcal


def test_ical2jcal_single_calendar_file(calendars, output_file) -> None:
    """Convert ics to jcal using file arguments."""
    calendar = calendars["example.ics"]
    runner = CliRunner()
    result = runner.invoke(ical2jcal, [str(calendar.path), str(output_file)])
    assert result.exit_code == 0, result.output

    jcal = json.loads(output_file.read_text())
    expected = calendar.calendar.to_jcal()
    assert jcal == expected


def test_ical2jcal_single_calendar_stdin(calendars, output_file) -> None:
    """Convert ics to jcal using stdin."""
    calendar = calendars["example.ics"]
    runner = CliRunner()
    result = runner.invoke(ical2jcal, ["-", str(output_file)], input=calendar.path.read_text())
    assert result.exit_code == 0, result.output

    jcal = json.loads(output_file.read_text())
    expected = calendar.calendar.to_jcal()
    assert jcal == expected


def test_ical2jcal_single_calendar_stout(calendars) -> None:
    """Convert ics to jcal using stdin."""
    calendar = calendars["example.ics"]
    runner = CliRunner()
    result = runner.invoke(ical2jcal, [str(calendar.path), "-"])
    assert result.exit_code == 0, result.output

    jcal = json.loads(result.stdout)
    expected = calendar.calendar.to_jcal()
    assert jcal == expected


def test_pretty_option(calendars):
    """Test that we can print pretty json."""
    calendar = calendars["example.ics"]
    runner = CliRunner()
    result = runner.invoke(ical2jcal, [str(calendar.path), "-", "--pretty"])
    assert result.exit_code == 0, result.output

    jcal = json.loads(result.stdout)
    expected = calendar.calendar.to_jcal()
    assert jcal == expected
    assert result.output.startswith("[\n  ")


@pytest.mark.parametrize("content", ["", "Not a calendar"])
def test_error_input_is_not_a_calendar(tmp_path, content):
    """The input is not a calendar."""
    invalid_calendar = tmp_path / "invalid.ics"
    invalid_calendar.write_text(content)
    runner = CliRunner()
    result = runner.invoke(ical2jcal, [str(invalid_calendar), "-"])
    assert result.exit_code == 1, result.output
    assert "The input file is not a valid RFC 5545 iCalendar." in result.output


def test_error_multiple_calendars(calendars):
    """Multiple calendars exist."""
    calendar = calendars["stream.ics"]
    runner = CliRunner()
    result = runner.invoke(ical2jcal, [str(calendar.path), "-"])
    assert result.exit_code == 0, result.output

    jcal = json.loads(result.stdout)
    expected = calendar.calendar.to_jcal()
    assert jcal == expected


def test_default_is_stdin_stdout(calendars):
    calendar = calendars["example.ics"]
    runner = CliRunner()
    result = runner.invoke(ical2jcal, [], input=calendar.path.read_text())
    assert result.exit_code == 0, result.output

    jcal = json.loads(result.stdout)
    expected = calendar.calendar.to_jcal()
    assert jcal == expected
