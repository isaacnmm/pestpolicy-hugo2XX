import os
import yaml
from datetime import datetime

CONTENT_DIR = "content"  # Hugo content directory

def check_date_format(date_val):
    """Check if a date is valid ISO format."""
    if date_val is None:
        return False
    if isinstance(date_val, datetime):
        return True
    if isinstance(date_val, str):
        date_val = date_val.strip()
        if not date_val:
            return False
        try:
            datetime.fromisoformat(date_val.replace("Z", "+00:00"))
            return True
        except ValueError:
            return False
    return False

def validate_front_matter(fm, filepath):
    """Scan a single front matter dictionary for issues."""
    issues = []

    required_fields = ["title", "date", "lastmod", "author"]
    for field in required_fields:
        if field not in fm:
            issues.append(f"Missing required field: {field}")
        elif field in ["date", "lastmod"]:
            if not check_date_format(fm[field]):
                issues.append(f"Invalid date format in field: {field}")

    # Slug check
    if "slug" in fm and " " in fm["slug"]:
        issues.append("Slug contains spaces; consider using hyphens (-) only")

    # Categories & tags should be lists
    for key in ["categories", "tags"]:
        if key in fm and not isinstance(fm[key], list):
            issues.append(f"{key} should be a list")

    if issues:
        return f"Issues in {filepath}:\n  - " + "\n  - ".join(issues)
    return None

def scan_content():
    """Walk content directory and scan Markdown files."""
    problems = []
    for root, dirs, files in os.walk(CONTENT_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
                if lines and lines[0] == "---":
                    # Extract front matter
                    try:
                        end_idx = lines[1:].index("---") + 1
                        fm_text = "\n".join(lines[1:end_idx])
                        fm = yaml.safe_load(fm_text)
                        issue = validate_front_matter(fm, filepath)
                        if issue:
                            problems.append(issue)
                    except Exception as e:
                        problems.append(f"Error parsing front matter in {filepath}: {e}")
                else:
                    problems.append(f"No front matter found in {filepath}")
    return problems

def main():
    print("Scanning Hugo content for front matter issues...\n")
    content_issues = scan_content()
    if content_issues:
        print("\n".join(content_issues))
    else:
        print("No issues found. Front matter looks good!")
    print("\nScan complete.")

if __name__ == "__main__":
    main()
