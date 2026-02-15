
# YAML Frontmatter Reference

Complete reference for skill YAML frontmatter fields.

---

## Required Format

```yaml
---
name: skill-name
description: What it does. Use when user says X or asks about Y.
---
```

The `---` delimiters are **required**.

---

## Field Reference

### `name` (required)

**Format:** kebab-case string
**Max length:** 100 characters

```yaml
# ✓ Correct
name: project-manager
name: api-client-v2
name: figma-design-export

# ✗ Wrong
name: Project Manager      # spaces
name: projectManager       # camelCase
name: project_manager      # underscores
name: ProjectManager       # PascalCase
name: claude-helper        # reserved prefix
name: anthropic-tool       # reserved prefix
```

**Rule:** Must match folder name exactly.

---

### `description` (required)

**Format:** String (can be multiline)
**Max length:** 1024 characters

**Structure:** `[WHAT] + [WHEN] + [CAPABILITIES]`

```yaml
# Single line
description: Analyzes CSV files for data quality. Use when user uploads .csv or asks for "data validation".

# Multiline (literal block)
description: |
  Manages Linear project workflows including sprint planning and task creation.
  Use when user mentions "sprint", "Linear tasks", or "project planning".
  Key features: velocity tracking, automatic labeling, team assignment.

# Multiline (folded block)
description: >
  End-to-end customer onboarding for PayFlow.
  Use when user says "onboard customer" or "set up subscription".
```

**Required elements:**
- What the skill does
- When to trigger (user phrases, file types, etc.)

**Forbidden:**
- XML tags (`<` or `>`)
- Executable code

---

### `license` (optional)

**Format:** SPDX license identifier

```yaml
license: MIT
license: Apache-2.0
license: GPL-3.0
license: BSD-3-Clause
```

---

### `compatibility` (optional)

**Format:** String
**Max length:** 500 characters

```yaml
# Runtime requirements
compatibility: "Requires Python 3.11+"

# Product targeting
compatibility: "Optimized for Claude Code"

# Multiple requirements
compatibility: "Requires Node.js 18+, network access to api.example.com"
```

---

### `metadata` (optional)

**Format:** Key-value pairs (arbitrary)

```yaml
metadata:
  author: Your Name
  version: 1.0.0
  mcp-server: linear
  category: productivity
  tags:
    - project-management
    - automation
    - productivity
  documentation: https://example.com/docs
  support: support@example.com
  changelog: |
    1.0.0 - Initial release
    0.9.0 - Beta
```

**Common fields:**
| Field | Purpose |
|-------|---------|
| `author` | Creator name/org |
| `version` | Semantic version |
| `mcp-server` | Associated MCP server |
| `category` | Skill category |
| `tags` | Searchable tags |

---

## Complete Examples

### Minimal Skill

```yaml
---
name: quick-note
description: Creates quick notes. Use when user says "note this" or "remember".
---
```

### Standard Skill

```yaml
---
name: data-analyzer
description: |
  Analyzes CSV and Excel files for data quality and statistics.
  Use when user uploads .csv/.xlsx or asks for "data analysis", 
  "statistics", or "data quality check".
license: MIT
metadata:
  author: Data Team
  version: 2.1.0
---
```

### MCP-Enhanced Skill

```yaml
---
name: linear-sprint-planner
description: |
  Orchestrates Linear MCP for sprint planning workflows.
  Use when user mentions "sprint planning", "Linear tasks", 
  "velocity", or "create tickets".
  Requires Linear MCP server connected.
license: Apache-2.0
compatibility: "Requires Linear MCP server"
metadata:
  author: DevTools Inc
  version: 1.0.0
  mcp-server: linear
  category: project-management
  tags:
    - linear
    - agile
    - sprint
---
```

---

## Validation Checklist

- [ ] Starts with `---`
- [ ] Ends section with `---`
- [ ] `name` is kebab-case
- [ ] `name` matches folder name
- [ ] `name` doesn't contain "claude" or "anthropic"
- [ ] `description` includes WHAT
- [ ] `description` includes WHEN (triggers)
- [ ] `description` under 1024 chars
- [ ] No `<` or `>` characters
- [ ] All quotes properly closed

---

## Common Errors

### Missing Delimiters

```yaml
# ✗ Wrong - no delimiters
name: my-skill
description: Does things

# ✓ Correct
---
name: my-skill
description: Does things
---
```

### Unclosed Quotes

```yaml
# ✗ Wrong
description: "Does things

# ✓ Correct
description: "Does things"
```

### Invalid YAML Indentation

```yaml
# ✗ Wrong - inconsistent indentation
metadata:
  author: Name
   version: 1.0.0

# ✓ Correct - consistent 2-space indent
metadata:
  author: Name
  version: 1.0.0
```

### Reserved Names

```yaml
# ✗ Wrong - reserved prefixes
name: claude-assistant
name: anthropic-helper

# ✓ Correct
name: ai-assistant
name: workflow-helper
```
