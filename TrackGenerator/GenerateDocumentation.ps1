$files = Get-ChildItem $PSScriptRoot -Filter "*.py"

foreach($file in $files){
    Write-Host "$PSScriptRoot\$file"
    pydoc.exe -w `"$PSScriptRoot\$file`"
}

$docPath = "$PSScriptRoot\GeneratedDocumentation"
if (Test-Path $docPath){
    Remove-Item $docPath -Force -Recurse
}
New-Item $docPath -ItemType Directory

$htmlFiles = Get-ChildItem $PSScriptRoot -Filter "*.html"
foreach($file in $htmlFiles){
    Move-Item "$PSScriptRoot\$file" $docPath\$file
}
