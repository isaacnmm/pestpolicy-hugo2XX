# diagnose_build.ps1

param (
    [string]$SiteRoot = "C:\My Hugo Sites\pestpolicy-hugo2XX"
)

Write-Host "Checking Hugo site build readiness in $SiteRoot" -ForegroundColor Cyan

# Look for config file: config.toml, config.yaml or config.yml
$configFiles = @("config.toml", "config.yaml", "config.yml")
$configPath = $null

foreach ($configFile in $configFiles) {
    $fullPath = Join-Path -Path $SiteRoot -ChildPath $configFile
    if (Test-Path $fullPath) {
        $configPath = $fullPath
        break
    }
}

if ($null -eq $configPath) {
    Write-Warning "No config.toml, config.yaml, or config.yml found in root!"
} else {
    Write-Host "Found config file: $configPath" -ForegroundColor Green
}

# Check for package.json and node_modules folder
$packageJsonPath = Join-Path -Path $SiteRoot -ChildPath "package.json"
$nodeModulesPath = Join-Path -Path $SiteRoot -ChildPath "node_modules"

if (Test-Path $packageJsonPath) {
    Write-Host "Found package.json - checking node_modules folder..."
    if (Test-Path $nodeModulesPath) {
        Write-Host "node_modules folder found." -ForegroundColor Green
    } else {
        Write-Warning "node_modules folder NOT found."
    }
} else {
    Write-Warning "No package.json found."
}

# Attempt Hugo build
Write-Host "Attempting local Hugo build..." -ForegroundColor Cyan

$hugoExe = "hugo"
$arguments = @()

if ($configPath) {
    $arguments += "--config"
    $arguments += "`"$configPath`""
}

# Add minify flag to make build leaner
$arguments += "--minify"

# Optional: add build drafts if you want (comment out if not needed)
# $arguments += "-D"

try {
    # Redirect output to files
    $outputFile = Join-Path -Path $SiteRoot -ChildPath "hugo_build_output.txt"
    $errorFile = Join-Path -Path $SiteRoot -ChildPath "hugo_build_error.txt"

    $process = Start-Process -FilePath $hugoExe -ArgumentList $arguments `
        -NoNewWindow -Wait -PassThru `
        -RedirectStandardOutput $outputFile -RedirectStandardError $errorFile

    $stdout = Get-Content $outputFile -Raw
    $stderr = Get-Content $errorFile -Raw

    Write-Host $stdout

    if ($process.ExitCode -eq 0) {
        Write-Host "Build completed successfully." -ForegroundColor Green
        # Cleanup output files
        Remove-Item $outputFile, $errorFile -ErrorAction SilentlyContinue
        exit 0
    } else {
        Write-Error "Build failed with exit code $($process.ExitCode)."
        if ($stderr) {
            Write-Error "Error output:`n$stderr"
        }
        exit $process.ExitCode
    }
}
catch {
    Write-Error "Exception during build: $_"
    exit 1
}
