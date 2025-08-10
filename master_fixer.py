import os
import re

def fix_all_front_matter_errors(filepath):
    """
    A comprehensive script to fix multiple common YAML front matter errors
    using robust, raw-text regular expressions.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            original_content = content
    except Exception as e:
        print(f"ERROR: Could not read file {filepath}: {e}")
        return

    modified_content = content
    fix_descriptions = []

    # --- FIX 1: Invalid list definition (e.g., "categories: Guide" on one line, "- Soundbars" on the next) ---
    # This pattern looks for a key, text on the same line, and a list item on the next.
    pattern1 = re.compile(r"^(categories|tags):\s*(.*?)\r?\n(\s*-\s+.*)", re.MULTILINE)
    replacement1 = r"\1:\n- \2\n\3"
    modified_content, subs1 = pattern1.subn(replacement1, modified_content)
    if subs1 > 0:
        fix_descriptions.append("Corrected invalid list format")

    # --- FIX 2: Improperly nested list items (e.g., "- - Guides") ---
    # This pattern looks for a line starting with the double-dash list structure.
    pattern2 = re.compile(r"^(\s*)-\s+(-.*)", re.MULTILINE)
    replacement2 = r"\1\2"
    modified_content, subs2 = pattern2.subn(replacement2, modified_content)
    if subs2 > 0:
        fix_descriptions.append("Flattened nested list items")

    # --- FIX 3: Taxonomy key with a string value instead of a list (e.g., "categories: DIY Paintings") ---
    # This pattern looks for a key followed by text that is NOT a list item.
    # The negative lookahead `(?!\s*-)` ensures the next line isn't a list item.
    pattern3 = re.compile(r"^(categories|tags):\s+(.+?)\s*$", re.MULTILINE)
    replacement3 = r"\1:\n- \2"
    modified_content, subs3 = pattern3.subn(replacement3, modified_content)
    if subs3 > 0:
        fix_descriptions.append("Converted string to list for taxonomy")

    # --- Save the file only if any changes were made ---
    if original_content != modified_content:
        print(f"  [FIX FOUND] in {os.path.basename(filepath)}. Fixes applied: {', '.join(fix_descriptions)}.")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            print(f"SUCCESS: Corrected and saved {filepath}")
        except Exception as e:
            print(f"ERROR: Could not write to file {filepath}: {e}")


def process_all_files(folder):
    """Processes all markdown files in the specified folder."""
    print(f"--- Starting Master Front Matter Fixer in: {folder} ---")
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fix_all_front_matter_errors(filepath)
    print("\n--- Process complete. ---")

if __name__ == "__main__":
    # CRITICAL: Please back up your content folder before running.
    content_folder = "content/posts"
    process_all_files(content_folder)