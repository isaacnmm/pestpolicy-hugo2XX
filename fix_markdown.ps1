$postsPath = "C:\My Hugo Sites\pestpolicy-hugo2XX\content\posts"

Get-ChildItem -Path $postsPath -Filter *.md -Recurse | ForEach-Object {
    $file = $_.FullName
    Write-Host "Processing $file"

    # Read all lines
    $content = Get-Content $file -Raw

    # Fix URLs: Remove spaces inside http:// or https:// links
    $content = [regex]::Replace($content, '(https?:)\s*//\s*([\w\.-]+)(\s*[\w\./\-\?=&%]*)', {
        param($m)
        $scheme = $m.Groups[1].Value
        $domain = $m.Groups[2].Value -replace '\s',''
        $rest = $m.Groups[3].Value -replace '\s',''
        return "$scheme//$domain$rest"
    })

    # Fix pinnable shortcode src: remove any brackets or extra chars, keep only path starting with /
    # Matches: src="[best](/best-flea-collar-for-dogs.jpg)" or similar, replace with src="/best-flea-collar-for-dogs.jpg"
    $content = [regex]::Replace($content, 'src="\[.*?\]\((\/[^\)]+)\)"', 'src="$1"')

    # Escape apostrophes inside pinnable shortcode attributes (description and alt)
    # This replaces ' with &#39; inside pinnable shortcode attributes
    # Caution: only inside pinnable shortcode's attribute values between double quotes
    $content = [regex]::Replace($content, '({{<\s*pinnable\s+.*?description=")(.*?)(".*?>}})', {
        param($m)
        $prefix = $m.Groups[1].Value
        $desc = $m.Groups[2].Value -replace "'", '&#39;'
        $suffix = $m.Groups[3].Value
        return "$prefix$desc$suffix"
    }, [System.Text.RegularExpressions.RegexOptions]::Singleline)

    # Also fix apostrophes in alt attribute similarly (optional)
    $content = [regex]::Replace($content, '({{<\s*pinnable\s+.*?alt=")(.*?)(".*?>}})', {
        param($m)
        $prefix = $m.Groups[1].Value
        $alt = $m.Groups[2].Value -replace "'", '&#39;'
        $suffix = $m.Groups[3].Value
        return "$prefix$alt$suffix"
    }, [System.Text.RegularExpressions.RegexOptions]::Singleline)

    # Save fixed content back to file
    Set-Content -Path $file -Value $content -Encoding UTF8
}
Write-Host "Done fixing markdown files."
