
#!/usr/bin/env python3
"""
Skill Scaffolder - Creates a new skill folder with proper structure.

Usage:
    python create_skill.py skill-name
    python create_skill.py skill-name --mcp server-name
    python create_skill.py skill-name --minimal
"""

import sys
import argparse
from pathlib import Path

MINIMAL_TEMPLATE = '''---
name: {name}
description: Brief description. Use when user says "X" or asks about Y.
---

# {title}

## Instructions

1. First step
2. Second step
3. Final step

## Example

User: "Do X"
→ Action taken
→ Result achieved
'''

STANDARD_TEMPLATE = '''---
name: {name}
description: |
  [WHAT] Brief description of what this skill does.
  [WHEN] Use when user says "X", "Y", or asks about Z.
  [CAPABILITIES] Key features: A, B, C.
# metadata:
#   author: Your Name
#   version: 1.0.0
---

# {title}

Brief overview of what this skill accomplishes.

---

## Instructions

### Step 1: [First Major Action]

Clear explanation of what happens in this step.

**Expected output:** Description of success state.

### Step 2: [Second Major Action]

Continue with next step...

### Step 3: [Final Action]

Complete the workflow...

---

## Examples

### Example 1: [Common Scenario]

**User says:** "Help me do X with Y"

**Actions:**
1. First action taken
2. Second action taken
3. Final action

**Result:** Clear description of outcome.

---

## Error Handling

### Error: [Common Error Message]

**Cause:** Why this happens

**Solution:**
1. First fix step
2. Second fix step
'''

MCP_TEMPLATE = '''---
name: {name}
description: |
  [SERVICE] integration for [DOMAIN] workflows.
  Use when user mentions "[trigger1]", "[trigger2]", or asks to "[action]".
  Requires {mcp_server} MCP server connected.
metadata:
  author: Your Name
  version: 1.0.0
  mcp-server: {mcp_server}
---

# {title}

Orchestrates {mcp_server} MCP tools for common workflows.

---

## Prerequisites

- {mcp_server} MCP server connected (Settings > Extensions)
- Valid API credentials configured

---

## Workflows

### Workflow 1: [Primary Workflow Name]

**Trigger:** User says "X" or "Y"

#### Phase 1: [Setup Phase]

```
Call MCP tool: `tool_name`
Parameters:
  - param1: {{user_input}}
  - param2: default_value
```

**Validate:** Check response contains expected_field

#### Phase 2: [Execution Phase]

```
Call MCP tool: `another_tool`
Parameters:
  - id: {{from_phase_1}}
```

**Result:** Summarize outcome

---

## Error Handling

### MCP Connection Failed

**Symptoms:** "Connection refused" or timeout

**Resolution:**
1. Check Settings > Extensions > {mcp_server}
2. Verify status shows "Connected"
3. If disconnected, click Reconnect

---

## References

- MCP Server Docs: [link]
- See `references/api-guide.md` for detailed documentation
'''


def to_title(name: str) -> str:
    """Convert kebab-case to Title Case."""
    return " ".join(word.capitalize() for word in name.split("-"))


def create_skill(name: str, mcp_server: str = None, minimal: bool = False):
    """Create a new skill folder with proper structure."""
    
    # Validate name
    if name != name.lower():
        print(f"Error: Skill name must be lowercase. Try: {name.lower()}")
        sys.exit(1)
    
    if " " in name:
        suggested = name.replace(" ", "-")
        print(f"Error: Skill name cannot contain spaces. Try: {suggested}")
        sys.exit(1)
    
    if "_" in name:
        suggested = name.replace("_", "-")
        print(f"Warning: Prefer kebab-case over underscores. Consider: {suggested}")
    
    if "claude" in name.lower() or "anthropic" in name.lower():
        print("Error: Skill name cannot contain 'claude' or 'anthropic' (reserved)")
        sys.exit(1)
    
    # Create folder
    skill_path = Path(name)
    if skill_path.exists():
        print(f"Error: Folder '{name}' already exists")
        sys.exit(1)
    
    skill_path.mkdir()
    
    # Choose template
    title = to_title(name)
    
    if minimal:
        content = MINIMAL_TEMPLATE.format(name=name, title=title)
    elif mcp_server:
        content = MCP_TEMPLATE.format(name=name, title=title, mcp_server=mcp_server)
        # Create references folder for MCP skills
        (skill_path / "references").mkdir()
        (skill_path / "references" / "api-guide.md").write_text(
            f"# {mcp_server} API Reference\n\nAdd API documentation here.\n"
        )
    else:
        content = STANDARD_TEMPLATE.format(name=name, title=title)
    
    # Write SKILL.md
    (skill_path / "SKILL.md").write_text(content)
    
    # Create optional folders for non-minimal
    if not minimal:
        (skill_path / "scripts").mkdir(exist_ok=True)
        (skill_path / "scripts" / ".gitkeep").touch()
        
        if not mcp_server:
            (skill_path / "references").mkdir(exist_ok=True)
            (skill_path / "references" / ".gitkeep").touch()
    
    print(f"✓ Created skill: {name}/")
    print(f"  └── SKILL.md")
    if not minimal:
        print(f"  └── scripts/")
        print(f"  └── references/")
    
    print(f"\nNext steps:")
    print(f"  1. Edit {name}/SKILL.md with your instructions")
    print(f"  2. Validate: python validate_skill.py {name}")
    print(f"  3. Test in Claude Code or Claude.ai")


def main():
    parser = argparse.ArgumentParser(description="Create a new skill folder")
    parser.add_argument("name", help="Skill name in kebab-case")
    parser.add_argument("--mcp", dest="mcp_server", help="MCP server name for MCP-enhanced skills")
    parser.add_argument("--minimal", action="store_true", help="Create minimal skill structure")
    
    args = parser.parse_args()
    
    create_skill(args.name, args.mcp_server, args.minimal)


if __name__ == "__main__":
    main()
