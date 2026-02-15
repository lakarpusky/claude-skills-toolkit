---
name: example-workflow
description: |
  Example skill demonstrating all skill patterns and best practices.
  Use when user asks for "skill examples", "skill patterns", or 
  wants to learn about skill development.
license: MIT
metadata:
  author: Skills Guide
  version: 1.0.0
  category: examples
  tags:
    - example
    - learning
    - patterns
---

# Example Workflow Skill

This skill demonstrates proper structure and common patterns for building skills.

---

## Instructions

### Step 1: Understand the Request

Analyze user input to determine:
- What outcome they want
- What tools/data are needed
- Any constraints or preferences

### Step 2: Execute Workflow

Based on analysis:

**For document creation:**
1. Gather required information
2. Apply template from `assets/`
3. Generate content
4. Run quality checks

**For MCP operations:**
1. Verify MCP connection
2. Make API calls in sequence
3. Validate each response
4. Handle errors gracefully

### Step 3: Deliver Results

1. Summarize what was done
2. Provide output/links
3. Suggest next steps if applicable

---

## Examples

### Example 1: Simple Task

**User says:** "Create a project checklist"

**Actions:**
1. Ask for project name and key milestones
2. Generate checklist from template
3. Format as markdown

**Result:** Formatted checklist ready for use

### Example 2: Multi-Step Workflow

**User says:** "Set up a new client workspace"

**Actions:**
1. Create project folder (Phase 1)
2. Generate standard documents (Phase 2)
3. Set up tracking (Phase 3)
4. Send notification (Phase 4)

**Result:** Complete workspace with all components linked

---

## Error Handling

### Error: Missing Required Input

**Cause:** User didn't provide necessary information

**Solution:**
1. Identify missing fields
2. Ask user for specific missing items
3. Provide examples of expected format

### Error: Validation Failed

**Cause:** Generated content didn't meet quality threshold

**Solution:**
1. Log specific validation failures
2. Attempt automated fix if possible
3. Request user guidance if needed

---

## References

- See `references/patterns.md` for detailed pattern documentation
- See `references/yaml-frontmatter.md` for YAML field reference
- See `scripts/validate_skill.py` for validation logic

---

## Best Practices Demonstrated

1. **Clear structure** - Organized with headers and sections
2. **Specific examples** - Shows actual user phrases and outcomes
3. **Error handling** - Covers common failure cases
4. **References linked** - Points to additional resources
5. **Actionable steps** - Each instruction is clear and specific
