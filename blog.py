#!/usr/bin/env python3
"""
Blog management CLI tool for creating and publishing posts.
Usage:
    python blog.py new <post-name>
    python blog.py publish <post-file>
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple


def create_new_post(post_name: str) -> None:
    """Create a new blog post from the template."""
    template_file = Path("post-template.html")
    posts_dir = Path("posts")
    output_file = posts_dir / f"{post_name}.html"
    
    # Check if template exists
    if not template_file.exists():
        print(f"Error: Template file '{template_file}' not found.", file=sys.stderr)
        sys.exit(1)
    
    # Check if posts directory exists
    if not posts_dir.exists():
        print(f"Error: Posts directory '{posts_dir}' not found.", file=sys.stderr)
        sys.exit(1)
    
    # Check if file already exists
    if output_file.exists():
        print(f"Error: Post file '{output_file}' already exists.", file=sys.stderr)
        sys.exit(1)
    
    # Read template
    content = template_file.read_text()
    
    # Replace {{DATE}} with current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    content = content.replace("{{DATE}}", current_date)
    
    # Write new post file
    output_file.write_text(content)
    
    print(f"Created new post: {output_file}")
    print(f"Date automatically set to: {current_date}")
    print("Don't forget to replace {{TITLE}} with your post title")


def extract_title_and_date(post_file: Path) -> Tuple[Optional[str], Optional[str]]:
    """Extract title and date from a post file."""
    content = post_file.read_text()
    
    # Extract title from <h1> tag in article header
    title_match = re.search(r'<h1>([^<]*)</h1>', content)
    title = title_match.group(1) if title_match else None
    
    # Extract date from <div class="meta"> tag
    date_match = re.search(r'<div class="meta">([^<]*)</div>', content)
    date = date_match.group(1) if date_match else None
    
    return title, date


def insert_entry_into_file(file_path: Path, new_entry: str) -> None:
    """Insert a new entry into an index file."""
    content = file_path.read_text()
    lines = content.splitlines()
    
    # Find the insertion point
    ul_start = None
    comment_line = None
    
    for i, line in enumerate(lines):
        if '<ul class="post-list">' in line:
            ul_start = i
        if '<!-- Posts will be listed here -->' in line:
            comment_line = i
    
    if ul_start is None:
        print(f"Error: Could not find post-list section in {file_path}", file=sys.stderr)
        sys.exit(1)
    
    # Find the first <li> tag after the <ul> tag
    insert_line = None
    for i in range(ul_start + 1, len(lines)):
        if '<li>' in lines[i]:
            insert_line = i
            break
    
    # If no <li> found, insert after comment or after <ul>
    if insert_line is None:
        if comment_line is not None:
            insert_line = comment_line + 1
        else:
            insert_line = ul_start + 1
    
    # Insert the new entry
    lines.insert(insert_line, new_entry)
    
    # Write back to file
    file_path.write_text('\n'.join(lines) + '\n')


def limit_recent_posts(file_path: Path, limit: int = 5) -> None:
    """Limit the number of recent posts in index.html to the specified limit."""
    content = file_path.read_text()
    lines = content.splitlines()
    
    # Find the <ul class="post-list"> section
    ul_start = None
    ul_end = None
    
    for i, line in enumerate(lines):
        if '<ul class="post-list">' in line:
            ul_start = i
        if ul_start is not None and '</ul>' in line:
            ul_end = i
            break
    
    if ul_start is None or ul_end is None:
        print(f"Warning: Could not find post-list section in {file_path}")
        return
    
    # Extract all <li> entries with their dates
    entries = []
    for i in range(ul_start + 1, ul_end):
        line = lines[i]
        if '<li>' in line:
            # Extract date from the line
            date_match = re.search(r'<span class="date">([^<]*)</span>', line)
            date = date_match.group(1) if date_match else ""
            entries.append((date, line))
    
    # Sort by date (descending - most recent first) and take top N
    entries.sort(key=lambda x: x[0], reverse=True)
    top_entries = entries[:limit]
    
    # Rebuild the file
    new_lines = lines[:ul_start + 1]
    
    # Add comment if it exists in the original
    if any('<!-- Posts will be listed here -->' in line for line in lines[ul_start:ul_end]):
        new_lines.append('            <!-- Posts will be listed here -->')
    
    # Add the top entries
    for _, entry_line in top_entries:
        new_lines.append(entry_line)
    
    # Add closing </ul> and rest of file
    new_lines.append('        </ul>')
    new_lines.extend(lines[ul_end + 1:])
    
    # Write back to file
    file_path.write_text('\n'.join(new_lines) + '\n')


def publish_post(post_file: str) -> None:
    """Publish a post by adding it to both index.html and posts/index.html."""
    post_path = Path(post_file)
    
    # Check if post file exists
    if not post_path.exists():
        print(f"Error: Post file '{post_path}' not found.", file=sys.stderr)
        sys.exit(1)
    
    # Extract post filename and path
    post_filename = post_path.name
    post_url_path = f"/posts/{post_filename}"
    
    # Extract title and date
    title, date = extract_title_and_date(post_path)
    
    if not title:
        print("Error: Could not extract title from post file.", file=sys.stderr)
        sys.exit(1)
    
    if not date:
        print("Error: Could not extract date from post file.", file=sys.stderr)
        sys.exit(1)
    
    # Check if index files exist
    index_file = Path("index.html")
    posts_index_file = Path("posts/index.html")
    
    if not index_file.exists():
        print("Error: index.html not found.", file=sys.stderr)
        sys.exit(1)
    
    if not posts_index_file.exists():
        print("Error: posts/index.html not found.", file=sys.stderr)
        sys.exit(1)
    
    # Check if post is already in the index files
    index_content = index_file.read_text()
    posts_index_content = posts_index_file.read_text()
    
    if post_url_path in index_content or post_url_path in posts_index_content:
        print(f"Warning: Post '{post_url_path}' already exists in one or both index files.")
        print("Skipping to avoid duplicates. If you want to update, remove the entry manually first.")
        return
    
    # Create the new list item
    new_entry = f'            <li><a href="{post_url_path}">{title}</a> <span class="date">{date}</span></li>'
    
    # Add entry to both index files
    insert_entry_into_file(index_file, new_entry)
    insert_entry_into_file(posts_index_file, new_entry)
    
    # Limit recent posts to 5 most recent in index.html
    limit_recent_posts(index_file, limit=5)
    
    print(f"Published post: {title}")
    print("Added to index.html and posts/index.html")
    print(f"Date: {date}")


def main():
    parser = argparse.ArgumentParser(
        description="Blog management CLI tool for creating and publishing posts"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute", required=True)
    
    # New post command
    new_parser = subparsers.add_parser("new", help="Create a new blog post")
    new_parser.add_argument("post_name", help="Name of the new post (without .html extension)")
    
    # Publish post command
    publish_parser = subparsers.add_parser("publish", help="Publish a blog post")
    publish_parser.add_argument("post_file", help="Path to the post file (e.g., posts/my-post.html)")
    
    args = parser.parse_args()
    
    if args.command == "new":
        create_new_post(args.post_name)
    elif args.command == "publish":
        publish_post(args.post_file)


if __name__ == "__main__":
    main()

