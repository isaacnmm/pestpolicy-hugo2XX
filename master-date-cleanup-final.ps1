$targetDirectory = "C:\Users\Zak\Documents\pestpolicy-hugo2XX\content"

# Define the exact date and lastmod values to ensure
$correctDateValue = "2025-05-19T00:00:00+00:00"
$correctLastmodValue = "2025-05-19T00:00:00+03:00"

# VERY Robust regex to find ANY line starting with $1 followed by a date pattern.
# It now broadly matches '$1' then a date, then anything (or nothing) until the end of the line.
$patternToRemove = '(?m)^\$1\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2}.*$'

# Get all Markdown files (posts and pages) recursively from the target directory.
Get-ChildItem -Path $targetDirectory -Recurse -File -Include "*.md", "*.markdown" | ForEach-Object {
    $filePath = $_.FullName
    $content = Get-Content -Path $filePath -Raw # Read the entire file content as a single string.
    $originalContent = $content # Keep original to check for changes

    Write-Host "Processing file: $($filePath)"

    # --- Step 1: Aggressively remove any problematic '$1' lines ---
    if ($content -match $patternToRemove) {
        $content = $content -replace $patternToRemove, ""
        Write-Host "  > Removed problematic '$1' date line(s)."
    } else {
        Write-Host "  > No problematic '$1' date line found."
    }

    # --- Step 2: Ensure 'date' and 'lastmod' fields are correctly set and unique ---
    $frontMatterMatch = $content -match "(?msi)^(---\s*\r?\n)(.*?)\r?\n(---)"

    if ($frontMatterMatch) {
        $openingDelimiter = $Matches[1] # e.g., "---" + newline
        $frontMatterBlock = $Matches[2] # All content between delimiters
        $closingDelimiter = $Matches[3] # e.g., "---"

        $frontMatterLines = $frontMatterBlock -split "`r?`n" # Split block into lines
        $filteredLines = @() # To store non-date/lastmod lines

        # Filter out all existing date/lastmod lines to prepare for re-insertion
        foreach ($line in $frontMatterLines) {
            # Trim the line to handle leading/trailing whitespace before checking
            $trimmedLine = $line.Trim()
            if ($trimmedLine -notmatch '(?mi)^date:\s*' -and $trimmedLine -notmatch '(?mi)^lastmod:\s*') {
                if ($trimmedLine -ne "") { # Only keep non-empty, non-date/lastmod lines
                    $filteredLines += $line # Add original line (not trimmed) to preserve indentation if any
                }
            }
        }

        # Reconstruct the new front matter block:
        $newFrontMatterBlockArray = @()
        $newFrontMatterBlockArray += "date: '$correctDateValue'"   # Add the canonical date line
        $newFrontMatterBlockArray += "lastmod: '$correctLastmodValue'" # Add the canonical lastmod line
        $newFrontMatterBlockArray += $filteredLines # Add all other filtered lines

        # Join the new block with newlines.
        # Use .Trim() on the result to avoid extra leading/trailing newlines within the block.
        $newFrontMatterContent = ($newFrontMatterBlockArray -join "`n").Trim()

        # Replace the old front matter block with the newly constructed one
        $content = $content -replace "(?msi)^(---\s*\r?\n)(.*?)\r?\n(---)", "$openingDelimiter$newFrontMatterContent`n$closingDelimiter"

        # Indicate modification if content has changed
        if ($content -ne $originalContent) {
            Write-Host "  > Front matter updated (date/lastmod ensured unique and correct)."
        } else {
            Write-Host "  > Front matter already correct (date/lastmod unique and correct)."
        }
    } else {
        Write-Host "  > Warning: No YAML front matter detected (missing '---' delimiters). Skipping date/lastmod processing."
    }

    # Save the file only if the content has changed
    if ($content -ne $originalContent) {
        $content | Set-Content -Path $filePath -Force -Encoding UTF8 # Ensure UTF8 encoding.
        Write-Host "  > File saved with changes."
    } else {
        Write-Host "  > No further changes needed, skipping save."
    }
    Write-Host "---" # Separator for clarity in console output
}

Write-Host " "
Write-Host "Script finished. Review your files and deploy to Netlify."