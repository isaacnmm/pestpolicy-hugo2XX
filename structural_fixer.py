import os

def fix_structural_error_in_file(filepath):
    """
    Finds and fixes a specific two-line structural error in Hugo front matter
    where a description is followed by an invalid continuation line.
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
    
    while i < len(lines):
        current_line = lines[i]
        
        # Check if we are at the last line to prevent index error
        if i + 1 < len(lines):
            next_line = lines[i+1]
            
            # THE CORE LOGIC: Check for the specific two-line error pattern
            if current_line.lstrip().startswith('description:') and next_line.lstrip().startswith('- '):
                
                # Get the text from the invalid line, stripping the "- " and any newline characters
                continuation_text = next_line.lstrip()[2:].strip()
                
                # Combine the lines
                # rstrip() removes the newline from the description line before merging
                merged_line = current_line.rstrip() + ' ' + continuation_text + '\n'
                
                new_lines.append(merged_line)
                
                print(f"  [FIX FOUND] in {os.path.basename(filepath)}. Merging two lines.")
                was_modified = True
                
                # Skip the next line because we've already processed it
                i += 2
                continue
        
        # If the pattern is not found, just add the current line and move to the next
        new_lines.append(current_line)
        i += 1

    # If we made a change, write the new, corrected content back to the file.
    if was_modified:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"SUCCESS: Corrected and saved {filepath}")
        except Exception as e:
            print(f"ERROR: Could not write to file {filepath}: {e}")

def process_all_files(folder):
    """Processes all markdown files in the specified folder."""
    print(f"--- Starting Structural Front Matter Fixer in: {folder} ---")
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                fix_structural_error_in_file(filepath)
    print("\n--- Process complete. ---")

if __name__ == "__main__":
    # CRITICAL: Please back up your content folder before running this script.
    content_folder = "content/posts"
    process_all_files(content_folder)