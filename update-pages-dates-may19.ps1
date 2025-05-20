$targetDirectory = "C:\Users\Zak\Documents\pestpolicy-hugo2XX\content"

# Define the specific date and time values: May 19, 2025.
# 'date' typically uses UTC.
$newDateValue = "2025-05-19T00:00:00+00:00"
# 'lastmod' uses your local timezone's offset (+03:00) as per your samples.
$newLastmodValue = "2025-05-19T00:00:00+03:00"

# Regular expressions to find and capture parts of the date and lastmod lines.
# (?mi) makes the match case-insensitive and multiline.
$datePattern = "(?mi)^(date:\s*').*?(\+\d{2}:\d{2}')"
$lastmodPattern = "(?mi)^(lastmod:\s*).*?([+-]\d{2}:\d{2})"

# Loop through all Markdown files in the target directory, excluding the 'posts' subdirectory.
Get-ChildItem -Path $targetDirectory -Recurse -File -Include "*.md", "*.markdown" | Where-Object {
    # Exclude any files that are within a directory named 'posts'
    $_.DirectoryName -notlike "*\posts\*"
} | ForEach-Object {
    $filePath = $_.FullName
    $content = Get-Content -Path $filePath -Raw # Read the entire file content as a single string.
    $modified = $false # Flag to track if the file was changed.

    Write-Host "Processing file: $($filePath)"

    # Attempt to update the 'date' field.
    if ($content -match $datePattern) {
        $newContent = $content -replace $datePattern, "`$1$newDateValue"
        $content = $newContent
        $modified = $true
        Write-Host "  > 'date' updated."
    } else {
        Write-Host "  > 'date' field not found or not matching pattern. Skipping."
    }

    # Attempt to update the 'lastmod' field.
    if ($content -match $lastmodPattern) {
        $newContent = $content -replace $lastmodPattern, "`$1$newLastmodValue"
        $content = $newContent
        $modified = $true
        Write-Host "  > 'lastmod' updated."
    } else {
        Write-Host "  > 'lastmod' field not found or not matching pattern."
    }

    # If any changes were made, write the modified content back to the file.
    if ($modified) {
        $content | Set-Content -Path $filePath -Force # -Force ensures overwriting.
    } else {
        Write-Host "  > No date fields updated in this file. Skipping save."
    }
}

Write-Host " "
Write-Host "Script finished. Review your files for changes."