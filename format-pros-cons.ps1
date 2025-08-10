# Path to your posts folder
$postsPath = "C:\My Hugo Sites\pestpolicy-hugo2XX\content\posts"

# Regex to match Pros or Cons lines with items separated by ' - '
$pattern = '(Pros|Cons):\s*(.+)'

# Process each index.md file recursively
Get-ChildItem -Path $postsPath -Filter "index.md" -Recurse | ForEach-Object {
    $file = $_.FullName
    $content = Get-Content $file -Raw

    if ($content -match $pattern) {
        # Replace Pros/Cons lines with properly formatted bullet lists
        $newContent = [regex]::Replace($content, $pattern, {
            param($match)

            $heading = $match.Groups[1].Value
            $itemsLine = $match.Groups[2].Value.Trim()

            # Split items by ' - ' and remove empty entries
            $items = $itemsLine -split ' - ' | Where-Object { $_ -ne "" }

            # Format each item as a bullet point
            $formattedItems = $items | ForEach-Object { "- $_" }

            # Return heading and formatted list with newlines
            "`n${heading}:`n" + ($formattedItems -join "`n") + "`n"
        })

        # Write back the new content to the file
        Set-Content -Path $file -Value $newContent -Encoding UTF8
        Write-Host "Processed: $file"
    } else {
        Write-Host "No Pros/Cons found in: $file"
    }
}

Write-Host "=== Done formatting Pros and Cons ==="
