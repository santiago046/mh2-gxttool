# Manhunt 2 GXT Tool

The Manhunt 2 GXT Tool is a Python CLI program designed to pack and unpack GXT files from Manhunt 2. It currently supports the PSP, PS2, and PC versions of the game.

The tool is based on the GXT implementation from [Manhunt Toolkit](https://github.com/Sor3nt/manhunt-toolkit) by Sor3nt.

## Installation

To install the `mh2-gxttool`, you can use pip. Follow these steps:

1. Clone this repository:

   ```bash
   git clone https://github.com/santiago046/mh2-gxttool
   ```

2. Change to the project directory:

   ```bash
   cd mh2-gxttool
   ```

3. Install using pip:

   ```bash
   pip install .
   ```

## Usage

The `mh2-gxttool` has two main commands: `pack` and `unpack`. Here is an overview of how to use them:

### Pack Command

The `pack` command converts a TOML document (`SRC_FILE`) into a GXT file. The TOML document must follow a specific syntax. Here is the usage and available options:

```bash
Usage: mh2-gxttool pack [OPTIONS] SRC_FILE

Pack a TOML document to a GXT file

Options:
  -c, --charset-file FILE      Specify a TOML file with the charset to use.
  -f, --force                  Overwrite existing files.
  -o, --output FILE            Specify the output file name. (default: change
                               src_file extension to .gxt)
  -p, --platform [PC|PSP|PS2]  Specify the GXT game platform. (default: PSP)
  -h, --help                   Show this message and exit.
```

### Unpack Command

The `unpack` command extracts the text data from a GXT file (`SRC_FILE`) and saves it as a TOML document. The TOML document can be edited and packed back into a GXT file. Here is the usage and available options:

```bash
Usage: mh2-gxttool unpack [OPTIONS] SRC_FILE

Unpack a GXT file to a TOML document

Options:
  -c, --charset-file FILE      Specify a TOML file with the charset to use.
  -f, --force                  Overwrite existing files.
  -o, --output FILE            Specify the output file name. (default: change
                               src_file extension to .toml)
  -p, --platform [PC|PSP|PS2]  Specify the GXT game platform. (default: PSP)
  -h, --help                   Show this message and exit.
```

### TOML Syntax

The tool uses the TOML format for the input of the `pack` command and the output of the `unpack` command. Here is an example of how the TOML document should look:

```toml
title = "Decompiled FILE.GXT" # Optional, always ignored in packing mode

# Key table format:
[KEYNAME]                     # Key name
console = true                # Optional, true or false
duration = 192                # Integer, duration
string = "Hello, world!"      # Key string
```

In the TOML document:
- `KEYNAME` can have a maximum of 8 characters for PSP/PS2 or 12 characters for PC.
- `console` is optional and determines whether the string should be encoded in UTF-16 charset when set to `true`. This is useful for strings handled by the console and not the game.
- `duration` represents the duration of the key.
- `string` contains the key string, always enclosed in double quotes. If the string itself contains a double quote, it should be escaped using `\"`.

**Note:** `mh2-gxttool` uses UTF-8 encoding for the TOML files. You can check the available characters for Manhunt 2 [here](https://github.com/santiago046/manhunt2-translation-resources/blob/main/font-and-charset-info.md#manhunt-2-charset-en-fr-ge-it-sp).

#### Charset File Syntax

The `-c/--charset-file` option allows you to specify a TOML file that maps the game charset to UTF-8. The file should have the following format:

```toml
"\unicode_hex" = "utf-8"
```

The `\unicode_hex` represents the hexadecimal representation of a character in the game font, and `utf-8` represents a single UTF-8 character. For example, from the original Manhunt 2 charset:

```toml
"\u0080" = "À"
"\u0081" = "Á"
"\u0082" = "Â"
"\u0083" = "Ä"
"\u0084" = "Æ"
"\u0085" = "Ç"
"\u0086" = "È"
"\u0087" = "É"
"\u0088" = "Ê"
"\u0089" = "Ë"
"\u008A" = "Ì"
"\u008B" = "Í"
```

## Examples

Here are a few examples demonstrating how to use the `mh2-gxttool`:

1. Unpack `GAME.GXT` from PSP:

   ```bash
   mh2-gxttool unpack -p PSP path_to/GAME.GXT
   ```

2. Unpack `GAME.GXT` from PS2 to `~/resources/` and force overwriting:

   ```bash
   mh2-gxttool unpack -f -p PS2 -o ~/resources/GAME.toml path_to/GAME.GXT
   ```

3. Pack a TOML document (`GAME.toml`) to the PC version:

   ```bash
   mh2-gxttool pack -p PC ~/resources/GAME.toml
   ```

## To-Do

- Add support for the Wii version of Manhunt 2 (it's the same as PC, but big-endian instead).
- Maybe add support for Manhunt (2003).

Happy modding and translating!
