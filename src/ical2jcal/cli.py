#!/usr/bin/env python3

from typing import Annotated

from icalendar import Calendar
import typer
from rich.console import Console

ical2jcal = typer.Typer(add_completion=False)


@ical2jcal.command()
def convert_to_jcal(
        ics_path:Annotated[typer.FileText, typer.Argument(exists=True)],
        jcal_path: Annotated[typer.FileTextWrite, typer.Argument()],
        pretty: Annotated[bool, typer.Option("--pretty", "-p", help="Pretty print json")] = False
    ) -> None:
    """Convert an ics file to a jcal file."""
    calendar = Calendar.from_ical(ics_path.read())
    if pretty:
        console = Console(file=jcal_path)
        console.print_json(calendar.to_json())
    else:
        jcal_path.write(calendar.to_json())

