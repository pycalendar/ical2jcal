---
icon: material/book-open-blank-variant-outline
---

Advanced Usage
==============

This document provides a guide to advanced usage of the `ical2jcal` project.

Convert an online calendar to JSON
----------------------------------

Calendar services line Nextcloud, Google Calendar and Microsoft Outlook can provide an link to a `.ics` file for your calendar.

In the example below, we convert the example calender from our project website to JSON.

=== "curl[^1]"

    ```bash
    curl -sL https://github.com/niccokunzmann/ical2jcal/raw/refs/heads/main/example.ics | ical2jcal --pretty
    ```

    ```json
    [
      "vcalendar",
      [
        [
          "version",
          {},
          "text",
          "2.0"
        ],
        [
          "prodid",
          {},
          "text",
          "-//niccokunzmann//ical2jcal//EN"
        ]
      ],
      []
    ]
    ```

=== "wget[^2]"

    ```bash
    $ wget -qO- https://github.com/niccokunzmann/ical2jcal/raw/refs/heads/main/example.ics | ical2jcal --pretty
    ```

    ```json
    [
      "vcalendar",
      [
        [
          "version",
          {},
          "text",
          "2.0"
        ],
        [
          "prodid",
          {},
          "text",
          "-//niccokunzmann//ical2jcal//EN"
        ]
      ],
      []
    ]
    ```

Filter the JSON calendar with `jq`
----------------------------------

Once converted, you can filter the JSON calendar using `jq`[^3].

In this example, we only print the `prodid` field of the calendar.

```bash
$ ical2jcal example.ics | jq '.[1][] | select(.[0] == "prodid") | .[3]'
```

Output:

```json
"-//niccokunzmann//ical2jcal//EN"
```

Here, we use `jq` to get all event summaries.

```bash
$ ical2jcal other-example.ics | jq '.[2][] | select(.[0] == "vevent") | .[1][] | select(.[0] == "summary") | .[3]'
```

Output:

```json
"Planning meeting"
```

Get today's events as JSON
--------------------------

Given you have a calendar file as a valid jCalendar, you can use different tools to filter the calendar by date and time and use the JSON output.

=== "ics-query[^4]"

    ```bash
    jcal2ical input.jcal | ics-query at --as-calendar `` - - | ical2jcal --pretty
    ```

    Output:

    ```json
    [
        "vcalendar",
        [
            ...
        ],
        [
            ...
        ]
    ]
    ```

=== "icalendar-events-cli[^5]"

    ```bash
    $ jcal2ical my-calendar.jcal my-calendar.ics
    $ icalendar-events-cli \
        --calendar.url file://`pwd`/my-calendar.ics \
        --filter.start-date `date +%Y-%m-%d`T00:00:00 \
        --filter.end-date `date +%Y-%m-%d`T23:59:59
    ```

    Output:

    ```text
    Start Date:         2026-02-03T21:10:54+00:00
    End Date:           2026-02-03T23:59:59+00:00
    Number of Events:   0
    ```

[^1]: [curl website](https://curl.se/)
[^2]: [wget website](https://www.gnu.org/software/wget/)
[^3]: [jq website](https://jqlang.org)
[^4]: [ics-query website](https://pypi.org/project/ics-query/)
[^5]: [icalendar-events-cli website](https://github.com/waldbaer/icalendar-events-cli)
