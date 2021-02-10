[CmdletBinding()]
param (
    [Parameter()]
    [string]
    $Path
)

$os = [System.Environment]::OSVersion
if($os -match "Unix"){
    $linux = $true
}
else{
    $linux = $false
}

if($linux){
    python3 `"$PSScriptRoot/../util/config.py`" -x $Path
}
else{
	python.exe "$PSScriptRoot\..\util\config.py" -x $Path
}