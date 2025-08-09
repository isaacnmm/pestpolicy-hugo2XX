import os

# Path to your Hugo content directory (adjust as needed)
content_dir = r"C:\My Hugo Sites\pestpolicy-hugo2XX\content\posts"

def clean_replacement_characters():
    replaced_any = False
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                if "�" in content:
                    new_content = content.replace("�", "")
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    print(f"Removed replacement characters in: {filepath}")
                    replaced_any = True

    if not replaced_any:
        print("No replacement characters found in any markdown files.")

if __name__ == "__main__":
    clean_replacement_characters()
