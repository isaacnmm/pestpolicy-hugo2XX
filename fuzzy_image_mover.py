import os
import shutil
import re

# --- CONFIGURATION ---
PROJECT_ROOT = r"C:\My Hugo Sites\pestpolicy-hugo2XX"
SOURCE_IMAGES_ROOT = os.path.join(PROJECT_ROOT, "static", "images")
DEST_POSTS_ROOT = os.path.join(PROJECT_ROOT, "content", "posts")

# List of generic filenames to ignore completely
GENERIC_FILENAMES_TO_IGNORE = ['pest-control', 'home-improvement', 'product-reviews', 'default-image']

# --- SAFETY SWITCH ---
DRY_RUN = False

def create_slug_from_filename(filename):
    """Converts an image filename into a Hugo-like slug for matching."""
    name_without_ext = os.path.splitext(filename)[0]
    slug = name_without_ext.lower()
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    return slug.strip('-')

def fuzzy_move_images():
    """
    Moves images using a "fuzzy" matching logic to find the best-fit post folder,
    renaming images for a perfect match if necessary.
    """
    print("--- Starting Fuzzy Image Mover Script ---")
    if DRY_RUN:
        print("--- RUNNING IN DRY RUN MODE. NO FILES WILL BE MODIFIED. ---")

    try:
        dest_post_folders = {name for name in os.listdir(DEST_POSTS_ROOT)
                             if os.path.isdir(os.path.join(DEST_POSTS_ROOT, name))}
    except FileNotFoundError:
        print(f"ERROR: Destination posts directory not found at: '{DEST_POSTS_ROOT}'")
        return

    print(f"Found {len(dest_post_folders)} potential destination post folders.")
    moved_files_count = 0
    unmatched_files_count = 0

    try:
        source_subfolders = [f for f in os.listdir(SOURCE_IMAGES_ROOT) if os.path.isdir(os.path.join(SOURCE_IMAGES_ROOT, f))]
    except FileNotFoundError:
        print(f"ERROR: Source images directory not found at: '{SOURCE_IMAGES_ROOT}'")
        return

    for generic_folder in source_subfolders:
        source_folder_path = os.path.join(SOURCE_IMAGES_ROOT, generic_folder)
        print(f"\nProcessing source folder: '{generic_folder}'")
        
        images_in_folder = [f for f in os.listdir(source_folder_path) if os.path.isfile(os.path.join(source_folder_path, f))]

        for image_name in images_in_folder:
            original_slug = create_slug_from_filename(image_name)

            if any(generic in original_slug for generic in GENERIC_FILENAMES_TO_IGNORE):
                print(f"  [IGNORE] Skipping generic image '{image_name}'")
                continue

            best_match_folder = None
            
            # --- The Fuzzy Matching Logic ---
            if original_slug in dest_post_folders:
                best_match_folder = original_slug # Perfect match
            else:
                # Try simplifying the slug to find a match
                simplified_slug = original_slug
                # Remove common WordPress suffixes like -1, -1-1, etc.
                simplified_slug = re.sub(r'-\d+-\d+$', '', simplified_slug)
                simplified_slug = re.sub(r'-\d+$', '', simplified_slug)
                # Remove common WordPress edit suffixes like -e1234567890
                simplified_slug = re.sub(r'-e\d+$', '', simplified_slug)

                if simplified_slug in dest_post_folders:
                    best_match_folder = simplified_slug # Found a close enough match
            
            # --- The Action ---
            if best_match_folder:
                dest_folder_path = os.path.join(DEST_POSTS_ROOT, best_match_folder)
                source_image_path = os.path.join(source_folder_path, image_name)

                # NEW: We will rename the image to match the folder for consistency
                file_extension = os.path.splitext(image_name)[1]
                new_image_name = f"{best_match_folder}{file_extension}"
                dest_image_path = os.path.join(dest_folder_path, new_image_name)

                print(f"  [MATCH] Image '{image_name}' matches post folder '{best_match_folder}'.")
                
                if image_name.lower() != new_image_name.lower():
                    print(f"    -> Planning to RENAME to '{new_image_name}'")

                if os.path.exists(dest_image_path):
                    print(f"    [WARN] Skipping. File '{new_image_name}' already exists in destination.")
                    continue

                print(f"    -> Planning to MOVE to '{dest_folder_path}'")
                if not DRY_RUN:
                    try:
                        shutil.move(source_image_path, dest_image_path)
                        moved_files_count += 1
                    except Exception as e:
                        print(f"    [ERROR] Failed to move. Reason: {e}")
            else:
                print(f"  [NO MATCH] Could not find a match for image '{image_name}'")
                unmatched_files_count += 1

    print("\n--- Script Complete ---")
    if DRY_RUN:
        print("Dry run finished. Review the plan above. To move/rename files, set DRY_RUN = False and run again.")
    else:
        print(f"Successfully moved and/or renamed {moved_files_count} file(s).")
        if unmatched_files_count > 0:
            print(f"Could not find a match for {unmatched_files_count} file(s).")

if __name__ == "__main__":
    fuzzy_move_images()