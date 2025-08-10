import os
import re

def fix_invalid_list_in_file(filepath):
    """
    Finds and fixes a common two-line list error in Hugo front matter
    for 'categories' and 'tags'.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            original_content = content
    except Exception as e:
        print(f"ERROR: Could not read file {filepath}: {e}")
        return

    # This regex is the key. It looks for the specific broken pattern:
    # A key ('categories' or 'tags'), followed by text on the same line,
    # followed by a newline, followed by a list item on the next line.
    # It uses re.MULTILINE so '^' matches the start of each line.
    pattern = re.compile(
        r"^(categories|tags):\s*(.*?)\r?\n(\s*-\s+.*)",
        re.MULTILINE
    )

    # The replacement function defines the correct structure.
    # \1 = the key ('categories' or 'tags')
    # \2 = the text from the first line ('Guide')
    # \3 = the full second line ('- Soundbars')
    replacement = r"\1:\n- \2\n\3"

    # Use re.subn to replace the pattern and get the count of substitutions.
    new_content, num_subs = pattern.subn(replacement, content)

    if num_subs > 0:
        print(f"  [FIX FOUND] in {os.path.basename(filepath)}. Correcting invalid list format.")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"SUCCESS: Corrected and saved {filepath}")
        except Exception as e:
            print(f"ERROR: Could not write to file {filepath}: {e}")

def process_all_files(folder):
    """Processes all markdown files in the specified folder."""
    print(f"--- Starting YAML List Fixer in: {folder} ---")
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fix_invalid_list_in_file(filepath)
    print("\n--- Process complete. ---")

if __name__ == "__main__":
    # CRITICAL: Please back up your content folder before running.
    content_folder = "content/posts"
    process_all_files(content_folder)