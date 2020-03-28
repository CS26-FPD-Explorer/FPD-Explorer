# FPD-Explorer

A GUI visualizer for the FPD library  

## Getting started

A Python 3 installation is needed to run this program  
Data from a [STEM](https://en.wikipedia.org/wiki/Scanning_transmission_electron_microscopy) microscope is needed to make full use of the program's capabilities

### Installing

Install **FPD-Explorer** package using the *setup* script from the project root:

```shell
python setup.py install
```
#### Dark style
A dark style is available for this program. It can be installed with either pip:

```shell
pip3 install git+git://github.com/09ubberboy90/qdarkgraystyle.git
```
or cloning the repository:

```shell
git clone https://github.com/09ubberboy90/qdarkgraystyle.git
cd qdarkgraystyle
python setup.py install
```

### Interface compilation
Run this command from the project root before starting for the first time:
```shell
python compile_ui.py
```

## Running

Run this command from the project root:

```shell
python main.py
```

## Running the tests

Run this command from the project root:

```shell
pytest
```
## Built with

* [Qt5](https://www.qt.io/) - The GUI framework used
* [PySide2](https://pypi.org/project/PySide2/) - Python wrapper for Qt5


## Authors

* [Bruce Kerr](mailto:2316957k@student.gla.ac.uk)
* [Ewan Duncan Pandelus](mailto:2319069p@student.gla.ac.uk)
* [Florent Audonnet](mailto:2330834a@student.gla.ac.uk)
* [Michal Broos](mailto:2330994b@student.gla.ac.uk)
* [Ruize Shen](mailto:2361590s@student.gla.ac.uk)


## License

This project is licensed under the GPLv3 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* [FPD library](https://gitlab.com/fpdpy/fpd) and its developer for providing the code needed to analyse the data
* University of Glasgow School of Physics & Astronomy for giving us this project, especially [Dr Damien McGrouther](mailto:Damien.McGrouther@glasgow.ac.uk) and [Dr Trevor Almeida](mailto:Trevor.Almeida@glasgow.ac.uk)
* University of Glasgow School of Computing Science for providing the courses without which this project would not have been possible
* [Justyna Toporkiewicz](mailto:2270645t@student.gla.ac.uk) for being our coach and helping us during the development
