
# Skills Troubleshooting Quick Reference

Fast fixes for common skill issues.

---

## Upload Errors

### "Could not find SKILL.md"

**Cause:** File not named exactly `SKILL.md`

**Fix:**
```bash
# Check current name
ls -la | grep -i skill

# Rename if needed
mv skill.md SKILL.md
mv SKILL.MD SKILL.md
```

---

### "Invalid frontmatter"

**Cause:** YAML formatting issue

**Common mistakes:**

```yaml
# ✗ Missing delimiters
name: my-skill
description: Does things

# ✗ Unclosed quote
description: "Does things

# ✗ Bad indentation
metadata:
  author: Name
   version: 1.0  # wrong indent

# ✓ Correct
---
name: my-skill
description: Does things
---
```

---

### "Invalid skill name"

**Cause:** Name format violation

```yaml
# ✗ Wrong
name: My Cool Skill    # spaces
name: myCoolSkill      # camelCase
name: my_cool_skill    # underscores

# ✓ Correct
name: my-cool-skill
```

---

## Triggering Issues

### Skill doesn't trigger

**Debug:** Ask Claude: "When would you use the [skill-name] skill?"

**Fixes:**
1. Add specific trigger phrases to description
2. Include relevant keywords users say
3. Mention file types if applicable

```yaml
# ✗ Too vague
description: Helps with projects

# ✓ Specific triggers
description: Creates project plans. Use when user says "plan project", "create timeline", or "project roadmap".
```

---

### Skill triggers too often

**Fixes:**

1. **Add negative triggers:**
```yaml
description: Advanced data analysis. Do NOT use for simple charts (use data-viz instead).
```

2. **Be more specific:**
```yaml
# ✗ Too broad
description: Processes documents

# ✓ Specific
description: Processes PDF legal contracts for clause extraction
```

3. **Clarify scope:**
```yaml
description: PayFlow payments for e-commerce only, not general finance.
```

---

## Execution Issues

### Instructions not followed

**Causes & Fixes:**

| Cause | Fix |
|-------|-----|
| Too verbose | Keep concise, use bullets |
| Critical info buried | Put important stuff at top |
| Ambiguous language | Be explicit |

```markdown
# ✗ Ambiguous
Validate things properly before proceeding

# ✓ Explicit
CRITICAL: Before calling create_project, verify:
- Project name is non-empty
- At least one team member assigned
- Start date is not in the past
```

---

### MCP connection failed

**Checklist:**

1. Check connection: Settings > Extensions > [Service]
2. Verify "Connected" status
3. Test MCP directly: "Use [Service] to fetch my projects"
4. Check API key validity
5. Verify tool names match docs (case-sensitive)

---

### Slow/degraded responses

**Causes:**
- SKILL.md too large
- Too many skills enabled

**Fixes:**
1. Move detailed docs to `references/`
2. Keep SKILL.md under 5,000 words
3. Disable unused skills (aim for < 20-50 active)

---

## Quick Validation

Run before upload:

```bash
python validate_skill.py /path/to/skill
```

**Manual checks:**
- [ ] `SKILL.md` exists (exact case)
- [ ] Folder is kebab-case
- [ ] YAML has `---` delimiters
- [ ] `name` matches folder
- [ ] `description` has WHAT + WHEN
- [ ] No `<>` in frontmatter

---

## Debug Commands

```bash
# Check file naming
ls -la | grep -i skill

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('SKILL.md').read().split('---')[1])"

# Count words in body
wc -w SKILL.md

# Check for XML tags
grep -n '[<>]' SKILL.md
```

---

## Getting Help

1. **Ask Claude:** "Review this skill and suggest improvements"
2. **Use skill-creator:** "Help me fix this skill using skill-creator"
3. **Validate:** Run `validate_skill.py` for automated checks
