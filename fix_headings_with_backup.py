import os
import re
import sys
import shutil

def fix_headings_with_backup(folder_path):
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                backup_path = file_path + ".bak_heading"

                # Create backup
                shutil.copy2(file_path, backup_path)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Fix headings like "##  s: ..."
                fixed_content = re.sub(r"(##+)\s*s:\s*", r"\1 ", content)

                if fixed_content != content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(fixed_content)
                    print(f"Fixed: {file_path}  |  Backup saved: {backup_path}")
                else:
                    print(f"No change: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_headings_with_backup.py <folder_path>")
    else:
        fix_headings_with_backup(sys.argv[1])
