import os
import re

def fix_description_in_file(filepath):
    """
    Reads a file and fixes the common ' - ' error in the description field
    by operating on the raw text content.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"ERROR: Could not read file {filepath}: {e}")
        return

    # Use a flag to track if we need to save the file
    was_modified = False
    new_lines = []

    for line in lines:
        # We are looking for a very specific pattern: a line starting with 'description:'
        # that contains the problematic spaced hyphen.
        if line.lstrip().startswith('description:') and ' - ' in line:
            # Replace the first occurrence of ' - ' with a single space.
            # This correctly merges the text while fixing the YAML syntax error.
            modified_line = line.replace(' - ', ' ', 1)
            new_lines.append(modified_line)
            was_modified = True
            print(f"  [FIX FOUND] in {os.path.basename(filepath)}")
        else:
            new_lines.append(line)

    # If we made a change, write the new content back to the file.
    if was_modified:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"SUCCESS: Corrected and saved {filepath}")
        except Exception as e:
            print(f"ERROR: Could not write to file {filepath}: {e}")

def process_all_files(folder):
    """Processes all markdown files in the specified folder."""
    print(f"--- Starting Final Description Fixer in: {folder} ---")
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fix_description_in_file(filepath)
    print("\n--- Process complete. ---")


if __name__ == "__main__":
    # CRITICAL: Please back up your content folder before running this script.
    content_folder = "content/posts"
    process_all_files(content_folder)