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
    ics_path: Annotated[
        typer.FileText, typer.Argument(exists=True, help="Input iCalendar file or - for stdin")
    ] = "-",
    jcal_path: Annotated[
        typer.FileTextWrite, typer.Argument(help="Output jCalendar file or - for stdout")
    ] = "-",
    pretty: Annotated[bool, typer.Option("--pretty", "-p", help="Pretty print json")] = False,
    version: Annotated[
        bool | None,
        typer.Option("--version", callback=version_callback, help="Print version and exit"),
    ] = None,
) -> None:
    """Convert an ics file [RFC 5545] to jCalendar [RFC 7265].

    If the file contains multiple calendars, only the first one is converted.

    | Error Code | Description                                      |
    | ---------- | -----------                                      |
    |          1 | The input file is not a valid RFC 5545 iCalendar |
    |          2 | The input file does not exist                    |

    Examples
    --------

    Convert an ics file to a jcal file:

        $ ical2jcal example.ics example.jcal

    Convert stdin to stdout with an invalid calendar:

        $ echo ... | ical2jcal - -
        The input file is not a valid RFC 5545 iCalendar.

    Print the jcal version of an ics file:

        $ ical2jcal example.ics --pretty
        [
            ...
        ]

    [RFC 5545]: https://datatracker.ietf.org/doc/html/rfc5545
    [RFC 7265]: https://datatracker.ietf.org/doc/html/rfc7265
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
    jcal_path: Annotated[
        typer.FileText, typer.Argument(exists=True, help="Input jCalendar file or - for stdin")
    ] = "-",
    ics_path: Annotated[
        typer.FileBinaryWrite,
        typer.Argument(help="Output iCalendar file or - for stdout (default)"),
    ] = "-",
    version: Annotated[
        bool | None,
        typer.Option("--version", callback=version_callback, help="Print version and exit"),
    ] = None,
) -> None:
    """Convert a jCalendar file [RFC 7265] to ics [RFC 5545].

    | Error Code | Description                                      |
    | ---------- | -----------                                      |
    |          1 | The input file is not a valid RFC 7265 jCalendar |
    |          2 | The input file does not exist                    |

    Examples
    --------

    Convert a jcal file to an ics file:

        $ jcal2ical example.jcal example.ics

    Convert stdin to stdout with an invalid calendar:

        $ echo ... | jcal2ical
        The input file is not a valid RFC 7265 jCalendar.

    Print the ics version of an jcal file:

        $ jcal2ical example.jcal
        BEGIN:VCALENDAR
        VERSION:2.0
        PRODID:-//niccokunzmann//ical2jcal//EN
        END:VCALENDAR

    [RFC 5545]: https://datatracker.ietf.org/doc/html/rfc5545
    [RFC 7265]: https://datatracker.ietf.org/doc/html/rfc7265
    """
    try:
        calendar = Calendar.from_jcal(jcal_path.read())
    except json.JSONDecodeError as e:
        raise typer.Exit("The input file is not a valid RFC 7265 jCalendar.") from e
    except JCalParsingError as e:
        err_console.print(e)
        raise typer.Exit("The input file is not a valid RFC 7265 jCalendar.") from e
    ics_path.write(calendar.to_ical())
