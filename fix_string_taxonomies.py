import os
import re
from ruamel.yaml import YAML
from io import StringIO

def fix_string_taxonomy_in_file(filepath):
    """
    Checks for 'categories' or 'tags' that are strings instead of lists
    and converts them to a list with a single item.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            original_content = content
    except Exception as e:
        print(f"ERROR: Could not read file {filepath}: {e}")
        return

    # Use regex to safely isolate the front matter block
    match = re.match(r'^(---.*?\n---\s*)', content, re.DOTALL)
    if not match:
        return # No front matter found

    front_matter_block = match.group(0)
    front_matter_string = match.group(1).strip().split('\n', 1)[1] # Get content between ---

    yaml = YAML()
    yaml.preserve_quotes = True
    
    try:
        data = yaml.load(front_matter_string)
    except Exception as e:
        # If there's a syntax error, we can't process it.
        # The user should run the other fixer scripts first.
        return
        
    was_modified = False
    
    # Check both 'categories' and 'tags'
    for key in ['categories', 'tags']:
        if key in data and isinstance(data[key], str):
            print(f"  [FIX FOUND] in {os.path.basename(filepath)}. Converting '{key}' from string to list.")
            
            # Convert the string to a list containing that string
            string_value = data[key]
            data[key] = [string_value]
            was_modified = True

    if was_modified:
        string_stream = StringIO()
        yaml.dump(data, string_stream)
        new_front_matter_content = string_stream.getvalue()

        # Rebuild the file content
        new_content = f"---\n{new_front_matter_content}---\n" + content[len(front_matter_block):]
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"SUCCESS: Corrected and saved {filepath}")
        except Exception as e:
            print(f"ERROR: Could not write to file {filepath}: {e}")


def process_all_files(folder):
    """Processes all markdown files in the specified folder."""
    print(f"--- Starting YAML Taxonomy String Fixer in: {folder} ---")
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fix_string_taxonomy_in_file(filepath)
    print("\n--- Process complete. ---")

if __name__ == "__main__":
    # CRITICAL: Please back up your content folder before running.
    content_folder = "content/posts"
    process_all_files(content_folder)