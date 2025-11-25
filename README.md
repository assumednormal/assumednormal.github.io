# assumednormal.github.io

Minimal, text-only blog.

## Structure

- `index.html` - Home page with recent posts
- `posts/` - Directory containing blog posts (HTML files)
- `css/main.css` - Minimal stylesheet
- `CNAME` - Custom domain configuration
- `blog.py` - CLI tool for creating and publishing posts
- `main.py` - Main entry point
- `pyproject.toml` - Python project configuration

## Setup

This project uses `uv` for Python package management. To set up:

```bash
uv sync
```

## Local Development

To preview the site locally in your browser:

```bash
python main.py
```

This starts a local web server at `http://localhost:8000/`. Open this URL in your browser to view the site. The server will automatically reload when you make changes to the files. Press `Ctrl+C` to stop the server.

**Options:**
- `--port <number>` - Specify a custom port (e.g., `python main.py --port 8080`)
- `--auto-port` - Automatically try the next available port if the default port is in use

## Adding a New Post

Use the `blog.py` CLI tool to create and publish posts:

1. **Create a new post:**
   ```bash
   python blog.py new <post-name>
   ```
   This creates a new HTML file in the `posts/` directory from the template, automatically setting the date.

2. **Edit the post:**
   - Open the created file in `posts/<post-name>.html`
   - Replace `{{TITLE}}` with your post title
   - Add your content

3. **Publish the post:**
   ```bash
   python blog.py publish posts/<post-name>.html
   ```
   This automatically adds the post to both `index.html` and `posts/index.html`, and limits the home page to the 5 most recent posts.

## Features

- Math support via MathJax (inline: `$...$`, display: `$$...$$`)
- Code highlighting (basic styling, can be enhanced)
- Minimal, text-only design
- Google Analytics integration

