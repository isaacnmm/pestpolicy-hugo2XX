# --- CONFIGURATION ---
$ProjectRoot = Get-Location
$PublicPath = Join-Path -Path $ProjectRoot -ChildPath "public"
$HomepageHTML = Join-Path -Path $PublicPath -ChildPath "index.html"
$ConfigFile = if (Test-Path (Join-Path $ProjectRoot "hugo.toml")) { "hugo.toml" } elseif (Test-Path (Join-Path $ProjectRoot "config.yaml")) { "config.yaml" } else { "config.yml" }
# --- END CONFIGURATION ---

# Helper function for colored output
function Write-Check {
    param(
        [string]$Message,
        [bool]$Success
    )
    if ($Success) {
        Write-Host "[✅ OK]      " -ForegroundColor Green -NoNewline
        Write-Host $Message
    } else {
        Write-Host "[❌ FAILED]  " -ForegroundColor Red -NoNewline
        Write-Host $Message
    }
}

Write-Host "--- Starting Hugo Site Post-Build Diagnosis ---" -ForegroundColor Yellow

# === CHECK 1: VERIFY BUILD OUTPUT ===
Write-Host "`n=== 1. Checking for Build Output ===" -ForegroundColor Cyan
$buildExists = Test-Path -Path $HomepageHTML
Write-Check "Homepage exists at '$HomepageHTML'." -Success $buildExists
if (-not $buildExists) {
    Write-Host "CRITICAL ERROR: 'public/index.html' not found. Please run 'hugo' to build the site first." -ForegroundColor Red
    return
}

# === CHECK 2: SEARCH FOR ASSETS ===
Write-Host "`n=== 2. Searching for Generated Assets ===" -ForegroundColor Cyan
$cssFiles = Get-ChildItem -Path $PublicPath -Recurse -Filter "*.css"
Write-Check "Found $($cssFiles.Count) CSS files in the 'public' directory." -Success ($cssFiles.Count -gt 0)

$jsFiles = Get-ChildItem -Path $PublicPath -Recurse -Filter "*.js"
Write-Check "Found $($jsFiles.Count) JavaScript files in the 'public' directory." -Success ($jsFiles.Count -gt 0)

if ($cssFiles.Count -eq 0) {
    Write-Host "WARNING: No CSS files were found. This is a primary cause of a disorganized site." -ForegroundColor Yellow
}

# === CHECK 3: INSPECT HTML FOR ASSET LINKS ===
Write-Host "`n=== 3. Inspecting 'index.html' for CSS and JS Links ===" -ForegroundColor Cyan
$htmlContent = Get-Content -Path $HomepageHTML -Raw

$cssLinkFound = $htmlContent -match '<link rel="stylesheet"'
Write-Check "Homepage HTML contains a CSS stylesheet link (<link rel=`"stylesheet`"...>)." -Success $cssLinkFound

$jsLinkFound = $htmlContent -match '<script src='
Write-Check "Homepage HTML contains a JavaScript link (<script src=...>)." -Success $jsLinkFound

if (-not $cssLinkFound) {
    Write-Host "CRITICAL ERROR: The generated homepage is MISSING the link to its stylesheet. This is why the site looks broken." -ForegroundColor Red
}

# === CHECK 4: CHECK baseURL CONFIGURATION ===
Write-Host "`n=== 4. Checking 'baseURL' in Configuration File ===" -ForegroundColor Cyan
if (Test-Path (Join-Path $ProjectRoot $ConfigFile)) {
    $configFileContent = Get-Content -Path (Join-Path $ProjectRoot $ConfigFile) -Raw
    $isProdURL = $configFileContent -match "baseURL: 'https://"
    Write-Check "Configuration file '$ConfigFile' is using a production baseURL (https://...)." -Success (-not $isProdURL)

    if ($isProdURL) {
        Write-Host "CRITICAL FINDING: Your baseURL is set to a live URL. For local testing, this is the most common cause of broken styles and links." -ForegroundColor Red
        Write-Host "RECOMMENDED FIX: Open '$ConfigFile', add a '#' to the beginning of the baseURL line to comment it out, then restart 'hugo server'." -ForegroundColor Yellow
    }
} else {
    Write-Host "WARNING: Could not find a hugo.toml or config.yaml file." -ForegroundColor Yellow
}

Write-Host "`n--- Diagnosis Complete ---" -ForegroundColor Yellow