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