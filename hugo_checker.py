import os
import subprocess
import toml
import yaml
import shutil

# --- CONFIGURATION ---
# This script assumes it's in the root of your Hugo project.
# If you place it elsewhere, change this path.
HUGO_SITE_PATH = "." 
CONTENT_DIR = "content"
# --- END CONFIGURATION ---

# Simple colors for output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(message):
    print(f"\n{bcolors.HEADER}=== {message} ==={bcolors.ENDC}")

def check_hugo_executable():
    """Checks if the 'hugo' command is available in the system's PATH."""
    print_header("Checking for Hugo Executable")
    try:
        # Use 'hugo version' as a simple, non-intrusive check
        result = subprocess.run(['hugo', 'version'], capture_output=True, text=True, check=True)
        print(f"{bcolors.OKGREEN}[SUCCESS]{bcolors.ENDC} Hugo found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC} Hugo command not found.")
        print(f"{bcolors.WARNING}Please ensure Hugo is installed and that its directory is in your system's PATH.{bcolors.ENDC}")
        return False

def validate_front_matter():
    """Walks through the content directory and validates the front matter of each .md file."""
    print_header("Validating Front Matter in all .md files")
    error_found = False
    content_path = os.path.join(HUGO_SITE_PATH, CONTENT_DIR)

    for root, _, files in os.walk(content_path):
        for file in files:
            if file.endswith('.md') or file.endswith('.markdown'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                    
                    # Check for front matter delimiters
                    if content.startswith('---'):
                        parts = content.split('---', 2)
                        if len(parts) >= 3:
                            front_matter = parts[1]
                            yaml.safe_load(front_matter) # This will raise an error if YAML is invalid
                        else:
                            raise ValueError("Invalid YAML front matter structure (missing closing '---')")
                    
                    # Note: Hugo also supports TOML with '+++', but YAML is more common.
                    # Add TOML check if you use it.
                    
                except Exception as e:
                    print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC} Invalid front matter in file: {bcolors.WARNING}{filepath}{bcolors.ENDC}")
                    print(f"  └─ Details: {e}")
                    error_found = True

    if not error_found:
        print(f"{bcolors.OKGREEN}[SUCCESS]{bcolors.ENDC} All front matter files parsed successfully.")
    else:
         print(f"\n{bcolors.WARNING}Tip: A common error is a missing colon, like `slug /path/` instead of `slug: /path/`. Check the files above carefully.{bcolors.ENDC}")
    return not error_found

def run_hugo_build():
    """Runs the 'hugo' command to build the site and captures output."""
    print_header("Attempting Local Hugo Build")
    print(f"This will simulate what your build server does. Building in: {os.path.abspath(HUGO_SITE_PATH)}")
    
    # Clean the public directory first for a fresh build
    public_dir = os.path.join(HUGO_SITE_PATH, 'public')
    if os.path.exists(public_dir):
        print(f"{bcolors.OKCYAN}[INFO]{bcolors.ENDC} Deleting existing 'public' directory for a clean build.")
        shutil.rmtree(public_dir)
        
    try:
        # Run the hugo command
        result = subprocess.run(
            ['hugo'], 
            capture_output=True, 
            text=True, 
            check=True,
            cwd=HUGO_SITE_PATH
        )
        print(f"{bcolors.OKGREEN}[SUCCESS]{bcolors.ENDC} Hugo build completed successfully!")
        print("--- Hugo Output ---")
        print(result.stdout)
        print("-------------------")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{bcolors.FAIL}[ERROR]{bcolors.ENDC} Hugo build failed!")
        print(f"{bcolors.BOLD}This is the critical error message your build server is likely seeing:{bcolors.ENDC}")
        print("--- Hugo Error Output ---")
        print(bcolors.FAIL + e.stderr + bcolors.ENDC)
        print("-----------------------")
        return False

def main():
    """Main function to run all checks."""
    print(f"{bcolors.BOLD}--- Starting Hugo Site Pre-flight Check ---{bcolors.ENDC}")
    
    if not check_hugo_executable():
        return # Stop if Hugo isn't installed

    if not validate_front_matter():
        print(f"\n{bcolors.FAIL}Front matter errors detected. Halting before build attempt.{bcolors.ENDC}")
        print("Please fix the errors listed above and run the script again.")
        return # Stop if front matter is broken

    if not run_hugo_build():
        print(f"\n{bcolors.FAIL}Build failed. Please review the Hugo error message above to diagnose the issue.{bcolors.ENDC}")
        print("Common causes include broken shortcodes, invalid config settings, or missing theme components.")
    else:
        print(f"\n{bcolors.OKGREEN}{bcolors.BOLD}✅ Pre-flight check complete. Your site builds successfully on your local machine.{bcolors.ENDC}")
        print("If Netlify is still failing, the issue is likely in the Netlify-specific build environment (e.g., Hugo version, Node version, private theme access).")

if __name__ == "__main__":
    main()