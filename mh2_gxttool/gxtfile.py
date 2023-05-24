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

import io
import struct

from pathlib import Path

from .mh2utils import MH2Utils


class GXTFileFormatError(Exception):
    """Error when file is not a valid GXT."""

    pass


class GXTFile:

    @staticmethod
    def pack(src_file: Path, dst_file: Path, platform="PSP"):
        """
        Pack a TOML document to a GXT file.

        Args:
            src_file: A pathlib.Path object to the TOML document to pack
            dst_file: A pathlib.Path object to the GXT file
            platform: A string to tell the game platform, default: PSP
        """

        keys_info = MH2Utils._from_toml(src_file)
        key_str_fmt = "<I12sI" if platform == "PC" else "<I8sI"

        with io.BytesIO() as tkey_buffer, io.BytesIO() as tdat_buffer:
            tdat_size = 0  # Used to key_data_offset too
            for key, value in keys_info.items():
                key_data_offset = tdat_size
                key_name = key.encode("ASCII")
                key_duration = value["duration"]

                tkey_buffer.write(
                    struct.pack(
                        key_str_fmt, key_data_offset, key_name, key_duration
                    )
                )

                key_string_bytes = (
                    value["string"].encode("UTF-16LE") + b"\x00\x00"
                    if value.get("console", False)
                    else MH2Utils._encode_string(value["string"])
                )

                tdat_buffer.write(key_string_bytes)
                # Update tdat size
                tdat_size += len(key_string_bytes)

            # Writing dst_file
            with dst_file.open("wb") as gxt_file:
                # Write TKEY signature and its size
                gxt_file.write(
                    struct.pack(
                        "<4sI", b"TKEY", tkey_buffer.getbuffer().nbytes
                    )
                )
                # Write TKEY data
                gxt_file.write(tkey_buffer.getvalue())

                # Write TDAT signature and its size
                gxt_file.write(struct.pack("<4sI", b"TDAT", tdat_size))
                # Write TDAT data
                gxt_file.write(tdat_buffer.getvalue())

    @staticmethod
    def unpack(src_file: Path, dst_file: Path, platform="PSP"):
        """
        Unpack a GXT file to a TOML document.

        Args:
            src_file: A pathlib.Path object to the GXT file to unpack
            dst_file: A pathlib.Path object to the TOML document file
            platform: A string to tell the game platform, default: PSP

        Raises:
            InvalidGXTFileError: when src_file is not a valid GXT file
        """

        key_str_fmt = struct_fmt = "<I12sI" if platform == "PC" else "<I8sI"

        with src_file.open("rb") as gxt_file:
            # Check TKEY
            if gxt_file.read(4) != b"TKEY":
                raise GXTFileFormatError(
                    f"'{src_file}' is not a valid GXT file, missing TKEY signature"
                )

            tkey_size = struct.unpack("<I", gxt_file.read(4))[0]

            # Read TKEY content
            keys_info = [
                {
                    "offset": key_offset,
                    "name": key_name.decode("ASCII").strip("\x00"),
                    "duration": key_duration,
                }
                for key_offset, key_name, key_duration in struct.iter_unpack(
                    key_str_fmt, gxt_file.read(tkey_size)
                )
            ]

            # Check TDAT
            if gxt_file.read(4) != b"TDAT":
                raise GXTFileFormatError(
                    f"'{src_file}' is not a valid GXT file, missing TDAT signature"
                )

            # Next four bytes is the tdat_size in int32 LE, not used in the code
            tdat_size = gxt_file.read(4)

            # Start of TDAT content
            current_pos = gxt_file.tell()

            # Read TDAT content
            for key in iter(keys_info):
                gxt_file.seek(key["offset"] + current_pos)

                key_str_data = bytearray()
                # Read string encoded in UTF-16LE until a NULL (end of the string)
                while True:
                    char = gxt_file.read(2)

                    if char == b"\x00\x00":
                        break
                    else:
                        key_str_data.extend(char)

                key["string"] = MH2Utils._decode_string(key_str_data)

        # Write dst file
        with dst_file.open("wt", encoding="UTF-8") as toml_file:
            toml_file.write(MH2Utils._to_toml(src_file.name, keys_info))
