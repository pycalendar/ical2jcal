from icalendar import Calendar
import pytest
from typer.testing import CliRunner

from ical2jcal.cli import jcal2ical


def test_jcal2ical_single_calendar_file(calendars, output_file) -> None:
    """Convert ics to jcal using file arguments."""
    calendar = calendars["rfc_7265_appendix_example_1_jcal.jcal"]
    runner = CliRunner()
    result = runner.invoke(jcal2ical, [str(calendar.path), str(output_file)])
    assert result.exit_code == 0, result.output

    ics = output_file.read_text()
    assert Calendar.from_ical(ics) == calendar.calendar


@pytest.mark.parametrize("content", ["[]", "Not a calendar", ""])
def test_error_input_is_not_a_calendar(content, tmp_path):
    """The calendar is not valid."""
    invalid_calendar = tmp_path / "invalid.jcal"
    invalid_calendar.write_text(content)
    runner = CliRunner()
    result = runner.invoke(jcal2ical, [str(invalid_calendar), "-"])
    assert result.exit_code == 1, result.output
    assert "The input file is not a valid RFC 7265 jCalendar." in result.output


def test_error_jcal_information_problem_given(tmp_path):
    """The calendar is not valid."""
    invalid_calendar = tmp_path / "invalid.jcal"
    invalid_calendar.write_text("[]")
    runner = CliRunner()
    result = runner.invoke(jcal2ical, [str(invalid_calendar), "-"])
    assert result.exit_code == 1, result.output
    assert "in Calendar: A component must be a list with 3 items. Got value: []" in result.stderr
