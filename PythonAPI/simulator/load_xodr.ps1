[CmdletBinding()]
param (
    [Parameter()]
    [string]
    $Path
)

python.exe "$PSScriptRoot\..\util\config.py" -x $Path