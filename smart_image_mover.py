import os
import shutil

# --- CONFIGURATION ---
PROJECT_ROOT = r"C:\My Hugo Sites\pestpolicy-hugo2XX"
SOURCE_IMAGES_ROOT = os.path.join(PROJECT_ROOT, "static", "images")
DEST_POSTS_ROOT = os.path.join(PROJECT_ROOT, "content", "posts")

# --- SAFETY SWITCH ---
# ALWAYS run with True first to review the plan!
DRY_RUN = True

def create_slug_from_filename(filename):
    """Converts an image filename into a Hugo-like slug for matching."""
    # Remove the file extension (e.g., .jpg, .png)
    name_without_ext = os.path.splitext(filename)[0]
    # Convert to lowercase
    slug = name_without_ext.lower()
    # Replace spaces and underscores with hyphens
    slug = re.sub(r'[\s_]+', '-', slug)
    # Remove any other non-alphanumeric characters (except hyphens)
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    return slug.strip('-')

def smart_move_images():
    """
    Moves images by matching the image filename (converted to a slug)
    with the destination post folder name.
    """
    print("--- Starting Smart Image Mover Script ---")
    if DRY_RUN:
        print("--- RUNNING IN DRY RUN MODE. NO FILES WILL BE MOVED. ---")

    # --- Step 1: Get a list of all valid destination post folder names ---
    try:
        dest_post_folders = {name for name in os.listdir(DEST_POSTS_ROOT)
                             if os.path.isdir(os.path.join(DEST_POSTS_ROOT, name))}
        if not dest_post_folders:
            print(f"ERROR: No post folders found in '{DEST_POSTS_ROOT}'. Cannot proceed.")
            return
    except FileNotFoundError:
        print(f"ERROR: Destination posts directory not found at: '{DEST_POSTS_ROOT}'")
        return

    print(f"Found {len(dest_post_folders)} potential destination post folders.")

    moved_files_count = 0
    unmatched_files_count = 0

    # --- Step 2: Iterate through the generic source folders (e.g., '03', '04') ---
    try:
        source_subfolders = [f for f in os.listdir(SOURCE_IMAGES_ROOT) if os.path.isdir(os.path.join(SOURCE_IMAGES_ROOT, f))]
    except FileNotFoundError:
        print(f"ERROR: Source images directory not found at: '{SOURCE_IMAGES_ROOT}'")
        return

    for generic_folder in source_subfolders:
        source_folder_path = os.path.join(SOURCE_IMAGES_ROOT, generic_folder)
        print(f"\nProcessing source folder: '{generic_folder}'")
        
        images_in_folder = [f for f in os.listdir(source_folder_path) if os.path.isfile(os.path.join(source_folder_path, f))]

        if not images_in_folder:
            print("  - No image files found in this source folder.")
            continue

        # --- Step 3: Match each image to a destination folder ---
        for image_name in images_in_folder:
            # Create a potential slug from the image filename
            image_slug = create_slug_from_filename(image_name)

            # Check if this slug matches any of our known post folders
            if image_slug in dest_post_folders:
                dest_folder_path = os.path.join(DEST_POSTS_ROOT, image_slug)
                source_image_path = os.path.join(source_folder_path, image_name)
                dest_image_path = os.path.join(dest_folder_path, image_name)
                
                print(f"  [MATCH] Image '{image_name}' matches post folder '{image_slug}'.")

                if os.path.exists(dest_image_path):
                    print(f"    [WARN] Skipping. File already exists in destination.")
                    continue

                # --- The Move Operation ---
                print(f"    -> Planning to move to '{dest_folder_path}'")
                if not DRY_RUN:
                    try:
                        shutil.move(source_image_path, dest_image_path)
                        moved_files_count += 1
                    except Exception as e:
                        print(f"    [ERROR] Failed to move. Reason: {e}")
            else:
                print(f"  [NO MATCH] Could not find a matching post folder for image '{image_name}' (slug: '{image_slug}')")
                unmatched_files_count += 1

    print("\n--- Script Complete ---")
    if DRY_RUN:
        print("Dry run finished. Review the plan above. To move files, set DRY_RUN = False and run again.")
    else:
        print(f"Successfully moved {moved_files_count} file(s).")
        if unmatched_files_count > 0:
            print(f"Could not find a match for {unmatched_files_count} file(s).")

# We need the 're' module for this script
import re

if __name__ == "__main__":
    smart_move_images()