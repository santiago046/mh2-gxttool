# mh2-gxttool - A tool to unpack/pack GXT files from Manhunt 2.
# Copyright (C) 2023 santiago046

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import click
import pathlib

from mh2_gxttool import GXTFile


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    """A CLI tool to pack/unpack GXT files from Manhunt 2."""
    pass


@cli.command(help="Pack a TOML document to a GXT file")
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="force destination file overwriting (default: False)",
)
@click.option(
    "-o",
    "--output",
    "dst_file",
    type=click.Path(dir_okay=False),
    help="output file name (default: change src_file extension to .toml)",
)
@click.argument(
    "src_file", type=click.Path(exists=True, dir_okay=False, readable=True)
)
def pack(force, dst_file, src_file):
    src_file = pathlib.Path(src_file)

    if dst_file == None:
        dst_file = src_file.with_suffix(".gxt")
    else:
        dst_file = pathlib.Path(dst_file)

    if dst_file.exists() and not force:
        raise click.ClickException(
            f"{dst_file} already exist. Use -f to overwrite"
        )

    GXTFile.pack(src_file, dst_file)


@cli.command(help="Unpack a GXT file to a TOML document")
@click.option(
    "-f",
    "--force",
    is_flag=True,
    help="force destination file overwriting (default: False)",
)
@click.option(
    "-o",
    "--output",
    "dst_file",
    type=click.Path(dir_okay=False),
    help="output file name (default: change src_file extension to .gxt)",
)
@click.argument(
    "src_file", type=click.Path(exists=True, dir_okay=False, readable=True)
)
def unpack(force, dst_file, src_file):
    src_file = pathlib.Path(src_file)

    if dst_file == None:
        dst_file = src_file.with_suffix(".toml")
    else:
        dst_file = pathlib.Path(dst_file)

    if dst_file.exists() and not force:
        raise click.ClickException(
            f"{dst_file} already exists. Use -f to overwrite"
        )

    GXTFile.unpack(src_file, dst_file)


if __name__ == "__main__":
    cli()
