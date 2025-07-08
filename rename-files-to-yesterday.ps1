# --- IMPORTANT: BACK UP YOUR C:\Sites\pestpolicy-hugo2XX\content folder BEFORE RUNNING THIS SCRIPT! ---

# Calculate yesterday's date in YYYY-MM-DD format
$yesterdayDate = (Get-Date).AddDays(-1).ToString('yyyy-MM-dd')

# !!! VERIFY THIS PATH IS CORRECT FOR YOUR HUGO POSTS FOLDER !!!
$postsPath = "C:\Sites\pestpolicy-hugo2XX\content\posts"

Write-Host "Starting file renaming process for posts in: $postsPath"
Write-Host "Target filename date: $yesterdayDate (Yesterday's date)"
Write-Host "--------------------------------------------------------"

# Get all markdown files recursively in the posts directory
Get-ChildItem -Path $postsPath -Recurse -Include *.md, *.markdown | ForEach-Object {
    $filePath = $_.FullName
    $fileName = $_.BaseName # e.g., "2025-06-21-what-is-wet-area-bathroom"
    $fileExtension = $_.Extension

    # CORRECTED REGEX AND FILENAME CONSTRUCTION:
    # This regex now captures everything AFTER the initial "YYYY-MM-DD-" part into $Matches[1] (the slug).
    if ($fileName -match "^\d{4}-\d{2}-\d{2}-(.+)$") {
        $slug = $Matches[1] # This captures only the slug part (e.g., "what-is-wet-area-bathroom")

        # Construct the new filename using the full yesterday's date (which includes the year)
        $newFileNameOnly = "$yesterdayDate-$slug" + $fileExtension
        $newFilePath = Join-Path -Path $_.DirectoryName -ChildPath $newFileNameOnly

        # Only attempt to rename if the name is actually different
        if ($filePath -ne $newFilePath) {
            try {
                Rename-Item -Path $filePath -NewName $newFileNameOnly -Force
                Write-Host "SUCCESS: Renamed: '$filePath'"
                Write-Host "         -> New name: '$newFilePath'"
            } catch {
                Write-Error "ERROR: Failed to rename '$filePath': $($_.Exception.Message)"
            }
        } else {
            Write-Host "INFO: Skipped: '$filePath' already has the target date ($yesterdayDate) in its filename."
        }
    } else {
        Write-Warning "WARNING: Filename format not recognized for '$filePath'. Expected 'YYYY-MM-DD-slug'. Skipping."
    }
}

Write-Host "--------------------------------------------------------"
Write-Host "File renaming process complete. **REMEMBER TO HANDLE REDIRECTS FOR ALL CHANGED URLS.**"