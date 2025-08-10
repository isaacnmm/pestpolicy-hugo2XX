import os
import re

def fix_description_with_regex(filepath):
    """
    Reads a file and uses a regular expression to fix the common hyphen error
    in the description field of the front matter.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"ERROR: Could not read file {filepath}: {e}")
        return

    was_modified = False
    new_lines = []

    # This regex looks for a hyphen surrounded by one or more whitespace characters (\s+).
    # This is much more flexible than looking for a fixed ' - ' string.
    pattern = re.compile(r'\s+-\s+')

    for line in lines:
        # We only operate on lines that start with 'description:'
        if line.lstrip().startswith('description:'):
            # re.subn returns the modified string and the number of substitutions made.
            modified_line, num_subs = pattern.subn(' ', line, count=1)
            
            # If a substitution was made, we know we found the error.
            if num_subs > 0:
                new_lines.append(modified_line)
                was_modified = True
                print(f"  [FIX FOUND] in {os.path.basename(filepath)}")
            else:
                new_lines.append(line) # No error found, add the original line
        else:
            new_lines.append(line) # Not a description line, add it as-is

    # If the file was changed, write the new content back.
    if was_modified:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"SUCCESS: Corrected and saved {filepath}")
        except Exception as e:
            print(f"ERROR: Could not write to file {filepath}: {e}")

def process_all_files(folder):
    """Processes all markdown files in the specified folder."""
    print(f"--- Starting Regex Description Fixer in: {folder} ---")
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fix_description_with_regex(filepath)
    print("\n--- Process complete. ---")


if __name__ == "__main__":
    # CRITICAL: Please back up your content folder before running this script.
    content_folder = "content/posts"
    process_all_files(content_folder)