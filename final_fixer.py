import os
import re
from ruamel.yaml import YAML
from io import StringIO

def fix_hugo_front_matter(filepath):
    """
    Reads a Hugo markdown file and fixes multiple common YAML front matter errors.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"ERROR: Cannot read file {filepath}: {e}")
        return

    original_content = content

    # Regex to capture the front matter block
    fm_match = re.match(r'^(---)\s*\r?\n(.*?)(\r?\n---\s*(\r?\n|$))', content, re.DOTALL)
    if not fm_match:
        return # No front matter found, nothing to fix.

    front_matter_string = fm_match.group(2)
    
    # --- Pre-processing for structurally fatal errors ---
    # Fix for rogue list items that break the parser
    # This turns "- some text" into "description: some text" if description doesn't exist
    # or appends it if it does. This is a common error pattern.
    lines = front_matter_string.splitlines()
    cleaned_lines = []
    description_index = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('description:'):
            description_index = i
        # A rogue list item is a line starting with '-' not preceded by a list key
        if line.strip().startswith('-') and not lines[i-1].strip().endswith(':'):
             if 'categories:' not in lines[i-1] and 'tags:' not in lines[i-1]:
                rogue_text = line.strip()[1:].strip()
                if description_index != -1:
                    lines[description_index] += f" {rogue_text}"
                    print(f"  [FIX] Merged rogue line into description in {os.path.basename(filepath)}")
                # Do not add the rogue line to cleaned_lines
                continue
        cleaned_lines.append(line)
    
    processed_front_matter = "\n".join(cleaned_lines)
    
    # --- Load into YAML parser ---
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 4096 # Prevent line wrapping

    try:
        data = yaml.load(processed_front_matter)
    except Exception as e:
        print(f"ERROR: Could not parse YAML in {filepath} after cleaning. Please fix manually. Reason: {e}")
        return

    was_modified = False

    # --- Post-processing for content errors ---
    if data and 'description' in data and isinstance(data['description'], str):
        original_desc = data['description']
        # Fix for " - " pattern within the description
        if ' - ' in original_desc:
            # Replace with a space, preserving text, as requested
            data['description'] = original_desc.replace(' - ', ' ', 1)
            print(f"  [FIX] Cleaned hyphen in description for {os.path.basename(filepath)}")
            was_modified = True

    # Check for unquoted colons in title and description
    for key in ['title', 'description']:
        if data and key in data and isinstance(data[key], str):
            if ':' in data[key]:
                # ruamel.yaml will automatically quote this on dump if needed
                # We can force it for clarity if we want, but its default is smart.
                pass 

    if was_modified:
        string_stream = StringIO()
        yaml.dump(data, string_stream)
        new_front_matter_string = string_stream.getvalue()
        
        # Rebuild the entire file content
        new_content = original_content.replace(front_matter_string, new_front_matter_string.strip())

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"SUCCESS: Fixed and saved {filepath}")
        except Exception as e:
            print(f"ERROR: Could not write to file {filepath}: {e}")

def process_all_files(folder):
    """Processes all markdown files in the specified folder."""
    print(f"--- Starting automated front matter fixing process in: {folder} ---")
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fix_hugo_front_matter(filepath)
    print("\n--- Process complete. ---")


if __name__ == "__main__":
    # IMPORTANT: ALWAYS BACK UP YOUR CONTENT FOLDER BEFORE RUNNING A SCRIPT LIKE THIS.
    content_folder = "content/posts"
    process_all_files(content_folder)