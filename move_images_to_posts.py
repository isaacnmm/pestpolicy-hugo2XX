import os
import shutil

# --- CONFIGURATION ---
# The root of your Hugo project. We will build paths from here.
PROJECT_ROOT = r"C:\My Hugo Sites\pestpolicy-hugo2XX"

# The folder where images are CURRENTLY located.
SOURCE_IMAGES_ROOT = os.path.join(PROJECT_ROOT, "static", "images")

# The folder where your post bundles ARE LOCATED.
DEST_POSTS_ROOT = os.path.join(PROJECT_ROOT, "content", "posts")


# --- SAFETY SWITCH ---
# Set to True to only PRINT what the script would do without moving any files.
# Set to False to perform the actual file move operation.
# ALWAYS run with True first to review the plan!
DRY_RUN = True

def move_post_images():
    """
    Moves images from subfolders in the static/images directory to their
    corresponding post bundle folders in the content/posts directory.
    """
    print("--- Starting Image Mover Script ---")
    if DRY_RUN:
        print("--- RUNNING IN DRY RUN MODE. NO FILES WILL BE MOVED. ---")

    # Check if the source directory exists
    if not os.path.isdir(SOURCE_IMAGES_ROOT):
        print(f"\nERROR: Source images directory not found at:\n'{SOURCE_IMAGES_ROOT}'")
        return

    # Check if the destination directory exists
    if not os.path.isdir(DEST_POSTS_ROOT):
        print(f"\nERROR: Destination posts directory not found at:\n'{DEST_POSTS_ROOT}'")
        return

    moved_files_count = 0
    skipped_folders_count = 0
    
    # Get all the subfolders in the source images directory (e.g., 'my-first-post', 'another-post')
    try:
        source_subfolders = [f for f in os.listdir(SOURCE_IMAGES_ROOT) if os.path.isdir(os.path.join(SOURCE_IMAGES_ROOT, f))]
    except FileNotFoundError:
        print(f"ERROR: Cannot access source folder. Check permissions and path.")
        return

    for folder_name in source_subfolders:
        source_folder_path = os.path.join(SOURCE_IMAGES_ROOT, folder_name)
        # Construct the corresponding destination folder path
        dest_folder_path = os.path.join(DEST_POSTS_ROOT, folder_name)

        print(f"\nProcessing source folder: '{folder_name}'")

        # Check if the matching destination post folder exists
        if not os.path.isdir(dest_folder_path):
            print(f"  [SKIP] Destination post folder not found: '{dest_folder_path}'")
            skipped_folders_count += 1
            continue

        # Get a list of all files inside the source image subfolder
        images_to_move = [f for f in os.listdir(source_folder_path) if os.path.isfile(os.path.join(source_folder_path, f))]

        if not images_to_move:
            print("  - No image files found in this source folder.")
            continue

        for image_name in images_to_move:
            source_image_path = os.path.join(source_folder_path, image_name)
            dest_image_path = os.path.join(dest_folder_path, image_name)

            # Check if a file with the same name already exists in the destination
            if os.path.exists(dest_image_path):
                print(f"  [WARN] Skipping '{image_name}'. File already exists in destination.")
                continue

            # --- The Move Operation ---
            print(f"  -> Planning to move '{image_name}' to '{dest_folder_path}'")
            if not DRY_RUN:
                try:
                    shutil.move(source_image_path, dest_image_path)
                    moved_files_count += 1
                except Exception as e:
                    print(f"  [ERROR] Failed to move '{image_name}'. Reason: {e}")
        
        # Optional: Clean up empty source folder after moving
        if not DRY_RUN and not os.listdir(source_folder_path):
            print(f"  - Source folder '{folder_name}' is now empty. Deleting.")
            try:
                os.rmdir(source_folder_path)
            except Exception as e:
                    print(f"  [ERROR] Failed to delete empty source folder. Reason: {e}")


    print("\n--- Script Complete ---")
    if DRY_RUN:
        print("Dry run finished. Review the plan above. To move files, set DRY_RUN = False and run again.")
    else:
        print(f"Successfully moved {moved_files_count} file(s).")
        if skipped_folders_count > 0:
            print(f"Skipped {skipped_folders_count} folder(s) because no matching post folder was found.")

if __name__ == "__main__":
    # CRITICAL: Always back up your folders before performing file operations.
    move_post_images()