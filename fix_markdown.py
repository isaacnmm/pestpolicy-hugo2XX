import os
import re
from datetime import datetime

def fix_markdown_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove extra blank lines in front matter (between --- ... ---)
    frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        # Remove blank lines inside front matter
        frontmatter_fixed = "\n".join(line for line in frontmatter.splitlines() if line.strip() != "")
        content = content.replace(frontmatter, frontmatter_fixed)

    # 2. Fix URLs: remove all spaces inside URLs
    # Find URLs in the form http(s)://... or inside markdown links and remove spaces
    def url_space_fix(match):
        url = match.group(0)
        return url.replace(" ", "")
    content = re.sub(r'https?://[^\s)"]+', url_space_fix, content)

    # 3. Fix headings with extraneous '#'
    # Change headings like ## # Heading to ### Heading (remove redundant #)
    content = re.sub(r'^(#+) #+', lambda m: '#' * (len(m.group(1)) + 1) + ' ', content, flags=re.MULTILINE)

    # 4. Fix {{< pinnable src="...">}} to have src start with '/' and no domain or protocol, no spaces
    def fix_pinnable_src(match):
        src = match.group(1)
        # Remove protocol and domain
        src = re.sub(r'https?://[^/]+', '', src)
        # Remove spaces
        src = src.replace(" ", "")
        # Ensure src starts with '/'
        if not src.startswith('/'):
            src = '/' + src
        return '{{< pinnable src="{}" >}}'.format(src)
    content = re.sub(r'\{\{< pinnable src="([^"]+)" >\}\}', fix_pinnable_src, content)

    # Save fixed content back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_all_posts(root_folder):
    # Process all markdown files (*.md) inside root_folder recursively
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(subdir, file)
                print(f"Fixing: {filepath}")
                fix_markdown_file(filepath)

if __name__ == "__main__":
    posts_dir = r"C:\My Hugo Sites\pestpolicy-hugo2XX\content\posts"
    fix_all_posts(posts_dir)
