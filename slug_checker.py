import os
import re
import shutil

# Path to your Hugo posts folder
POSTS_DIR = r"C:\My Hugo Sites\pestpolicy-hugo2XX\content\posts"

# Regex to match slug line with leading/trailing slashes
slug_pattern = re.compile(r'^(slug:\s*/)(.*?)(/?)\s*$', re.IGNORECASE)

for root, dirs, files in os.walk(POSTS_DIR):
    for filename in files:
        if filename.endswith(".md"):
            filepath = os.path.join(root, filename)

            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()

            changed = False
            for i, line in enumerate(lines):
                match = slug_pattern.match(line.strip())
                if match:
                    core_slug = match.group(2)  # Remove leading/trailing slash
                    lines[i] = f"slug: {core_slug}\n"
                    changed = True

            if changed:
                # Create backup file
                backup_path = filepath + ".bak"
                shutil.copy2(filepath, backup_path)

                # Write updated file
                with open(filepath, "w", encoding="utf-8") as f:
                    f.writelines(lines)

                print(f"Updated slug in: {filepath} (backup saved to {backup_path})")

print("✅ All slugs fixed. Backups created with .bak extension.")
