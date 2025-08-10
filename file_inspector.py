import os

def inspect_file_raw(filepath):
    """
    Reads the beginning of a file in binary mode and prints a hex dump
    to help diagnose structural or encoding issues.
    """
    print(f"--- Raw Inspector for: {filepath} ---\n")
    if not os.path.exists(filepath):
        print(f"ERROR: File not found at '{filepath}'")
        return

    try:
        with open(filepath, 'rb') as f:
            # Read the first 512 bytes, which should be enough to cover the front matter
            raw_bytes = f.read(512)
            
            print(" Offset | Hex                                             | Characters")
            print("--------|-------------------------------------------------|------------------")
            
            for i in range(0, len(raw_bytes), 16):
                chunk = raw_bytes[i:i+16]
                
                # Format the offset (e.g., 00000000)
                offset = f"{i:08x}"
                
                # Format the hex values (e.g., 48 65 6c 6c 6f)
                hex_part = ' '.join(f"{b:02x}" for b in chunk)
                
                # Format the character representation (replace non-printable with '.')
                char_part = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in chunk)
                
                print(f"{offset} | {hex_part:<47} | {char_part}")

    except Exception as e:
        print(f"ERROR: Could not read or process file: {e}")


if __name__ == "__main__":
    # --- IMPORTANT ---
    # We are only inspecting the ONE file that we know is broken.
    # Please ensure this path is correct.
    problem_file_path = "content/posts/best-rocking-chairs-for-nursery/index.md"
    
    inspect_file_raw(problem_file_path)