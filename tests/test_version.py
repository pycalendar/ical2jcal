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
