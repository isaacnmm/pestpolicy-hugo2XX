import os
import datetime
import re

# --- CONFIGURATION: PLEASE EDIT THESE VALUES ---

# 1. Path to your Hugo site's "posts" folder.
#    Based on your example, it should look like this.
#    IMPORTANT: Replace "C:\My Hugo Sites\pestpolicy-hugo2XX" with the actual path on your computer.
HUGO_POSTS_PATH = r"C:\My Hugo Sites\pestpolicy-hugo2XX\content\posts"

# 2. Default author for the posts.
DEFAULT_AUTHOR = "Isaac"

# 3. The list of 50 keywords.
KEYWORDS = [
    "How to get rid of sugar ants in Portland, Oregon kitchens",
    "Signs of carpenter ants in houses in the Pacific Northwest",
    "Best way to kill scorpions in Phoenix, Arizona homes",
    "Natural scorpion repellent for Las Vegas yards",
    "How to deal with roof rats in Southern California attics",
    "Cost of termite tenting for Formosan termites in New Orleans",
    "Fire ant mound treatment for lawns in Dallas, Texas",
    "How to get rid of palmetto bugs in Florida apartments",
    "Preventing ticks in wooded yards in Connecticut",
    "Rodent proofing brownstone apartments in Brooklyn, NY",
    "Overwintering pests to watch for in the Midwest",
    "Common pests found in different regions of the U.S.",
    "How to keep spiders out of the house in the fall",
    "What to do about a wasp nest on your porch in summer",
    "How to stop ants from coming in the house when it rains",
    "Getting rid of cluster flies on windows in late summer",
    "How to prevent mice from coming inside for the winter",
    "Spring pest control checklist for homeowners",
    "Signs of a yellow jacket nest in the ground",
    "How to get rid of fruit flies in the kitchen overnight",
    "What attracts stink bugs into the house in September",
    "Natural mosquito control for summer backyard parties",
    "DIY bed bug treatment for a single room",
    "Pet-safe ant killer for inside the house",
    "Homemade spray to kill cockroaches instantly",
    "Does boric acid work for killing German cockroaches",
    "Using diatomaceous earth for fleas in carpet",
    "Best essential oils to repel spiders and mice",
    "How to make a natural wasp and hornet killer spray",
    "Vinegar and Dawn dish soap trap for fruit flies",
    "Is professional pest control safe for babies and pets",
    "Eco-friendly termite prevention methods",
    "How to get rid of drain flies in the bathroom sink",
    "Signs of mice in the kitchen cabinets",
    "What is the buzzing sound inside my walls",
    "How to remove squirrels from the attic and chimney",
    "Getting rid of spiders in the basement and crawl space",
    "Small black bugs on the windowsill, what are they",
    "How to get rid of ants in a potted plant",
    "Why do I have cockroaches in my car",
    "Carpet beetle larvae in closet, how to eliminate",
    "Silverfish in the bathtub, what causes them",
    "Average cost of a one-time pest control visit",
    "How much does monthly vs. quarterly pest control cost",
    "Is DIY pest control cheaper than hiring an exterminator",
    "Cost of professional bed bug heat treatment",
    "Factors that determine the price of termite treatment",
    "Is organic pest control more expensive",
    "Wildlife removal cost for raccoons vs. squirrels",
    "Why is pest control so expensive in my city"
]
# --- END OF CONFIGURATION ---


def sanitize_slug(keyword):
    """Converts a keyword into a URL-friendly slug for the folder name."""
    s = keyword.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s

def create_hugo_post_bundle(keyword, posts_path, author):
    """Creates a Hugo post bundle (folder + index.md) for a given keyword."""
    if not os.path.exists(posts_path):
        print(f"Error: The path '{posts_path}' does not exist.")
        print("Please update the HUGO_POSTS_PATH variable in the script.")
        return

    # Generate title, slug, and paths
    title = ' '.join(word.capitalize() for word in keyword.split())
    slug = sanitize_slug(keyword)
    post_folder_path = os.path.join(posts_path, slug)
    index_file_path = os.path.join(post_folder_path, "index.md")

    # Create the directory for the post bundle
    try:
        os.makedirs(post_folder_path, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory {post_folder_path}: {e}")
        return

    # Format date and time exactly as in the sample
    now = datetime.datetime.now(datetime.timezone.utc)
    date_str = now.strftime("'%Y-%m-%d %H:%M:%S+00:00'")

    # Create placeholder content
    content_placeholder = f"""
## The Problem: Understanding {keyword}

Start the article with a compelling introduction that directly addresses the user's search query. Acknowledge their frustration and promise a clear solution.

### Key Takeaways at a Glance

| Aspect | Summary |
| :--- | :--- |
| **Identification** | Briefly describe how to identify the pest or problem. |
| **Primary Solution** | Mention the most effective solution you'll discuss. |
| **Prevention Tip** | Give one quick tip for preventing the issue from returning. |

## Step-by-Step Guide to Solving Your Pest Problem

Use clear, actionable headings. Break down the solution into easy-to-follow steps.

1.  **Step 1: Inspection and Identification**
    *   Detail where to look and what to look for.

2.  **Step 2: Immediate Action & DIY Solutions**
    *   Provide safe, effective DIY methods using common household items.

3.  **Step 3: When to Call a Professional**
    *   Explain the signs that indicate a professional exterminator is needed.

## Essential Prevention Tips

Offer a list of long-term strategies to prevent the pest from coming back. Use bullet points for readability.

*   Seal entry points...
*   Remove food and water sources...
*   Maintain your yard...

## Frequently Asked Questions (FAQ)

**Q: Is this method safe for pets and children?**
A: Address common safety concerns related to your proposed solutions.

**Q: How long does it take for this method to work?**
A: Set realistic expectations for the user.

## The Verdict

Conclude the article by summarizing the most important points and empowering the reader to take control of their pest situation.
"""

    # Create the front matter and the full file content
    file_content = f"""---
title: "{title}"
description: "Your complete guide to understanding and solving '{keyword}'. Get expert tips, DIY solutions, and prevention strategies to protect your home."
slug: /{slug}/
date: {date_str}
lastmod: {date_str}
author: {author}
categories:
- Pest Control
- Guides
tags:
- {keyword.split()[0].lower()}
- diy pest control
- home maintenance
layout: post
---
{content_placeholder}
"""

    # Write the content to the new index.md file
    try:
        with open(index_file_path, "w", encoding="utf-8") as f:
            f.write(file_content)
        print(f"Successfully created bundle: {slug}\\index.md")
    except IOError as e:
        print(f"Error creating file {index_file_path}: {e}")


def main():
    """Main function to generate all posts."""
    print("Starting Hugo post bundle generation...")
    
    # Basic validation of the path
    if "pestpolicy-hugo2XX" not in HUGO_POSTS_PATH:
         print("!!! WARNING: Please update the HUGO_POSTS_PATH variable to match your project folder. !!!")
         return

    for keyword in KEYWORDS:
        create_hugo_post_bundle(keyword, HUGO_POSTS_PATH, DEFAULT_AUTHOR)
    
    print("\nScript finished. All post bundles have been created.")
    print("Next steps:")
    print("1. Open each new folder in your 'content/posts' directory.")
    print("2. Edit the 'index.md' file and replace the placeholder with AI-generated content.")
    print("3. When ready to publish, run 'hugo server' to preview your site.")


if __name__ == "__main__":
    main()