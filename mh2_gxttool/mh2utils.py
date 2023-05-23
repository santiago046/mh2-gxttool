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

import tomlkit
from pathlib import Path


class MH2Utils:
    CHARSET = str.maketrans({
        "\x80": "À",
        "\x81": "Á",
        "\x82": "Â",
        "\x83": "Ä",
        "\x84": "Æ",
        "\x85": "Ç",
        "\x86": "È",
        "\x87": "É",
        "\x88": "Ê",
        "\x89": "Ë",
        "\x8A": "Ì",
        "\x8B": "Í",
        "\x8C": "Î",
        "\x8D": "Ï",
        "\x8E": "Ò",
        "\x8F": "Ó",
        "\x90": "Ô",
        "\x91": "Ö",
        "\x92": "Ù",
        "\x93": "Ú",
        "\x94": "Û",
        "\x95": "Ü",
        "\x96": "ß",
        "\x97": "à",
        "\x98": "á",
        "\x99": "â",
        "\x9A": "ä",
        "\x9B": "æ",
        "\x9C": "ç",
        "\x9D": "è",
        "\x9E": "é",
        "\x9F": "ê",
        "\xA0": "ë",
        "\xA1": "ì",
        "\xA2": "í",
        "\xA3": "î",
        "\xA4": "ï",
        "\xA5": "ò",
        "\xA6": "ó",
        "\xA7": "ô",
        "\xA8": "ö",
        "\xA9": "ù",
        "\xAA": "ú",
        "\xAB": "û",
        "\xAC": "ü",
        "\xAD": "Ñ",
        "\xAE": "ñ",
        "\xAF": "¿",
        "\xB0": "¡",
        "\xF3": "°",
        "\xF4": "▲",
        "\xF5": "⬤",
        "\xF6": "✕",
        "\xF7": "■",
        "\xF9": "★",
        "\xFA": "®",
        "\xFB": "©",
        "\xFE": "™",
    })

    CHARSET_INV = str.maketrans({
        192: "\x80",
        193: "\x81",
        194: "\x82",
        196: "\x83",
        198: "\x84",
        199: "\x85",
        200: "\x86",
        201: "\x87",
        202: "\x88",
        203: "\x89",
        204: "\x8A",
        205: "\x8B",
        206: "\x8C",
        207: "\x8D",
        210: "\x8E",
        211: "\x8F",
        212: "\x90",
        214: "\x91",
        217: "\x92",
        218: "\x93",
        219: "\x94",
        220: "\x95",
        223: "\x96",
        224: "\x97",
        225: "\x98",
        226: "\x99",
        228: "\x9A",
        230: "\x9B",
        231: "\x9C",
        232: "\x9D",
        233: "\x9E",
        234: "\x9F",
        235: "\xA0",
        236: "\xA1",
        237: "\xA2",
        238: "\xA3",
        239: "\xA4",
        242: "\xA5",
        243: "\xA6",
        244: "\xA7",
        246: "\xA8",
        249: "\xA9",
        250: "\xAA",
        251: "\xAB",
        252: "\xAC",
        209: "\xAD",
        241: "\xAE",
        191: "\xAF",
        161: "\xB0",
        176: "\xF3",
        9650: "\xF4",
        11044: "\xF5",
        10005: "\xF6",
        9632: "\xF7",
        9733: "\xF9",
        174: "\xFA",
        169: "\xFB",
        8482: "\xFE",
    })

    @staticmethod
    def _decode_string(bytes_data: bytes) -> str:
        return bytes_data.decode("UTF-16LE").translate(MH2Utils.CHARSET)

    @staticmethod
    def _encode_string(string_data: str) -> bytes:
        return (
            string_data.translate(MH2Utils.CHARSET_INV).encode("UTF-16LE")
            + b"\x00\x00"
        )

    @staticmethod
    def _to_toml(gxt_name: str, data_list: list):
        doc = {"title": f"Decompiled {gxt_name}"}

        for entry in data_list:
            key = {"duration": entry["duration"], "string": entry["string"]}

            doc[entry["name"]] = key

        return tomlkit.dumps(doc)

    @staticmethod
    def _from_toml(toml_file):
        with open(toml_file, "rt", encoding="UTF-8") as f:
            toml_data = tomlkit.load(f)

            toml_data.pop("title", None)

        return toml_data
