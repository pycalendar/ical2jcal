icon: material/tools
---

Development Guide
=================

This document provides a guide to developeing the `ical2jcal` project.

Setup `git`
-----------

1. Install [git](https://git-scm.com/).
2. Clone the repository:

    ```bash
    git clone https://github.com/pycalendar/ical2jcal.git
    cd ical2jcal
    ```

Setup `uv`
----------

Install [uv](https://docs.astral.sh/uv/getting-started/installation).
To install uv, run:

=== "macOS and Linux"

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "Windows"

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

Then install the `ical2jcal` package and its dependencies:

```bash
uv sync
```
