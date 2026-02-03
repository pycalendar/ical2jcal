import json

from icalendar import Calendar
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

