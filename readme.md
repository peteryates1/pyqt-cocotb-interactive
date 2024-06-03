# [PyQt5] [cocotb] interactive

Very simple interactive simulation using [cocotb] and [PyQt5] based on on [GHDL Interactive Simulation] and [GHDL VPI virtual board]

## Requirements
- [Python] (tested using version 3.10)
- [iverilog] (tested using version 13 from master)
- [GNU Make]

## Running
- Get Python dependencies first...
```bash
pip install -r requirements.txt
```
- Then in the test directory...
```bash
make
```

## Credits
Many thanks to the [GHDL Interactive Simulation] and [GHDL VPI virtual board] project for the inspiration and the images (which I shamelessly borrowed given how artistically challenged I am - ditto).

[GHDL Interactive Simulation]:  https://github.com/chuckb/ghdl-interactive-sim/blob/main/README.md
[GHDL VPI virtual board]:       https://gitlab.ensta-bretagne.fr/bollenth/ghdl-vpi-virtual-board
[GNU Make]:                     https://www.gnu.org/software/make/
[PyQt5]:                        https://pypi.org/project/PyQt5/
[Cocotb]:                       https://docs.cocotb.org/en/stable/
[Python]:                       https://www.python.org/downloads/
[iverilog]:                     https://steveicarus.github.io/iverilog/
[iverilog-src]:                 https://github.com/steveicarus/iverilog
