from setuptools import setup, find_packages

with open("README.md") as rf:
    readme_file = rf.read()

setup(
    name="mh2-gxttool",
    version="2023.05.27",
    description="CLI tool to unpack/pack GXT files from Manhunt 2 PSP/PS2/PC",
    long_description=readme_file,
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://github.com/santiago046/mh2-gxtttool",
    project_urls={"Source code": "https://github.com/santiago046/mh2-gxttool"},
    author="santiago046",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=["click>=8.1.3", "natsort>=8.3.1", "tomlkit>=0.11.8"],
    entry_points={"console_scripts": ["mh2-gxttool = mh2_gxttool.main:cli"]},
)
