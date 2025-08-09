import os
import re

# Adjust this to your Hugo content directory
content_dir = r"C:\My Hugo Sites\pestpolicy-hugo2XX\content"

# Regex to find amazon bestseller shortcodes (flexible matching)
bestseller_shortcode_regex = re.compile(
    r'\[amazon\b[^\]]*bestseller="[^"]*"[^\]]*items="\d+"[^\]]*template="table"[^\]]*\]',
    re.IGNORECASE
)

matches_found = 0

for root, _, files in os.walk(content_dir):
    for filename in files:
        if filename.endswith(('.md', '.markdown')):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = bestseller_shortcode_regex.findall(content)
                if matches:
                    matches_found += len(matches)
                    print(f"Found {len(matches)} match(es) in: {filepath}")
                    for match in matches:
                        print(f"  -> {match}")

if matches_found == 0:
    print("No amazon bestseller shortcodes found in the content directory.")
else:
    print(f"Total {matches_found} amazon bestseller shortcode(s) found.")
