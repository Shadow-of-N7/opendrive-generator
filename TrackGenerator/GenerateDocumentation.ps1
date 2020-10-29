$files = Get-ChildItem $PSScriptRoot -Filter "*.py"
$os = [System.Environment]::OSVersion
if($os -match "Unix"){
    $linux = $true
}
else{
    $linux = $false
}

if($linux){
    foreach($file in $files){
        pydoc3 -w `"$PSScriptRoot\$file`"
    }
    $docPath = "$PSScriptRoot/GeneratedDocumentation"
}
else{
    foreach($file in $files){
        pydoc.exe -w `"$PSScriptRoot\$file`"
    }
    $docPath = "$PSScriptRoot\GeneratedDocumentation"
}


if (Test-Path $docPath){
    Remove-Item $docPath -Force -Recurse
}
New-Item $docPath -ItemType Directory

$htmlFiles = Get-ChildItem $PSScriptRoot -Filter "*.html"

if($linux){
    foreach($file in $htmlFiles){
        Move-Item "$PSScriptRoot/$file" "$docPath/$file"
    }
}
else{
    foreach($file in $htmlFiles){
        Move-Item "$PSScriptRoot\$file" "$docPath\$file"
    }
}

