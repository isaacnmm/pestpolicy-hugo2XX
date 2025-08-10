import os
import re
import yaml

def clean_front_matter(raw_front_matter):
    """
    Parses YAML front matter, cleans it, and returns a standardized string.
    """
    try:
        # Load the YAML content from the raw string
        data = yaml.safe_load(raw_front_matter)
    except Exception as e:
        # If there's an error loading the YAML, return it as-is to avoid data loss
        print(f"YAML load error: {e}")
        return raw_front_matter.strip()
    
    # Ensure the loaded data is a dictionary (standard for front matter)
    if not isinstance(data, dict):
        return raw_front_matter.strip()
    
    # Dump the data back into a string with standardized formatting
    # sort_keys=False preserves the original order of keys
    dumped = yaml.dump(data, sort_keys=False, default_flow_style=False)

    # Specific fix: Ensure list items are not indented before the dash
    fixed_lines = []
    for line in dumped.splitlines():
        if line.lstrip().startswith('- '):
            # Remove all indentation before the dash, placing it at the start of the line
            fixed_lines.append('-' + line.lstrip()[1:])
        else:
            fixed_lines.append(line)
            
    return '\n'.join(fixed_lines).strip()

def process_markdown_file(filepath):
    """
    Reads a Markdown file, cleans its front matter, and writes it back if changed.
    """
    try:
        # Use 'utf-8' encoding which is standard and handles various characters
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return

    # Regex to capture the front matter block at the very start of the file
    # It matches a block starting and ending with '---' on its own line
    fm_match = re.match(r'^---\s*\n(.*?)(\n---\s*\n|\n---\s*$)', content, re.DOTALL)
    
    if not fm_match:
        print(f"No front matter found in: {filepath}")
        return

    # Extract the front matter and the rest of the content
    front_matter_content = fm_match.group(1)
    rest_of_content = content[fm_match.end():]

    # Get the cleaned and standardized front matter
    cleaned_fm = clean_front_matter(front_matter_content)

    # Rebuild the file content with the cleaned front matter
    new_content = f"---\n{cleaned_fm}\n---\n{rest_of_content.lstrip()}"

    # Only write to the file if changes were actually made
    if content != new_content:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Cleaned front matter in: {filepath}")
        except Exception as e:
            print(f"Error writing to file {filepath}: {e}")
    else:
        print(f"No change needed: {filepath}")

def process_folder(folder):
    """
    Recursively finds all .md files in a folder and processes them.
    """
    print(f"Processing folder: {folder}")
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                process_markdown_file(filepath)

if __name__ == "__main__":
    # Set this to the directory containing your Markdown posts
    content_folder = "content/posts"
    process_folder(content_folder)
    print("\nFront matter cleaning process complete.")