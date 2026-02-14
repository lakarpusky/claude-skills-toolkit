# Claude Skills Toolkit

A comprehensive toolkit for building, validating, and distributing skills for Claude Code and Claude.ai.

## What are Skills?

Skills are instruction sets (packaged as folders) that teach Claude how to handle specific tasks or workflows. Instead of re-explaining your preferences in every conversation, skills let you teach Claude once and benefit every time.

## Quick Start

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/claude-skills-toolkit.git
cd claude-skills-toolkit

# Create a new skill
python scripts/create_skill.py my-awesome-skill

# Validate before deploying
python scripts/validate_skill.py my-awesome-skill/

# Package for distribution
python scripts/package_skill.py my-awesome-skill/
```

## Repository Structure

```
claude-skills-toolkit/
├── SKILLS-KNOWLEDGE-BASE.md    # Complete reference guide
├── scripts/
│   ├── create_skill.py         # Scaffold new skills
│   ├── validate_skill.py       # Validate structure & YAML
│   └── package_skill.py        # Package for distribution
├── templates/
│   ├── SKILL-TEMPLATE.md       # Full-featured template
│   ├── SKILL-MINIMAL.md        # Quick-start template
│   ├── SKILL-MCP-TEMPLATE.md   # MCP-enhanced template
│   └── example-workflow/       # Working example
└── references/
    ├── patterns.md             # Implementation patterns
    ├── yaml-frontmatter.md     # YAML field reference
    └── troubleshooting.md      # Common issues & fixes
```

## Scripts

### `create_skill.py`

Scaffolds a new skill with proper structure.

```bash
# Standard skill
python scripts/create_skill.py my-skill

# Minimal (quick start)
python scripts/create_skill.py my-skill --minimal

# MCP-enhanced
python scripts/create_skill.py my-skill --mcp linear
```

### `validate_skill.py`

Validates skill structure and YAML frontmatter before deployment.

```bash
python scripts/validate_skill.py path/to/skill/

# Output:
# ✓ SKILL.md exists with correct naming
# ✓ Folder naming follows kebab-case
# ✓ YAML frontmatter has correct delimiters
# ✓ 'name' field present
# ✓ 'description' field present
# ✓ No XML tags in frontmatter
# ✓ Skill validation passed!
```

### `package_skill.py`

Packages a skill folder into a distributable zip file.

```bash
python scripts/package_skill.py path/to/skill/
# Creates: skill-name-20260214.zip
```

## Templates

| Template | Use Case |
|----------|----------|
| `SKILL-TEMPLATE.md` | Full-featured with examples, error handling, references |
| `SKILL-MINIMAL.md` | Quick 10-line skill for simple tasks |
| `SKILL-MCP-TEMPLATE.md` | Skills that orchestrate MCP server tools |

## Skill Anatomy

```yaml
---
name: skill-name-in-kebab-case
description: |
  What it does. Use when user says "X" or asks about Y.
  Include specific trigger phrases.
metadata:
  author: Your Name
  version: 1.0.0
---

# Skill Name

## Instructions
1. Step one
2. Step two

## Examples
User: "Do X"
→ Result

## Error Handling
...
```

### Required Fields

| Field | Rules |
|-------|-------|
| `name` | kebab-case, must match folder name |
| `description` | Include WHAT + WHEN (trigger phrases), max 1024 chars |

### Forbidden

- XML tags (`<` `>`) in frontmatter
- Names containing "claude" or "anthropic"
- `README.md` inside skill folder

## Installation

### Claude Code

Copy skill folders to your Claude Code skills directory:
```
~/.claude/skills/
```

### Claude.ai

1. Zip the skill folder
2. Go to Settings → Capabilities → Skills
3. Upload the zip file

## Documentation

- **[SKILLS-KNOWLEDGE-BASE.md](./SKILLS-KNOWLEDGE-BASE.md)** - Complete guide covering everything from the official Anthropic documentation
- **[references/patterns.md](./references/patterns.md)** - 7 implementation patterns (sequential workflow, multi-MCP, iterative refinement, etc.)
- **[references/yaml-frontmatter.md](./references/yaml-frontmatter.md)** - Complete YAML field reference
- **[references/troubleshooting.md](./references/troubleshooting.md)** - Quick fixes for common issues

## Skill Categories

### Category 1: Document & Asset Creation
Creating consistent output (documents, presentations, code, designs).

### Category 2: Workflow Automation
Multi-step processes with validation gates.

### Category 3: MCP Enhancement
Workflow guidance for MCP server integrations.

## Resources

- [Anthropic Skills Documentation](https://docs.anthropic.com)
- [Official Skills Repository](https://github.com/anthropics/skills)
- [MCP Documentation](https://modelcontextprotocol.io)

## License

MIT

---

Built with knowledge from [The Complete Guide to Building Skills for Claude](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf) by Anthropic.
