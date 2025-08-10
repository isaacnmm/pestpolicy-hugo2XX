import os
import re

def fix_structural_error_robustly(filepath):
    """
    Finds and fixes a specific two-line structural error using regular expressions
    to handle variations in dashes and whitespace.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"ERROR: Could not read file {filepath}: {e}")
        return

    was_modified = False
    new_lines = []
    i = 0
    
    # This regex pattern matches:
    # ^        - start of the line
    # \s*      - zero or more whitespace characters
    # [-–—]    - ANY of the three common dash types (hyphen, en-dash, em-dash)
    # \s+      - one or more whitespace characters
    pattern = re.compile(r"^\s*[-–—]\s+")

    while i < len(lines):
        current_line = lines[i]
        
        if i + 1 < len(lines):
            next_line = lines[i+1]
            
            # Use the robust regex to check the next line
            if current_line.lstrip().startswith('description:') and pattern.match(next_line):
                
                # Strip the newline from the description line
                desc_line = current_line.rstrip()
                
                # Use the pattern to remove the dash/space prefix from the continuation line
                continuation_text = pattern.sub('', next_line).strip()
                
                # Create the newly merged line with a newline at the end
                merged_line = f"{desc_line} {continuation_text}\n"
                
                new_lines.append(merged_line)
                
                print(f"  [FIX FOUND] in {os.path.basename(filepath)}. Merging two lines.")
                was_modified = True
                
                # Crucially, skip the next line as it has been merged
                i += 2
                continue
        
        # If the pattern wasn't found, add the line as is and move on
        new_lines.append(current_line)
        i += 1

    if was_modified:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"SUCCESS: Corrected and saved {filepath}")
        except Exception as e:
            print(f"ERROR: Could not write to file {filepath}: {e}")

def process_all_files(folder):
    """Processes all markdown files in the specified folder."""
    print(f"--- Starting Robust Structural Front Matter Fixer in: {folder} ---")
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fix_structural_error_robustly(filepath)
    print("\n--- Process complete. ---")

if __name__ == "__main__":
    # CRITICAL: Please back up your content folder before running this script.
    content_folder = "content/posts"
    process_all_files(content_folder)