import os
import re

# Path to your Hugo content folder
CONTENT_DIR = r"C:\My Hugo Sites\pestpolicy-hugo2XX\content"

# Pattern to capture front matter title lines
TITLE_PATTERN = re.compile(r'^title:\s*["\']?(.*?)["\']?\s*$', re.IGNORECASE)

matches = []

for root, _, files in os.walk(CONTENT_DIR):
    for file in files:
        if file.endswith(".md"):
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        match = TITLE_PATTERN.match(line.strip())
                        if match:
                            title = match.group(1)
                            if "Home - " in title or " - Home" in title:
                                matches.append((file_path, title))
                            break  # only check the first title line
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

if matches:
    print("Titles containing 'Home - ' or ' - Home':")
    for path, title in matches:
        print(f"{path} → {title}")
else:
    print("No titles with 'Home - ' or ' - Home' found.")
