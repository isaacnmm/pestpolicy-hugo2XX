import os

def remove_blank_lines_in_frontmatter(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    in_frontmatter = False
    frontmatter_lines = []

    for line in lines:
        if line.strip() == '---':
            if not in_frontmatter:
                # Start frontmatter
                in_frontmatter = True
                new_lines.append(line)  # add starting ---
                frontmatter_lines = []
            else:
                # End frontmatter
                in_frontmatter = False
                # Add frontmatter lines WITHOUT blank lines
                for fm_line in frontmatter_lines:
                    if fm_line.strip() != '':
                        new_lines.append(fm_line)
                new_lines.append(line)  # add ending ---
        else:
            if in_frontmatter:
                frontmatter_lines.append(line)
            else:
                new_lines.append(line)

    # Write back only if changed
    new_content = ''.join(new_lines)
    original_content = ''.join(lines)
    if new_content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated frontmatter in: {filepath}")

def process_all_markdown_files(root_folder='content/posts'):
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(subdir, file)
                remove_blank_lines_in_frontmatter(full_path)

if __name__ == "__main__":
    process_all_markdown_files()
