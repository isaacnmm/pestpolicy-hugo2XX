$postsPath = "C:\My Hugo Sites\pestpolicy-hugo2XX\content\posts"

Get-ChildItem -Path $postsPath -Filter "index.md" -Recurse | ForEach-Object {
    $file = $_.FullName
    $backupFile = "$file.bak"

    # Create a backup if not already exists
    if (-not (Test-Path $backupFile)) {
        Copy-Item $file $backupFile
    }

    # Read content, filter out lines with 'See Also:' (case-insensitive), with or without leading '>'
    $content = Get-Content $file | Where-Object { $_ -notmatch "^\s*>?\s*See Also:" }

    # Overwrite the original file with filtered content
    Set-Content -Path $file -Value $content -Encoding utf8

    Write-Host "Processed: $file"
}

Write-Host "=== Done removing 'See Also:' lines from posts ==="
