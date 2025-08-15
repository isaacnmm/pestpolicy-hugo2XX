import os
import glob

# Path to your posts folder
POSTS_DIR = r"C:\My Hugo Sites\pestpolicy-hugo2XX\content\posts"

# Find all .bak files recursively
bak_files = glob.glob(os.path.join(POSTS_DIR, "**", "*.bak"), recursive=True)

if not bak_files:
    print("No .bak files found.")
else:
    for file_path in bak_files:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

    print(f"\nDeleted {len(bak_files)} backup files.")
