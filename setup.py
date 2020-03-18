# Standard Library
import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = []
if os.path.isfile("requirements.txt"):
    with open("requirements.txt") as f:
        install_requires = f.read().splitlines()

setuptools.setup(
    name="FPD-Explorer",
    version="1.0",
    author="Bruce Kerr, Ewan Pandelus, Florent Audonnet, Michal Broos, Ruize Shen",
    author_email="""2316957k@student.gla.ac.uk, 2319069p@student.gla.ac.uk,
    2330834a@student.gla.ac.uk, 2330994b@student.gla.ac.uk, 2361590s@student.gla.ac.uk""",
    description="A GUI visualizer for the FPD library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://stgit.dcs.gla.ac.uk./tp3-2019-cs26/cs26-main",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
