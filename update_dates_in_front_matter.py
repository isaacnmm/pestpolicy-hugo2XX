import os
import re
import yaml
from datetime import datetime

TARGET_DATE = "2025-08-10 00:00:00+00:00"

def update_dates_in_front_matter(raw_front_matter):
    try:
        data = yaml.safe_load(raw_front_matter)
    except Exception as e:
        print(f"YAML load error: {e}")
        return raw_front_matter.strip()

    if not isinstance(data, dict):
        return raw_front_matter.strip()

    # Update date and lastmod fields
    if 'date' in data:
        data['date'] = TARGET_DATE
    if 'lastmod' in data:
        data['lastmod'] = TARGET_DATE

    # Dump YAML without indentation on lists (if any)
    dumped = yaml.dump(data, sort_keys=False, default_flow_style=False)
    return dumped.strip()

def process_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fm_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not fm_match:
        print(f"No front matter found in: {filepath}")
        return

    front_matter = fm_match.group(1)
    rest_content = content[fm_match.end():]

    updated_fm = update_dates_in_front_matter(front_matter)

    new_content = f"---\n{updated_fm}\n---\n{rest_content.lstrip()}"
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated dates in: {filepath}")
    else:
        print(f"No date update needed: {filepath}")

def process_folder(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                process_markdown_file(filepath)

if __name__ == "__main__":
    content_folder = "content/posts"
    process_folder(content_folder)
