# Manhunt 2 GXT Tool

This is a Python CLI program that can pack and unpack GXT files from Manhunt 2. Currently, it supports the PSP, PS2 and PC versions.

The tool is based on the [GXT](https://github.com/Sor3nt/manhunt-toolkit/blob/5c3b56d237b0ead7f1ce633a5c22cf6996f77c57/Application/App/Service/Archive/Gxt.php) implementation from [Manhunt Toolkit](https://github.com/Sor3nt/manhunt-toolkit) by Sor3nt.

## Installation

You can install `mh2-gxttool` using pip:

```bash
# Clone this repository
git clone https://github.com/santiago046/mh2-gxttool
# Change to the project directory
cd mh2-gxttool
# Install using pip
pip install .
```

## Usage

```bash
Usage: mh2-gxttool [OPTIONS] COMMAND [ARGS]...

A CLI tool to pack/unpack GXT files from Manhunt 2.

Options:
  -h, --help  Show this message and exit.

Commands:
  pack    Pack a TOML document to a GXT file
  unpack  Unpack a GXT file to a TOML document
```

`mh2-gxttool` has two commands: `pack` and `unpack`.

### Pack

```bash
Usage: mh2-gxttool pack [OPTIONS] SRC_FILE

  Pack a TOML document to a GXT file

Options:
  -f, --force                  force overwrite existing file
  -o, --output FILE            output file name (default: change src_file
                               extension to .gxt)
  -p, --platform [PC|PSP|PS2]  GXT game platform (default: PSP)
  -h, --help                   Show this message and exit.
```

The `pack` command converts a TOML document (`SRC_FILE`) into a GXT file. The TOML document must follow the syntax described below.

### Unpack

```bash
Usage: mh2-gxttool unpack [OPTIONS] SRC_FILE

  Unpack a GXT file to a TOML document

Options:
  -f, --force                  force overwrite existing file
  -o, --output FILE            output file name (default: change src_file
                               extension to .toml)
  -p, --platform [PC|PSP|PS2]  GXT game platform (default: PSP)
  -h, --help                   Show this message and exit.
```

The `unpack` command extracts the text data from a GXT file (`SRC_FILE`) and saves it as a TOML document. The TOML document can be edited and packed back into a GXT file.

### TOML Syntax

The tool uses the [TOML](https://toml.io/en/) format for the input of the `pack` command and the output of `unpack`. This is an example of how it looks:

```toml
title = "Decompiled FILE.GXT" # Optional, always ignored in packing mode

# Key table format:
[KEYNAME]                     # Key name
console = ""                  # Optional, can be anything after '='
duration = 192                # Integer, duration
string = "Hello, world!"      # Key string
```

- `KEYNAME`: Maximum of 8 characters for PSP/PS2, 12 for PC.
- `console`: Tells the packer to encode the string in UTF-16 charset, useful for strings handled by the console and not the game.
- `duration`: Duration of the key in milliseconds.
- `string`: The key string, always inside double quotes. If the string contains a double quote, escape it using `\"`.

**Note:** mh2-gxttool uses UTF-8 for the TOML files. You can check the available characters for Manhunt 2 [here](https://github.com/santiago046/manhunt2-translation-resources/blob/main/font-and-charset-info.md#manhunt-2-charset-en-fr-ge-it-sp) — please, ignore the unicode column.

## Examples

Unpack `GAME.GXT` from PSP:

```bash
mh2-gxttool unpack -p PSP path_to/GAME.GXT
```

Unpack `GAME.GXT` from PS2 to `~/resources/` and force overwriting:

```bash
mh2-gxttool unpack -f -p PS2 -o ~/resources/GAME.toml path_to/GAME.GXT
```

Pack it to PC version:

```bash
mh2-gxttool pack -p PC ~/resources/GAME.toml
```

## To do
- Add support for the Wii version of Manhunt 2
- Maybe add support for Manhunt (2003)

Happy modding/translating!
