param (
    [string]$Message = ""
)

if (-not $Message) {
    $Message = "Auto commit - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
}

Write-Host "=== Checking Git status ==="
git status

Write-Host "=== Adding changes ==="
git add -A

Write-Host "=== Committing ==="
git commit -m "$Message"

Write-Host "=== Pushing to origin/main ==="
git push origin main

Write-Host "=== Done ==="
