# --- IMPORTANT: BACK UP YOUR C:\Sites\pestpolicy-hugo2XX\content folder BEFORE RUNNING THIS SCRIPT! ---

# Define the target date and time strings with the exact format and timezone offsets
$targetDateValue = "2025-07-05T00:00:00+00:00"
$targetLastmodValue = "2025-07-05T00:00:00+03:00"

# !!! THIS PATH TARGETS ONLY YOUR 'posts' DIRECTORY !!!
$contentPath = "C:\Sites\pestpolicy-hugo2XX\content\posts" 

Write-Host "Starting date update process for files in: $contentPath"
Write-Host "Target 'date': '$targetDateValue'"
Write-Host "Target 'lastmod': '$targetLastmodValue'"
Write-Host "--------------------------------------------------------"

# Get all markdown files recursively within the specified path
Get-ChildItem -Path $contentPath -Recurse -Include *.md, *.markdown | ForEach-Object {
    $filePath = $_.FullName
    $content = Get-Content -Path $filePath -Raw # Read file content as a single string

    # Regular expression to capture the YAML front matter block (between the '---' lines)
    # (?ms) enables multiline and single-line mode for the regex.
    $frontMatterRegex = "(?ms)^---\s*\r?\n(.*?)\r?\n---\r?\n(.*)$"

    if ($content -match $frontMatterRegex) {
        $frontMatterBlock = $Matches[1] # Content between the '---' markers
        $postContent = $Matches[2]      # Content after the front matter

        $updatedFrontMatter = $frontMatterBlock # Start with the original front matter

        # --- Process 'date:' field ---
        # Regular expression to find the 'date:' field within the front matter block
        # (?m) enables multiline mode for ^ and $ so it works per line within the block.
        $dateFieldRegex = "(?m)^(date:\s*['""]?.*?['""]?)$" # Matches date: followed by any current date string (with/without quotes)

        if ($updatedFrontMatter -match $dateFieldRegex) {
            $oldDateLine = $Matches[1] # The entire line, e.g., "date: 2023-01-15T10:30:00Z"
            $newDateLine = "date: '" + $targetDateValue + "'" # The new line with single quotes
            $updatedFrontMatter = $updatedFrontMatter -replace [regex]::Escape($oldDateLine), $newDateLine
            Write-Host "  -> Updated 'date' in: $filePath"
        } else {
            Write-Warning "  -> WARNING: Could not find 'date:' field in front matter of: $filePath. Skipping 'date' update for this file."
        }

        # --- Process 'lastmod:' field ---
        # Regular expression to find the 'lastmod:' field within the updated front matter block
        $lastmodFieldRegex = "(?m)^(lastmod:\s*['""]?.*?['""]?)$" # Matches lastmod: followed by any current date string (with/without quotes)

        if ($updatedFrontMatter -match $lastmodFieldRegex) {
            $oldLastmodLine = $Matches[1] # The entire line
            $newLastmodLine = "lastmod: '" + $targetLastmodValue + "'" # The new line with single quotes
            $updatedFrontMatter = $updatedFrontMatter -replace [regex]::Escape($oldLastmodLine), $newLastmodLine
            Write-Host "  -> Updated 'lastmod' in: $filePath"
        } else {
            Write-Warning "  -> WARNING: Could not find 'lastmod:' field in front matter of: $filePath. Skipping 'lastmod' update for this file."
        }

        # Reconstruct the entire file content: --- + updated front matter + --- + post content
        $newContent = "---`r`n" + $updatedFrontMatter + "`r`n---`r`n" + $postContent

        # Write the updated content back to the file
        Set-Content -Path $filePath -Value $newContent -NoNewline

        Write-Host "SUCCESS: Processed file: $filePath"
    } else {
        Write-Warning "WARNING: Could not find valid YAML front matter (--- block) in: $filePath. Skipping file."
    }
}

Write-Host "--------------------------------------------------------"
Write-Host "Date update process complete."