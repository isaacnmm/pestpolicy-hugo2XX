import os

def fix_nested_list_in_file(filepath):
    """
    Finds and corrects improperly nested list items (e.g., '- - item')
    in Hugo front matter by processing the file as raw text.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"ERROR: Could not read file {filepath}: {e}")
        return

    was_modified = False
    new_lines = []

    for line in lines:
        # Strip leading whitespace to consistently check the start of the text
        stripped_line = line.lstrip()
        
        # The specific pattern is a line starting with a double dash list item.
        if stripped_line.startswith('- -'):
            # This is the corrected logic: replace the first instance of '- ' with nothing.
            # The '1' is crucial to ensure we only replace the outer list marker, not any other hyphens.
            modified_line = line.replace('- ', '', 1)
            new_lines.append(modified_line)
            was_modified = True
        else:
            new_lines.append(line)

    if was_modified:
        # We only print the message if a fix was actually applied
        print(f"  [FIX FOUND] in {os.path.basename(filepath)}. Flattening nested list item(s).")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"SUCCESS: Corrected and saved {filepath}")
        except Exception as e:
            print(f"ERROR: Could not write to file {filepath}: {e}")

def process_all_files(folder):
    """Processes all markdown files in the specified folder."""
    print(f"--- Starting YAML Nested List Fixer in: {folder} ---")
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fix_nested_list_in_file(filepath)
    print("\n--- Process complete. ---")

if __name__ == "__main__":
    # CRITICAL: Please back up your content folder before running.
    content_folder = "content/posts"
    process_all_files(content_folder)