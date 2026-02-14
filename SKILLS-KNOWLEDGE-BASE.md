# Skills Knowledge Base for Claude Code

A comprehensive reference for building, testing, and distributing Claude skills.

## Table of Contents

1. [Fundamentals](#fundamentals)
2. [Skill Structure](#skill-structure)
3. [YAML Frontmatter Reference](#yaml-frontmatter-reference)
4. [Writing Effective Skills](#writing-effective-skills)
5. [Patterns & Use Cases](#patterns--use-cases)
6. [Testing & Iteration](#testing--iteration)
7. [Troubleshooting](#troubleshooting)
8. [Quick Checklist](#quick-checklist)

---

## Fundamentals

### What is a Skill?

A skill is a folder containing instructions that teach Claude how to handle specific tasks or workflows. Instead of re-explaining preferences in every conversation, skills let you teach Claude once.

### Core Design Principles

**Progressive Disclosure (Three Levels)**
1. **YAML frontmatter** - Always loaded in system prompt. Just enough for Claude to know WHEN to use the skill.
2. **SKILL.md body** - Loaded when skill is relevant. Contains full instructions.
3. **Linked files** - Additional files Claude discovers as needed (references/, scripts/).

**Composability**
Claude can load multiple skills simultaneously. Design skills to work alongside others.

**Portability**
Skills work identically across Claude.ai, Claude Code, and API without modification.

---

## Skill Structure

```
skill-name/
├── SKILL.md              # REQUIRED - main skill file
├── scripts/              # Optional - executable code
│   ├── process_data.py
│   └── validate.sh
├── references/           # Optional - documentation loaded as needed
│   ├── api-guide.md
│   └── examples/
└── assets/               # Optional - templates, fonts, icons
    └── report-template.md
```

### Critical Rules

| Rule | Correct | Wrong |
|------|---------|-------|
| File naming | `SKILL.md` (exact) | `skill.md`, `SKILL.MD` |
| Folder naming | `kebab-case` | `camelCase`, `snake_case`, spaces |
| README | No README.md inside skill | Including README.md |

---

## YAML Frontmatter Reference

### Minimal Required Format

```yaml
---
name: skill-name-in-kebab-case
description: What it does and when to use it. Include specific trigger phrases.
---
```

### All Optional Fields

```yaml
---
name: skill-name
description: [required]
license: MIT                    # For open-source skills
compatibility: "Requires Python 3.11+"  # Environment requirements (1-500 chars)
metadata:                       # Custom fields
  author: Your Name
  version: 1.0.0
  mcp-server: server-name
  category: productivity
  tags: [automation, workflow]
---
```

### Field Requirements

| Field | Required | Notes |
|-------|----------|-------|
| `name` | ✅ | kebab-case only, must match folder name |
| `description` | ✅ | MUST include WHAT + WHEN. Under 1024 chars. No XML tags |
| `license` | ❌ | MIT, Apache-2.0, etc. |
| `compatibility` | ❌ | Environment requirements |
| `metadata` | ❌ | Custom key-value pairs |

### Security Restrictions

**Forbidden in frontmatter:**
- XML angle brackets (`<` `>`) - frontmatter appears in system prompt
- Skills named with "claude" or "anthropic" (reserved)

---

## Writing Effective Skills

### The Description Field (Most Important)

Structure: `[What it does] + [When to use it] + [Key capabilities]`

**✅ Good Examples:**

```yaml
# Specific and actionable
description: Analyzes Figma design files and generates developer handoff documentation. Use when user uploads .fig files, asks for "design specs", "component documentation", or "design-to-code handoff".

# Includes trigger phrases
description: Manages Linear project workflows including sprint planning, task creation, and status tracking. Use when user mentions "sprint", "Linear tasks", "project planning", or asks to "create tickets".

# Clear value proposition
description: End-to-end customer onboarding workflow for PayFlow. Handles account creation, payment setup, and subscription management. Use when user says "onboard new customer", "set up subscription", or "create PayFlow account".
```

**❌ Bad Examples:**

```yaml
# Too vague
description: Helps with projects.

# Missing triggers
description: Creates sophisticated multi-page documentation systems.

# Too technical, no user triggers
description: Implements the Project entity model with hierarchical relationships.
```

### SKILL.md Body Template

```markdown
---
name: your-skill
description: [What + When + Capabilities]
---

# Your Skill Name

# Instructions

## Step 1: [First Major Step]
Clear explanation of what happens.

Example:
```bash
python scripts/fetch_data.py --project-id PROJECT_ID
```

Expected output: [describe what success looks like]

## Step 2: [Next Step]
...

# Examples

## Example 1: [common scenario]
User says: "Set up a new marketing campaign"
Actions:
1. Fetch existing campaigns via MCP 
2. Create new campaign with provided parameters
Result: Campaign created with confirmation link

# Troubleshooting

## Error: [Common error message]
Cause: [Why it happens]
Solution: [How to fix]
```

### Best Practices for Instructions

**Be Specific and Actionable**

```markdown
✅ Good:
Run `python scripts/validate.py --input {filename}` to check data format.
If validation fails, common issues include:
- Missing required fields (add them to the CSV)
- Invalid date formats (use YYYY-MM-DD)

❌ Bad:
Validate the data before proceeding.
```

**Include Error Handling**

```markdown
# Common Issues

## MCP Connection Failed
If you see "Connection refused":
1. Verify MCP server is running: Check Settings > Extensions
2. Confirm API key is valid
3. Try reconnecting: Settings > Extensions > [Your Service] > Reconnect
```

**Reference Bundled Resources Clearly**

```markdown
Before writing queries, consult `references/api-patterns.md` for:
- Rate limiting guidance
- Pagination patterns
- Error codes and handling
```

---

## Patterns & Use Cases

### Category 1: Document & Asset Creation

**Use for:** Creating consistent, high-quality output (documents, presentations, apps, designs, code)

**Key techniques:**
- Embedded style guides and brand standards
- Template structures for consistent output
- Quality checklists before finalizing
- No external tools required

### Category 2: Workflow Automation

**Use for:** Multi-step processes that benefit from consistent methodology

**Key techniques:**
- Step-by-step workflow with validation gates
- Templates for common structures
- Built-in review and improvement suggestions
- Iterative refinement loops

### Category 3: MCP Enhancement

**Use for:** Workflow guidance to enhance MCP server tool access

**Key techniques:**
- Coordinates multiple MCP calls in sequence
- Embeds domain expertise
- Provides context users would otherwise need to specify
- Error handling for common MCP issues

---

### Implementation Patterns

#### Pattern 1: Sequential Workflow Orchestration

```markdown
# Workflow: Onboard New Customer

## Step 1: Create Account
Call MCP tool: `create_customer`
Parameters: name, email, company

## Step 2: Setup Payment
Call MCP tool: `setup_payment_method`
Wait for: payment method verification

## Step 3: Create Subscription
Call MCP tool: `create_subscription`
Parameters: plan_id, customer_id (from Step 1)

## Step 4: Send Welcome Email
Call MCP tool: `send_email`
Template: welcome_email_template
```

#### Pattern 2: Multi-MCP Coordination

```markdown
# Phase 1: Design Export (Figma MCP)
1. Export design assets from Figma
2. Generate design specifications
3. Create asset manifest

# Phase 2: Asset Storage (Drive MCP)
1. Create project folder in Drive
2. Upload all assets
3. Generate shareable links

# Phase 3: Task Creation (Linear MCP)
1. Create development tasks
2. Attach asset links to tasks
3. Assign to engineering team

# Phase 4: Notification (Slack MCP)
1. Post handoff summary to #engineering
2. Include asset links and task references
```

#### Pattern 3: Iterative Refinement

```markdown
# Iterative Report Creation

## Initial Draft
1. Fetch data via MCP
2. Generate first draft report
3. Save to temporary file

## Quality Check
1. Run validation script: `scripts/check_report.py`
2. Identify issues:
   - Missing sections
   - Inconsistent formatting
   - Data validation errors

## Refinement Loop
1. Address each identified issue
2. Regenerate affected sections
3. Re-validate
4. Repeat until quality threshold met

## Finalization
1. Apply final formatting
2. Generate summary
3. Save final version
```

#### Pattern 4: Context-Aware Tool Selection

```markdown
# Smart File Storage

## Decision Tree
1. Check file type and size
2. Determine best storage location:
   - Large files (>10MB): Use cloud storage MCP
   - Collaborative docs: Use Notion/Docs MCP
   - Code files: Use GitHub MCP
   - Temporary files: Use local storage

## Execute Storage
Based on decision:
- Call appropriate MCP tool
- Apply service-specific metadata
- Generate access link

## Provide Context to User
Explain why that storage was chosen
```

#### Pattern 5: Domain-Specific Intelligence

```markdown
# Payment Processing with Compliance

## Before Processing (Compliance Check)
1. Fetch transaction details via MCP
2. Apply compliance rules:
   - Check sanctions lists
   - Verify jurisdiction allowances
   - Assess risk level
3. Document compliance decision

## Processing
IF compliance passed:
  - Call payment processing MCP tool
  - Apply appropriate fraud checks
  - Process transaction
ELSE:
  - Flag for review
  - Create compliance case

## Audit Trail
- Log all compliance checks
- Record processing decisions
- Generate audit report
```

---

## Testing & Iteration

### Testing Levels

1. **Manual testing in Claude.ai** - Fast iteration, no setup
2. **Scripted testing in Claude Code** - Repeatable validation
3. **Programmatic testing via API** - Systematic evaluation suites

### Pro Tip

Iterate on a single challenging task until Claude succeeds, then extract the winning approach into a skill. This leverages Claude's in-context learning.

### Test Categories

#### 1. Triggering Tests

```yaml
Should trigger:
- "Help me set up a new ProjectHub workspace"
- "I need to create a project in ProjectHub"
- "Initialize a ProjectHub project for Q4 planning"

Should NOT trigger:
- "What's the weather in San Francisco?"
- "Help me write Python code"
- "Create a spreadsheet"
```

#### 2. Functional Tests

```yaml
Test: Create project with 5 tasks
Given: Project name "Q4 Planning", 5 task descriptions
When: Skill executes workflow
Then:
  - Project created in ProjectHub
  - 5 tasks created with correct properties
  - All tasks linked to project
  - No API errors
```

#### 3. Performance Comparison

```yaml
Without skill:
- User provides instructions each time
- 15 back-and-forth messages
- 3 failed API calls requiring retry
- 12,000 tokens consumed

With skill:
- Automatic workflow execution
- 2 clarifying questions only
- 0 failed API calls
- 6,000 tokens consumed
```

### Success Criteria

**Quantitative:**
- Skill triggers on 90% of relevant queries
- Completes workflow in X tool calls
- 0 failed API calls per workflow

**Qualitative:**
- Users don't need to prompt about next steps
- Workflows complete without user correction
- Consistent results across sessions

### Iteration Signals

| Signal Type | Symptoms | Solution |
|-------------|----------|----------|
| **Undertriggering** | Skill doesn't load when it should, users manually enabling | Add more trigger keywords to description |
| **Overtriggering** | Skill loads for unrelated queries, users disabling | Add negative triggers, be more specific |
| **Execution Issues** | Inconsistent results, API failures | Improve instructions, add error handling |

---

## Troubleshooting

### Skill Won't Upload

**Error: "Could not find SKILL.md"**
- Rename to exactly `SKILL.md` (case-sensitive)
- Verify: `ls -la | grep SKILL`

**Error: "Invalid frontmatter"**

```yaml
# Wrong - missing delimiters
name: my-skill
description: Does things

# Wrong - unclosed quotes
name: my-skill
description: "Does things

# Correct
---
name: my-skill
description: Does things
---
```

**Error: "Invalid skill name"**

```yaml
# Wrong
name: My Cool Skill

# Correct
name: my-cool-skill
```

### Skill Doesn't Trigger

**Quick debug:** Ask Claude: "When would you use the [skill name] skill?"

**Fixes:**
- Make description more specific
- Add trigger phrases users actually say
- Mention relevant file types

### Skill Triggers Too Often

**Add negative triggers:**

```yaml
description: Advanced data analysis for CSV files. Use for statistical modeling, regression, clustering. Do NOT use for simple data exploration (use data-viz skill instead).
```

**Clarify scope:**

```yaml
description: PayFlow payment processing for e-commerce. Use specifically for online payment workflows, not for general financial queries.
```

### MCP Connection Issues

1. Verify MCP server connected: Settings > Extensions
2. Check authentication (API keys, OAuth tokens)
3. Test MCP independently: "Use [Service] MCP to fetch my projects"
4. Verify tool names match MCP server docs (case-sensitive)

### Instructions Not Followed

**Common causes:**
- Instructions too verbose → Keep concise, use lists
- Instructions buried → Put critical items at top
- Ambiguous language → Be explicit

```markdown
# Bad
Make sure to validate things properly

# Good
CRITICAL: Before calling create_project, verify:
- Project name is non-empty
- At least one team member assigned
- Start date is not in the past
```

### Large Context Issues

**Symptoms:** Slow responses, degraded quality

**Fixes:**
- Move detailed docs to `references/`
- Keep SKILL.md under 5,000 words
- Reduce enabled skills if > 20-50 active

---

## Quick Checklist

### Before You Start
- [ ] Identified 2-3 concrete use cases
- [ ] Tools identified (built-in or MCP)
- [ ] Planned folder structure

### During Development
- [ ] Folder named in kebab-case
- [ ] SKILL.md exists (exact spelling)
- [ ] YAML has `---` delimiters
- [ ] `name` field: kebab-case, no spaces/capitals
- [ ] `description` includes WHAT and WHEN
- [ ] No XML tags anywhere
- [ ] Instructions are clear and actionable
- [ ] Error handling included
- [ ] Examples provided
- [ ] References clearly linked

### Before Upload
- [ ] Triggers on obvious tasks
- [ ] Triggers on paraphrased requests
- [ ] Doesn't trigger on unrelated topics
- [ ] Functional tests pass
- [ ] Compressed as .zip (if uploading to Claude.ai)

### After Upload
- [ ] Test in real conversations
- [ ] Monitor for under/over-triggering
- [ ] Collect feedback
- [ ] Iterate on description and instructions

---

## Resources

- **Skills API**: `/v1/skills` endpoint
- **Example Skills**: `anthropics/skills` on GitHub
- **skill-creator**: Built into Claude.ai and Claude Code
- **Debugging**: Ask Claude "When would you use [skill-name] skill?"
