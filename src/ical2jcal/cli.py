#!/usr/bin/env python3

import json
from typing import Annotated

from icalendar import Calendar, JCalParsingError
from rich.console import Console
import typer

console = Console()
err_console = Console(stderr=True)
ical2jcal = typer.Typer(add_completion=False)


def version_callback(value: bool):
    if value:
        import ical2jcal

        console.print(f"{ical2jcal.__name__}: {ical2jcal.__version__}")
        raise typer.Exit()


@ical2jcal.command()
def convert_to_jcal(
    ics_path: Annotated[typer.FileText, typer.Argument(exists=True)],
    jcal_path: Annotated[typer.FileTextWrite, typer.Argument()],
    pretty: Annotated[bool, typer.Option("--pretty", "-p", help="Pretty print json")] = False,
    version: Annotated[
        bool | None, typer.Option("--version", callback=version_callback, help="Print version")
    ] = None,
) -> None:
    """Convert an ics file to a jcal file.

    Convert a file from the RFC 5545 iCalendar format to the RFC 7265 jCalendar format.

    The file is expected to contain a single calendar.
    """
    try:
        calendars = Calendar.from_ical(ics_path.read(), multiple=True)
    except ValueError as e:
        raise typer.Exit("The input file is not a valid RFC 5545 iCalendar.") from e
    if len(calendars) == 0:
        raise typer.Exit("The input file is not a valid RFC 5545 iCalendar.")
    calendar = calendars[0]
    if pretty:
        console = Console(file=jcal_path)
        console.print_json(calendar.to_json())
    else:
        jcal_path.write(calendar.to_json())


jcal2ical = typer.Typer(add_completion=False)


@jcal2ical.command()
def convert_to_ical(
    jcal_path: Annotated[typer.FileText, typer.Argument(exists=True)],
    ics_path: Annotated[typer.FileBinaryWrite, typer.Argument()],
    version: Annotated[
        bool | None, typer.Option("--version", callback=version_callback, help="Print version")
    ] = None,
) -> None:
    """Convert an jcal file to an ics file.

    Convert a file from the RFC 7265 jCalendar format to the RFC 5545 iCalendar format.
    """
    try:
        calendar = Calendar.from_jcal(jcal_path.read())
    except json.JSONDecodeError as e:
        raise typer.Exit("The input file is not a valid RFC 7265 jCalendar.") from e
    except JCalParsingError as e:
        err_console.print(e)
        raise typer.Exit("The input file is not a valid RFC 7265 jCalendar.") from e
    ics_path.write(calendar.to_ical())
