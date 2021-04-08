# OpenDRIVE Map Generator

This is a generator for race tracks within the [CARLA Simulator](https://carla.org/). It's not perfect yet, as curves are not connecting seemlessly to other track parts. Everything is implemented in accordance with the [OpenDRIVE 1.6 standard](https://releases.asam.net/OpenDRIVE/1.6.0/ASAM_OpenDRIVE_BS_V1-6-0.html).

To integrate this into the CARLA simulator, just copy everything into the CARLA main directory.

To start the simulator as server, just execute the StartSimulator.ps1 script with PowerShell.

## Code

The code of the generator is located inside the "TrackGenerator" directory.

#### Documentation

Code documentation is not delivered by default, but can be compiled by executing "GenerateDocumentation.ps1" inside the "TrackGenerator" directory using PowerShell.
This will create a directory called "GeneratedDocumentation" inside the "TrackGenerator" directory, containing the documentation for each code file in HTML format.

There is also a Linux version: Call "generateDocumentation.sh" in the same directory to generate documentation under Linux.

#### Generating streets

To generate a street with the OPENDrive API, import the API module with 
```python
import OpenDRIVE_API
```

After doing so, start and build your streets as follows:
```python
OpenDRIVE_API.start_street()
OpenDRIVE_API.generate_line(0, -10, 0, 0, 30)
(...)
OpenDRIVE_API.end_street()
```
Make sure to start each street with `OpenDRIVE_API.start_street()` and end it with `OpenDRIVE_API.end_street()`, otherwise you will run into exceptions.
Use the start method to set road parameters like lane width or road type.

#### Generating track polygons

Tracks are represented by irregular polygons with n corners. These can be generated using the TrackPolygonGenerator module. It can be either imported to be used by other Python modules or be called from the command line. Providing `-h` as parameter displays the help function.
The dimensions of the polygon can be adjusted with the `-x` and `-y` parameter respectively, defining maximum width and height. The amount of corners can be defined with the `-c` parameter.
Additionally, the generated polygon can be diplayed graphically by setting the `-s` flag.

Generating polygons from the command line does NOT save them anywhere. It merely provides a simple way to get a feeling for good values to use with the generator.


## License Note:

Thie project is provided unter MIT license ![MIT License Logo](/uploads/bc9f634c577db82a0d9a4292734a026c/91196268-63b5-4881-9885-a0e367829332.png "MIT License Logo"). See LICENSE file for additional information.

## Setup

#### Required Software

- CALRA simulator (min. version 0.9.10)
- Python IDE of your choice (or vim, emacs, or whatever you like)
- PowerShell (min. version 5.1) or PowerShell Core if you're a Linux user
    - For Linux: "snap install powershell --classic"
    - For Win 10: Pre-installed
- Python 3.7 or higher

#### Required Hardware

- Dedicated GPU with min. 4 GB of VRAM
- 64-bit OS
    - Attention Linus-users: CARLA does not work with Linux version 16.04 when using default compilers -> Upgrade! Alternatively upgrade you Linux to 16.09 or higher.

#### Installation

- Install CARLA
- Checkout this project into the CARLA main directory (where the CarlaUE4.exe/CarlaUE4.sh is located). This projects integrates itself seamlessly into the CARLA structure.
- Generate your documentation: Navigate into the "TrackGenerator" dir and execute "GenerateDocumentation.ps1" ("GenerateDocumentation.sh" if you're on Linux)
- Done! You can now open the project within your Python IDE or execute it however you like.
