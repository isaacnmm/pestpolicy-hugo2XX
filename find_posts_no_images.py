import os

# --- CONFIGURATION ---
# The root folder where your post bundles are located.
POSTS_ROOT = r"C:\My Hugo Sites\pestpolicy-hugo2XX\content\posts"

# Common image file extensions to look for.
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg'}

def find_folders_without_images():
    """
    Scans all subfolders in the posts directory and lists those
    that do not contain any files with common image extensions.
    """
    print(f"--- Scanning for Posts with No Images in: '{POSTS_ROOT}' ---")

    # Check if the posts directory exists
    if not os.path.isdir(POSTS_ROOT):
        print(f"\nERROR: Posts directory not found at the specified path.")
        return

    folders_without_images = []
    total_folders_scanned = 0

    # Get a list of all subdirectories in the posts root
    try:
        post_subfolders = [f for f in os.listdir(POSTS_ROOT) if os.path.isdir(os.path.join(POSTS_ROOT, f))]
    except FileNotFoundError:
        print(f"ERROR: Cannot access posts folder. Check permissions and path.")
        return

    for folder_name in post_subfolders:
        total_folders_scanned += 1
        post_folder_path = os.path.join(POSTS_ROOT, folder_name)
        
        found_image = False
        
        # Walk through all files in the current post folder
        try:
            for item in os.listdir(post_folder_path):
                # Check if the item is a file and its extension is in our list
                if os.path.isfile(os.path.join(post_folder_path, item)):
                    file_ext = os.path.splitext(item)[1].lower()
                    if file_ext in IMAGE_EXTENSIONS:
                        found_image = True
                        break # Found an image, no need to check further in this folder
            
            # If after checking all files, no image was found, add it to our list
            if not found_image:
                folders_without_images.append(post_folder_path)

        except Exception as e:
            print(f"  [WARN] Could not process folder '{folder_name}'. Reason: {e}")

    # --- Print the results ---
    print("\n--- Scan Complete ---")
    if folders_without_images:
        print(f"Found {len(folders_without_images)} post folder(s) with no images:\n")
        # Sort the list alphabetically for easier reading
        folders_without_images.sort()
        for folder_path in folders_without_images:
            print(folder_path)
    else:
        print("Success! All post folders contain at least one image.")
        
    print(f"\nScanned a total of {total_folders_scanned} post folder(s).")


if __name__ == "__main__":
    find_folders_without_images()