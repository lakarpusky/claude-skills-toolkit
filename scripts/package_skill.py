
#!/usr/bin/env python3
"""
Skill Packager - Packages a skill folder for distribution.

Usage:
    python package_skill.py /path/to/skill-folder
    python package_skill.py /path/to/skill-folder --output ./dist
"""

import sys
import argparse
import zipfile
from pathlib import Path
from datetime import datetime


def package_skill(skill_path: Path, output_dir: Path = None):
    """Package a skill folder into a distributable zip file."""
    
    skill_path = skill_path.resolve()
    
    if not skill_path.is_dir():
        print(f"Error: {skill_path} is not a directory")
        sys.exit(1)
    
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"Error: SKILL.md not found in {skill_path}")
        sys.exit(1)
    
    skill_name = skill_path.name
    
    # Determine output location
    if output_dir:
        output_dir = output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
    else:
        output_dir = skill_path.parent
    
    # Create zip filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    zip_name = f"{skill_name}-{timestamp}.zip"
    zip_path = output_dir / zip_name
    
    # Files/folders to exclude
    exclude_patterns = {
        ".git",
        ".gitignore",
        ".DS_Store",
        "__pycache__",
        "*.pyc",
        ".env",
        "node_modules",
        "README.md",  # README goes at repo level, not in skill
    }
    
    def should_exclude(path: Path) -> bool:
        name = path.name
        for pattern in exclude_patterns:
            if pattern.startswith("*"):
                if name.endswith(pattern[1:]):
                    return True
            elif name == pattern:
                return True
        return False
    
    # Create zip
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in skill_path.rglob("*"):
            if file_path.is_file() and not should_exclude(file_path):
                # Check parent folders too
                if any(should_exclude(p) for p in file_path.parents):
                    continue
                
                arcname = file_path.relative_to(skill_path.parent)
                zf.write(file_path, arcname)
                print(f"  Added: {arcname}")
    
    print(f"\n✓ Created: {zip_path}")
    print(f"  Size: {zip_path.stat().st_size / 1024:.1f} KB")
    
    return zip_path


def main():
    parser = argparse.ArgumentParser(description="Package a skill for distribution")
    parser.add_argument("skill_path", type=Path, help="Path to skill folder")
    parser.add_argument("--output", "-o", type=Path, help="Output directory for zip file")
    
    args = parser.parse_args()
    
    print(f"Packaging skill: {args.skill_path}\n")
    package_skill(args.skill_path, args.output)


if __name__ == "__main__":
    main()
