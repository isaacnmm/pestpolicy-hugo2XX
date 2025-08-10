import os
import re

def fix_markdown_links_with_spaces(root_dir):
    markdown_exts = {'.md', '.markdown'}
    # Regex to find markdown links: [link text](URL)
    # Capture groups: 1 = link text, 2 = URL
    md_link_pattern = re.compile(r'(\[[^\]]*\])\(\s*([^\)]+?)\s*\)')

    files_fixed = 0
    total_links_fixed = 0

    print(f"[INFO] Starting scan and fix in folder: {root_dir}")

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if any(file.endswith(ext) for ext in markdown_exts):
                filepath = os.path.join(subdir, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                matches = list(md_link_pattern.finditer(content))
                if not matches:
                    continue

                new_content = content
                fixed_this_file = False

                for match in reversed(matches):
                    full_match = match.group(0)
                    link_text = match.group(1)
                    url = match.group(2)

                    if ' ' in url:
                        fixed_url = url.replace(' ', '')
                        fixed_link = f"{link_text}({fixed_url})"
                        start, end = match.span()
                        # Replace in new_content using slice to avoid messing offsets
                        new_content = new_content[:start] + fixed_link + new_content[end:]
                        print(f"[FIX] In file: {filepath}")
                        print(f"       Original URL: {url}")
                        print(f"       Fixed URL:    {fixed_url}\n")
                        fixed_this_file = True
                        total_links_fixed += 1

                if fixed_this_file:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    files_fixed += 1

    print(f"\n[SUMMARY] Files fixed: {files_fixed}")
    print(f"[SUMMARY] Total links fixed: {total_links_fixed}")
    if files_fixed == 0:
        print("[SUMMARY] No markdown links with spaces in URLs were found.")

if __name__ == "__main__":
    content_folder = 'content/posts'
    fix_markdown_links_with_spaces(content_folder)
