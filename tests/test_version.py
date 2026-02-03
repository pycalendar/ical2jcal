import pytest
from typer.testing import CliRunner

from ical2jcal import __version__, cli


@pytest.mark.parametrize("endpoint", [cli.ical2jcal, cli.jcal2ical])
def test_version(endpoint):
    runner = CliRunner()
    result = runner.invoke(endpoint, ["--version"])
    assert result.exit_code == 0, result.output
    assert "ical2jcal" in result.stdout
    assert __version__ in result.stdout
