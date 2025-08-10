param(
    [string]$msg = "Auto commit"
)

Write-Host "=== Checking Git status ===" -ForegroundColor Cyan
git status

Write-Host "=== Adding changes ===" -ForegroundColor Cyan
git add -A

Write-Host "=== Committing ===" -ForegroundColor Cyan
git commit -m $msg

Write-Host "=== Pushing to origin/main ===" -ForegroundColor Cyan
git push origin main

Write-Host "=== Done ===" -ForegroundColor Green
