$targetDirectory = "C:\Users\Zak\Documents\pestpolicy-hugo2XX\content\posts"

# CORRECTED: Text to remove - NO newline at the very end after '---'
# The `n characters within the string are PowerShell's way of representing newlines.
$textToRemove = "> **We may earn a commission when you click and buy from Amazon.com.**`n>`n`n---"

# Escape special characters for Regex in the text to remove
$textToRemoveRegex = [regex]::Escape($textToRemove)

Get-ChildItem -Path $targetDirectory -Recurse -File -Include "*.md", "*.markdown" | ForEach-Object {
    $filePath = $_.FullName
    $content = Get-Content -Path $filePath -Raw

    if ($content -match $textToRemoveRegex) {
        Write-Host "Processing file: $($filePath)"
        # Replace the matched text with an empty string, effectively deleting it
        $newContent = $content -replace $textToRemoveRegex, ""
        $newContent | Set-Content -Path $filePath -Force

        Write-Host "  > Text removed."
    } else {
        Write-Host "Processing file: $($filePath)"
        Write-Host "  > Text not found in this file. Skipping."
    }
}

Write-Host " "
Write-Host "Script finished. Check your files."