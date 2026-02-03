---
icon: material/calendar-expand-horizontal
status: new
---

# `ical2jcal` User Guide

This document enables you to convert iCalendar to jCalendar and vice versa, using the commands `ical2jcal` and `jcal2ical` on the command line.

## Installation

`ical2jcal` is available on [PyPI](https://pypi.org/project/ical2jcal/).
It is compatible with [Python 3.10](https://www.python.org/) and later.

You have several options to install this tool.

=== "pip"

    `pip` comes with Python. To install this tool, run:

    ```bash
    python -m pip install ical2jcal
    ```

=== "pipx"

    After you have installed [pipx](https://pipx.pypa.io/stable/installation/), run:

    ```bash
    pipx install ical2jcal
    ```

=== "uv"

    The [development guide](development.md) provides instructions on how to install `ical2jcal` using `uv`.

## Convert `.ics` to JSON

iCalendar files have the `.ics` extension.
You can convert them to an [RFC 7265] compatible JSON using the `ical2jcal` command.
We recommend using the `.jcal` extension for compatible JSON files.

The example below converts the `example.ics` file to `example.jcal`:

```bash
ical2jcal example.ics example.jcal
```

For more options, view the [command line reference](ical2jcal.md).

## Convert JSON to `.ics`

[RFC 7265] compatible JSON files can be converted with the `jcal2ical` command.

The example below converts the `example.jcal` file to `example.ics`:

```bash
jcal2ical example.jcal example.ics
```

For more options, view the [command line reference](jcal2ical.md).


[RFC 7265]: https://tools.ietf.org/html/rfc7265
