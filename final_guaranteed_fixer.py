import os
import re

def fix_multiline_description_error(filepath):
    """
    Reads a file's raw content and uses a regular expression to fix a specific
    multi-line structural error in the front matter.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            original_content = content
    except Exception as e:
        print(f"ERROR: Could not read file {filepath}: {e}")
        return

    # This regex is the key. It looks for the multi-line error pattern.
    # It finds 'description:' and captures its value (Group 1).
    # It then finds a newline (\r?\n) followed by a line starting with a hyphen (Group 2).
    # re.DOTALL allows '.' to match newlines.
    pattern = re.compile(
        r"(description:.*?)\r?\n(\s*-\s+.*)",
        re.DOTALL
    )

    # We perform the substitution on the entire file content at once.
    # The replacement function `repl` will correctly merge the lines.
    def repl(match):
        # Group 1 is the 'description: ...' part.
        # Group 2 is the '- But...' part, including leading whitespace.
        
        # We clean group 2 by stripping whitespace and the leading dash.
        continuation_text = match.group(2).strip()[1:].strip()
        
        # We merge them with a space.
        return f"{match.group(1).strip()} {continuation_text}"

    # Use re.sub to find and replace the pattern.
    new_content, num_subs = pattern.subn(repl, content, count=1)

    if num_subs > 0:
        print(f"  [FIX FOUND] in {os.path.basename(filepath)}. Correcting multi-line description.")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"SUCCESS: Corrected and saved {filepath}")
        except Exception as e:
            print(f"ERROR: Could not write to file {filepath}: {e}")

def process_all_files(folder):
    """Processes all markdown files in the specified folder."""
    print(f"--- Starting Final Structural Fixer in: {folder} ---")
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fix_multiline_description_error(filepath)
    print("\n--- Process complete. ---")

if __name__ == "__main__":
    # CRITICAL: Please back up your content folder before running.
    content_folder = "content/posts"
    process_all_files(content_folder)