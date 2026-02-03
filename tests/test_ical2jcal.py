import json

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
