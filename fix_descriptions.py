import os
import re
from ruamel.yaml import YAML

def fix_description_in_file(filepath):
    """
    Reads a markdown file, checks for and fixes a common syntax error
    in the 'description' field of the front matter, and saves the file back.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return

    # Use regex to safely isolate the front matter block
    fm_match = re.match(r'^(---)\s*\n(.*?)(\n---\s*(\n|$))', content, re.DOTALL)
    if not fm_match:
        # No front matter found, nothing to do
        return

    front_matter_string = fm_match.group(2)
    original_front_matter_with_delimiters = fm_match.group(0)
    
    yaml = YAML()
    yaml.preserve_quotes = True
    
    try:
        data = yaml.load(front_matter_string)
    except Exception as e:
        print(f"Could not parse YAML in {filepath}: {e}")
        return

    if 'description' in data and isinstance(data['description'], str):
        original_desc = data['description']
        
        # The common error pattern is a sentence ending, a hyphen, and an incomplete thought.
        # e.g., "With a newborn baby, it is almost impossible to rest easy. - But..."
        if ' - ' in original_desc:
            # Fix the string by taking only the part before the hyphen pattern
            cleaned_desc = original_desc.split(' - ')[0]
            
            # Often, this leaves a trailing period or other punctuation, which is good.
            # If not, you might want to add an ellipsis, but this is safer.
            data['description'] = cleaned_desc
            
            # --- Rebuild the file ---
            from io import StringIO
            string_stream = StringIO()
            yaml.dump(data, string_stream)
            new_front_matter_string = string_stream.getvalue()
            
            # Reconstruct the full file with the cleaned front matter
            new_content = content.replace(front_matter_string, new_front_matter_string, 1)

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"FIXED description in: {filepath}")
            # No 'else' needed, if no change, we do nothing.

    # If 'description' doesn't exist or doesn't have the error, the file is left untouched.

def process_all_markdown_files(folder):
    """Walks through a folder and processes all .md files."""
    print(f"--- Scanning for description errors in: {folder} ---")
    fixed_count = 0
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fix_description_in_file(filepath)
    print("\n--- Scan complete. ---")


if __name__ == "__main__":
    # IMPORTANT: Before running, please back up your content folder!
    content_folder = "content/posts"
    process_all_markdown_files(content_folder)