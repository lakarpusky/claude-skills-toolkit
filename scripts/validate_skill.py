
#!/usr/bin/env python3
"""
Skill Validator - Validates skill structure and YAML frontmatter.

Usage:
    python validate_skill.py /path/to/skill-folder
    python validate_skill.py /path/to/SKILL.md
"""

import sys
import re
from pathlib import Path
from typing import Tuple, List

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def check_mark(passed: bool) -> str:
    return f"{GREEN}✓{RESET}" if passed else f"{RED}✗{RESET}"


def warn_mark() -> str:
    return f"{YELLOW}⚠{RESET}"


def validate_skill(skill_path: Path) -> Tuple[bool, List[str]]:
    """Validate a skill folder or SKILL.md file."""
    errors = []
    warnings = []
    
    # Determine if path is file or folder
    if skill_path.is_file():
        skill_md = skill_path
        skill_folder = skill_path.parent
    else:
        skill_folder = skill_path
        skill_md = skill_folder / "SKILL.md"
    
    # Check 1: SKILL.md exists with exact naming
    if not skill_md.exists():
        # Check for common mistakes
        for variant in ["skill.md", "SKILL.MD", "Skill.md"]:
            if (skill_folder / variant).exists():
                errors.append(f"Found '{variant}' but must be exactly 'SKILL.md' (case-sensitive)")
                break
        else:
            errors.append("SKILL.md not found")
        return False, errors
    
    print(f"{check_mark(True)} SKILL.md exists with correct naming")
    
    # Check 2: Folder naming (kebab-case)
    folder_name = skill_folder.name
    if folder_name != folder_name.lower():
        errors.append(f"Folder name '{folder_name}' contains uppercase - use kebab-case")
    if " " in folder_name:
        errors.append(f"Folder name '{folder_name}' contains spaces - use kebab-case")
    if "_" in folder_name:
        warnings.append(f"Folder name '{folder_name}' uses underscores - prefer kebab-case")
    
    if not any("Folder name" in e for e in errors):
        print(f"{check_mark(True)} Folder naming follows kebab-case")
    
    # Check 3: No README.md inside skill
    if (skill_folder / "README.md").exists():
        warnings.append("README.md found inside skill folder - move to repo root for distribution")
    
    # Read SKILL.md content
    content = skill_md.read_text()
    
    # Check 4: YAML frontmatter exists with delimiters
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        if content.startswith("name:") or content.startswith("description:"):
            errors.append("Missing YAML delimiters (---) around frontmatter")
        else:
            errors.append("No YAML frontmatter found")
        return False, errors
    
    print(f"{check_mark(True)} YAML frontmatter has correct delimiters")
    
    frontmatter = frontmatter_match.group(1)
    
    # Check 5: Required fields
    has_name = bool(re.search(r'^name:\s*\S', frontmatter, re.MULTILINE))
    has_description = bool(re.search(r'^description:\s*\S', frontmatter, re.MULTILINE))
    
    if not has_name:
        errors.append("Missing required field: name")
    else:
        print(f"{check_mark(True)} 'name' field present")
        
        # Validate name format
        name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
        if name_match:
            name = name_match.group(1).strip()
            if name != name.lower():
                errors.append(f"name '{name}' contains uppercase - use kebab-case")
            if " " in name:
                errors.append(f"name '{name}' contains spaces - use kebab-case")
            if "claude" in name.lower() or "anthropic" in name.lower():
                errors.append(f"name cannot contain 'claude' or 'anthropic' (reserved)")
    
    if not has_description:
        errors.append("Missing required field: description")
    else:
        print(f"{check_mark(True)} 'description' field present")
        
        # Extract description for analysis
        desc_match = re.search(r'^description:\s*[|>]?\s*\n?(.*?)(?=^[a-z]+:|$)', 
                               frontmatter, re.MULTILINE | re.DOTALL)
        if desc_match:
            description = desc_match.group(1).strip()
            
            # Check description length
            if len(description) > 1024:
                errors.append(f"description exceeds 1024 chars ({len(description)} chars)")
            
            # Check for trigger phrases
            trigger_words = ["use when", "trigger", "ask for", "user says", "user asks"]
            has_triggers = any(word in description.lower() for word in trigger_words)
            if not has_triggers:
                warnings.append("description may be missing trigger phrases (e.g., 'Use when user says...')")
    
    # Check 6: No XML tags in frontmatter
    if "<" in frontmatter or ">" in frontmatter:
        errors.append("XML angle brackets (<>) found in frontmatter - forbidden for security")
    else:
        print(f"{check_mark(True)} No XML tags in frontmatter")
    
    # Check 7: Unclosed quotes
    single_quotes = frontmatter.count("'")
    double_quotes = frontmatter.count('"')
    if single_quotes % 2 != 0:
        errors.append("Possible unclosed single quote in frontmatter")
    if double_quotes % 2 != 0:
        errors.append("Possible unclosed double quote in frontmatter")
    
    # Check 8: Body content exists
    body = content[frontmatter_match.end():].strip()
    if not body:
        warnings.append("SKILL.md body is empty - add instructions")
    elif len(body) < 100:
        warnings.append("SKILL.md body is very short - consider adding more detail")
    else:
        word_count = len(body.split())
        if word_count > 5000:
            warnings.append(f"SKILL.md body is {word_count} words - consider moving detail to references/")
        print(f"{check_mark(True)} SKILL.md body has content ({word_count} words)")
    
    # Print warnings
    for warn in warnings:
        print(f"{warn_mark()} {warn}")
    
    # Print errors
    for err in errors:
        print(f"{check_mark(False)} {err}")
    
    return len(errors) == 0, errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_skill.py /path/to/skill-folder")
        print("       python validate_skill.py /path/to/SKILL.md")
        sys.exit(1)
    
    skill_path = Path(sys.argv[1])
    
    if not skill_path.exists():
        print(f"{RED}Error: Path does not exist: {skill_path}{RESET}")
        sys.exit(1)
    
    print(f"\nValidating skill: {skill_path}\n")
    print("-" * 50)
    
    passed, errors = validate_skill(skill_path)
    
    print("-" * 50)
    
    if passed:
        print(f"\n{GREEN}✓ Skill validation passed!{RESET}\n")
        sys.exit(0)
    else:
        print(f"\n{RED}✗ Skill validation failed with {len(errors)} error(s){RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
