# FPD-Explorer

A GUI visualizer for the FPD library  

## Getting started

A Python 3 installation is needed to run this program  
Data from a [STEM](https://en.wikipedia.org/wiki/Scanning_transmission_electron_microscopy) microscope is needed to use the full capabilities of this program

### Installing

Install **FPD-Explorer** package using the *setup* script:

```shell
python setup.py install
```
#### Dark style
A dark style is available for this program. It can be installed with either pip :

```shell
pip3 install git+git://github.com/09ubberboy90/qdarkgraystyle.git
```
or cloning the repository:

```shell
git clone https://github.com/09ubberboy90/qdarkgraystyle.git
cd qdarkgraystyle
python setup.py install
```

## Running the tests

Run this command at the root of the project:

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
* University of Glasgow School of Physics for giving us this project to develop especially [Dr Damien McGrouther](mailto:Damien.McGrouther@glasgow.ac.uk) and [Dr Trevor Almeida](mailto:Trevor.Almeida@glasgow.ac.uk)
* University of Glasgow School of Computer Science for providing the course without which such a project would not have been doable 
* [Justyna Toporkiewicz](mailto:2270645t@student.gla.ac.uk) for being our coach and helping us during this project
