import os

def delete_bak_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".bak"):
                file_path = os.path.join(root, file)
                print(f"Deleting backup file: {file_path}")
                os.remove(file_path)

if __name__ == "__main__":
    base_dir = "./content"  # Adjust as needed
    delete_bak_files(base_dir)
