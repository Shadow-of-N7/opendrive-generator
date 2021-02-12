# OpenDRIVE Map Generator

To integrate this into the CARLA simulator, just copy everything into the CARLA main directory.

To start the simulator as server, just execute the StartSimulator.ps1 script with PowerShell.

## Code

The code of the generator is located inside the "TrackGenerator" directory.

#### Documentation

Code documentation is not delivered by default, but can be comiled by executing "GenerateDocumentation.ps1" inside the "TrackGenerator" directory using PowerShell.
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

![Figure_1](/uploads/4607a15e03fbe66a5cd1d16498f0be1a/Figure_1.png)

## License Note:

Thie project is provided unter MIT license ![MIT License Logo](/uploads/bc9f634c577db82a0d9a4292734a026c/91196268-63b5-4881-9885-a0e367829332.png "MIT License Logo"). See LICENSE file for additional information.
