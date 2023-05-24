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

from mh2_gxttool.gxtfile import GXTFile


# Common options
force_option = click.option(
    "-f",
    "--force",
    help="force overwrite existing file",
    is_flag=True,
)
platform_opt = click.option(
    "-p",
    "--platform",
    default="PSP",
    help="GXT game platform (default: PSP)",
    type=click.Choice(["PC", "PSP", "PS2"], case_sensitive=False),
)
src_argument = click.argument(
    "src_file", type=click.Path(exists=True, dir_okay=False, readable=True)
)


# Start of CLI
@click.group(context_settings={"help_option_names": ["-h", "--help"]})
def cli():
    """A CLI tool to pack/unpack GXT files from Manhunt 2."""
    pass


# Pack command
@cli.command(help="Pack a TOML document to a GXT file")
@force_option
@click.option(
    "-o",
    "--output",
    "dst_file",
    help="output file name (default: change src_file extension to .gxt)",
    type=click.Path(dir_okay=False),
)
@platform_opt
@src_argument
def pack(platform, force, dst_file, src_file):
    src_file = pathlib.Path(src_file)

    if dst_file is None:
        dst_file = src_file.with_suffix(".gxt")
    else:
        dst_file = pathlib.Path(dst_file)

    if dst_file.exists() and not force:
        raise click.ClickException(
            f"{dst_file} already exist. Use -f to overwrite"
        )

    GXTFile.pack(src_file, dst_file, platform)


# Unpack command
@cli.command(help="Unpack a GXT file to a TOML document")
@force_option
@click.option(
    "-o",
    "--output",
    "dst_file",
    help="output file name (default: change src_file extension to .toml)",
    type=click.Path(dir_okay=False),
)
@platform_opt
@src_argument
def unpack(platform, force, dst_file, src_file):
    src_file = pathlib.Path(src_file)

    if dst_file is None:
        dst_file = src_file.with_suffix(".toml")
    else:
        dst_file = pathlib.Path(dst_file)

    if dst_file.exists() and not force:
        raise click.ClickException(
            f"{dst_file} already exists. Use -f to overwrite"
        )

    GXTFile.unpack(src_file, dst_file, platform)


if __name__ == "__main__":
    cli()
