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

## Code Style Checking

[PEP 8](https://peps.python.org/pep-0008/) is the universally accepted style guide for Python
code. PEP 8 code compliance is verified using [Ruff][Ruff]. Ruff is configured in the
`[tool.ruff]` section of `pyproject.toml`.

[Ruff]: https://github.com/astral-sh/ruff

Some code style settings are included in `.editorconfig` and will be configured
automatically in editors such as PyCharm.

To lint code, run:

```shell
uv run nox -s lint
```

To automatically fix fixable lint errors, run:

```shell
uv run nox -s lint_fix
```

## Automated Code Formatting

[Ruff][Ruff] is used to automatically format code and group and sort imports.

To automatically format code, run:

```shell
uv run nox -s fmt
```

## Generating a User Guide

[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) is a powerful static site
generator that combines easy-to-write Markdown, with a number of Markdown extensions that increase
the power of Markdown. This makes it a great fit for user guides and other technical documentation.

The example MkDocs project included in this project is configured to allow the built documentation
to be hosted at any URL or viewed offline from the file system.

To build the user guide, run,

```shell
uv run nox -s docs
```

and open `docs/user_guide/site/index.html` using a web browser.

To build the user guide, additionally validating external URLs, run:

```shell
uv run nox -s docs_check_urls
```

To build the user guide in a format suitable for viewing directly from the file system, run:

```shell
uv run nox -s docs_offline
```

To build and serve the user guide with automatic rebuilding as you change the contents,
run:

```shell
uv run nox -s docs_serve
```

and open <http://127.0.0.1:8000> in a browser.

More
----

Have a look at `/USAGE.md` and copy over what what really use into this document.

Maintenance
-----------

Releasing a new version.

1. Update `changelog.md`
2. Create a tag and push it.

    ```sh
    git tag v1.0.7
    git push origin v1.0.7
    ```
