#!/usr/bin/env python3
"""
hugo_large_site_analyzer.py

Scalable analyzer for large local Hugo sites:
- Parses front matter + markdown
- Extracts links, tags, word counts
- Detects duplicates via MinHash + LSH (fast)
- Finds broken internal links, orphans, thin content
- Outputs JSON + CSV reports
"""

import os
import re
import json
import csv
import argparse
from pathlib import Path
from urllib.parse import urlparse

import frontmatter
import markdown
from bs4 import BeautifulSoup
from datasketch import MinHash, MinHashLSH
from tqdm import tqdm

SHINGLE_SIZE = 5
MINHASH_PERM = 128

def read_markdown_file(path: Path):
    try:
        post = frontmatter.load(str(path))
        return post.metadata or {}, post.content or ""
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return {}, ""

def normalize_link(href: str):
    if not href:
        return href
    href = href.split("#")[0].split("?")[0]
    return href.rstrip("/")

def extract_links_and_images(md_text: str):
    html = markdown.markdown(md_text, extensions=["extra", "tables", "fenced_code"])
    soup = BeautifulSoup(html, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)]
    # Include markdown links missed by converter
    md_links = re.findall(r'\[.*?\]\((.*?)\)', md_text)
    for l in md_links:
        if l not in links:
            links.append(l)
    images = [{"src": img.get("src", ""), "alt": img.get("alt", "")} for img in soup.find_all("img")]
    return links, images

def word_count(text: str):
    return len(re.findall(r"\w+", text))

def guess_url(filepath: Path, meta: dict, content_dir: Path):
    for k in ("url", "permalink"):
        if k in meta and meta[k]:
            return normalize_link(str(meta[k]))
    slug = meta.get("slug")
    rel = filepath.relative_to(content_dir)
    parts = list(rel.parts)
    name = filepath.stem
    folder = parts[:-1]

    if not slug:
        m = re.match(r"^\d{4}-\d{2}-\d{2}-(.+)$", name)
        slug = m.group(1) if m else name

    if name in ("index", "_index"):
        if folder:
            url = "/" + "/".join(folder) + "/"
        else:
            url = "/"
    else:
        if folder:
            url = "/" + "/".join(folder) + f"/{slug}/"
        else:
            url = f"/{slug}/"
    return normalize_link(url)

def make_shingles(text: str, k=SHINGLE_SIZE):
    toks = [t.lower() for t in re.findall(r"\w+", text)]
    if len(toks) < k:
        return set([" ".join(toks)]) if toks else set()
    return set(" ".join(toks[i:i+k]) for i in range(len(toks)-k+1))

def minhash_for_text(text, num_perm=MINHASH_PERM):
    shingles = make_shingles(text)
    m = MinHash(num_perm=num_perm)
    for sh in shingles:
        m.update(sh.encode("utf8"))
    return m

def analyze_site(content_dir: Path, thin_threshold=300, sim_threshold=0.7, max_pairs=20000):
    files = list(content_dir.rglob("*.md"))
    print(f"Found {len(files)} markdown files to analyze.")
    results = []
    url_to_file = {}
    file_to_url = {}

    # Parse files
    for fp in tqdm(files, desc="Parsing markdown"):
        meta, content = read_markdown_file(fp)
        title = meta.get("title", "").strip() or fp.stem
        date = meta.get("date", "")
        draft = bool(meta.get("draft", False))
        tags = meta.get("tags", []) or []
        categories = meta.get("categories", []) or meta.get("category", [])
        url = guess_url(fp, meta, content_dir)
        wc = word_count(content)
        links, images = extract_links_and_images(content)
        normalized_links = [normalize_link(l) for l in links if l and l.strip()]
        internal_links = [l for l in normalized_links if not urlparse(l).netloc]
        external_links = [l for l in normalized_links if urlparse(l).netloc]
        has_description = bool(meta.get("description") or meta.get("summary") or meta.get("excerpt"))

        rec = {
            "filepath": str(fp),
            "title": title,
            "date": str(date),
            "draft": draft,
            "tags": tags,
            "categories": categories,
            "word_count": wc,
            "url": url,
            "internal_links": internal_links,
            "external_links": external_links,
            "has_description": has_description,
            "images": images,
        }
        results.append(rec)
        url_to_file[url] = str(fp)
        file_to_url[str(fp)] = url

    # Detect duplicates using MinHash + LSH
    print("Computing duplicates with MinHash + LSH...")
    lsh = MinHashLSH(threshold=sim_threshold, num_perm=MINHASH_PERM)
    minhashes = {}
    for r in tqdm(results, desc="MinHash signatures"):
        text = (
            r["title"] + " " +
            " ".join(str(t) for t in r["tags"]) + " " +
            " ".join(str(c) for c in r["categories"])
        )
        try:
            with open(r["filepath"], encoding="utf-8") as f:
                body = f.read()
                text += " " + body
        except:
            pass
        m = minhash_for_text(text)
        lsh.insert(r["url"], m)
        minhashes[r["url"]] = m

    duplicates = []
    checked_pairs = set()
    for url, m in tqdm(minhashes.items(), desc="Finding duplicates"):
        matches = lsh.query(m)
        for match in matches:
            if match != url and (match, url) not in checked_pairs:
                checked_pairs.add((url, match))
                duplicates.append({"a": url, "b": match})

    # Find broken internal links
    print("Checking broken internal links...")
    broken_links = []
    for r in results:
        for l in r["internal_links"]:
            if l not in url_to_file:
                # Ignore mailto, tel, empty
                if l.startswith("mailto:") or l.startswith("tel:") or l == "":
                    continue
                broken_links.append({"from": r["url"], "link": l})

    # Find orphan pages (no incoming internal links)
    print("Finding orphan pages...")
    incoming_links = {url: 0 for url in url_to_file}
    for r in results:
        for l in r["internal_links"]:
            if l in incoming_links:
                incoming_links[l] += 1
    orphans = [url for url, count in incoming_links.items() if count == 0]

    # Pages missing essentials
    print("Checking pages for missing titles, descriptions, or thin content...")
    problems = []
    for r in results:
        p = []
        if not r["title"]:
            p.append("missing_title")
        if not r["has_description"]:
            p.append("missing_description")
        if r["word_count"] < thin_threshold and not r["draft"]:
            p.append("thin_content")
        if p:
            problems.append({"url": r["url"], "problems": p})

    return {
        "results": results,
        "duplicates": duplicates,
        "broken_links": broken_links,
        "orphans": orphans,
        "problems": problems,
    }

def save_reports(data, output_dir: Path):
    print(f"Saving reports to {output_dir}...")  # Confirm saving
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save JSON
    json_path = output_dir / "hugo_analysis.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Save CSV summary
    csv_path = output_dir / "hugo_summary.csv"
    keys = ["filepath", "title", "date", "draft", "word_count", "url", "has_description"]
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for r in data["results"]:
            writer.writerow({k: r.get(k, "") for k in keys})

    print(f"Reports saved to {output_dir}")

def print_summary(data):
    print("\nHugo Site Analysis Summary")
    print("-" * 30)
    print(f"Total pages: {len(data['results'])}")
    total_words = sum(r["word_count"] for r in data["results"])
    print(f"Total word count: {total_words:,}")
    avg_words = total_words / max(1, len(data["results"]))
    print(f"Average words per page: {avg_words:.1f}")
    print(f"Orphan pages (no incoming links): {len(data['orphans'])}")
    print(f"Broken internal links: {len(data['broken_links'])}")
    print(f"Pages with problems (missing titles/descriptions/thin content): {len(data['problems'])}")
    print(f"Duplicate page pairs detected: {len(data['duplicates'])}")

def main():
    parser = argparse.ArgumentParser(description="Analyze large Hugo site content directory")
    parser.add_argument("content_dir", type=Path, help="Path to Hugo site content/ directory")
    parser.add_argument("--output", type=Path, default=Path("hugo_analysis_output"), help="Output folder for reports")
    parser.add_argument("--thin-threshold", type=int, default=300, help="Word count threshold for thin content")
    parser.add_argument("--sim-threshold", type=float, default=0.7, help="MinHash similarity threshold for duplicates")
    args = parser.parse_args()

    data = analyze_site(
        content_dir=args.content_dir,
        thin_threshold=args.thin_threshold,
        sim_threshold=args.sim_threshold,
    )
    print_summary(data)
    save_reports(data, args.output)

if __name__ == "__main__":
    main()
