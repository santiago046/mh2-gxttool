from setuptools import setup, find_packages

with open("requirements.txt") as f, open("README.md") as fh:
    required = f.read().splitlines()
    long_description = fh.read()

setup(
    name="mh2-gxttool",
    version="1.0.0",
    description="CLI tool to unpack/pack GXT files from Manhunt 2 PSP/PS2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="santiago046",
    license="GPLv3",
    url="https://github.com/santiago046/mh2-gxtttool",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=required,
    entry_points={
        "console_scripts": ["mh2-gxttool = mh2_gxttool.__main__:cli"]
    },
    project_urls={"Source code": "https://github.com/santiago046/mh2-gxttool"},
)
