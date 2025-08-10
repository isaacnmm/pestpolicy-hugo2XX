import re
import os

def fix_links_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    pattern = re.compile(r'(\[.*?\])\((.*?)\)')

    def clean_url(match):
        text = match.group(1)
        url = match.group(2)
        fixed_url = url.replace(' ', '')
        return f"{text}({fixed_url})"

    fixed_content = pattern.sub(clean_url, content)

    if fixed_content != content:
        print(f"Fixed links in: {filepath}")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)

def fix_links_in_folder(folder):
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                fix_links_in_file(os.path.join(root, file))

if __name__ == "__main__":
    folder_path = r"C:\My Hugo Sites\pestpolicy-hugo2XX\content\posts"
    fix_links_in_folder(folder_path)
