def process_markdown_file(filepath):
    print(f"Processing file: {filepath}")  # debug
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    fm_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not fm_match:
        print(f"No front matter found in: {filepath}")
        return

    front_matter = fm_match.group(1)
    print(f"Original front matter:\n{front_matter}\n")  # debug

    cleaned_fm = clean_front_matter(front_matter)
    print(f"Cleaned front matter:\n{cleaned_fm}\n")  # debug

    new_content = f"---\n{cleaned_fm}\n---\n{content[fm_match.end():].lstrip()}"

    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Cleaned front matter in: {filepath}")
    else:
        print(f"No change needed: {filepath}")
