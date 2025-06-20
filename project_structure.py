import os
from pathlib import Path

# Root folder
root = Path("portfolio_website")

# Define subfolders
folders = [
    root / "static" / "css",
    root / "static" / "images",
    root / "static" / "js",
    root / "templates"
]

# Define files
files = [
    root / "app.py",
    root / "templates" / "base.html",
    root / "templates" / "index.html",
    root / "templates" / "about.html",
    root / "templates" / "projects.html",
    root / "templates" / "contact.html"
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for file in files:
    file.touch(exist_ok=True)

print("✅ portfolio_website structure created successfully.")
