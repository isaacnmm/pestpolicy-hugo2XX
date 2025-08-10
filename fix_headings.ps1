param(
    [string]$FolderPath = "."
)

# Backup files before editing (optional)
function Backup-File($file) {
    $bakPath = "$file.bak"
    if (-not (Test-Path $bakPath)) {
        Copy-Item $file $bakPath
    }
}

# Fix heading line
function Fix-HeadingLine($line) {
    # Match headings starting with ## and containing "s:" after hashes
    if ($line -match '^(#+)\s*s:\s*(.+)') {
        $level = $matches[1]
        $text = $matches[2]

        # Add space before [ if missing
        $text = $text -replace '(\S)\[', '$1 ['

        return "$level $text"
    }
    else {
        # Also fix spacing before [ if missing for headings without s:
        if ($line -match '^(#+)\s*(.+)') {
            $level = $matches[1]
            $text = $matches[2]

            $newText = $text -replace '(\S)\[', '$1 ['
            if ($newText -ne $text) {
                return "$level $newText"
            }
        }
        return $line
    }
}

Write-Host "Processing Markdown files in $FolderPath..."

Get-ChildItem -Path $FolderPath -Recurse -Include *.md | ForEach-Object {
    $file = $_.FullName
    Backup-File $file

    $content = Get-Content $file

    $changed = $false
    for ($i=0; $i -lt $content.Length; $i++) {
        $fixedLine = Fix-HeadingLine $content[$i]
        if ($fixedLine -ne $content[$i]) {
            $content[$i] = $fixedLine
            $changed = $true
        }
    }

    if ($changed) {
        Set-Content -Path $file -Value $content -Encoding utf8
        Write-Host "Fixed headings in: $file"
    }
}

Write-Host "Done."
