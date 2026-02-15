
# Skill Implementation Patterns

Quick reference for common skill patterns with copy-paste examples.

---

## Pattern 1: Sequential Workflow Orchestration

**Use when:** Multi-step processes in specific order.

```markdown
# Workflow: [Workflow Name]

## Step 1: [Action Name]
Call MCP tool: `tool_name`
Parameters: param1, param2
**Validate:** Check response.field exists

## Step 2: [Next Action]
Call MCP tool: `next_tool`
Parameters: 
  - id: {from step 1}
  - config: {...}
**Wait for:** Condition to be met

## Step 3: [Final Action]
Call MCP tool: `final_tool`
**Result:** Describe outcome
```

**Key techniques:**
- Explicit step ordering
- Dependencies between steps  
- Validation at each stage
- Rollback instructions for failures

---

## Pattern 2: Multi-MCP Coordination

**Use when:** Workflows span multiple services.

```markdown
# Cross-Service Workflow

## Phase 1: [Source Service] (MCP: source-server)
1. Fetch data from source
2. Transform format
3. Stage for transfer

## Phase 2: [Target Service] (MCP: target-server)  
1. Receive transformed data
2. Create resources
3. Confirm completion

## Phase 3: Notification (MCP: slack/email)
1. Send confirmation message
2. Include links from both services
```

**Key techniques:**
- Clear phase separation
- Data passing between MCPs
- Validation before next phase
- Centralized error handling

---

## Pattern 3: Iterative Refinement

**Use when:** Output quality improves with iteration.

```markdown
# Iterative [Output Type] Creation

## Initial Draft
1. Gather inputs
2. Generate first draft
3. Save to temporary file

## Quality Check
Run validation: `scripts/check_quality.py`
Identify issues:
- Missing sections
- Formatting inconsistencies
- Data validation errors

## Refinement Loop
1. Address each issue
2. Regenerate affected sections
3. Re-validate
4. Repeat until threshold met (max 3 iterations)

## Finalization
1. Apply final formatting
2. Generate summary
3. Save final version
```

**Key techniques:**
- Explicit quality criteria
- Validation scripts
- Iteration limits
- Clear stop conditions

---

## Pattern 4: Context-Aware Tool Selection

**Use when:** Same outcome, different tools by context.

```markdown
# Smart [Action] Selection

## Decision Tree
Analyze input:
- If condition A → Use tool_a
- If condition B → Use tool_b  
- If condition C → Use tool_c
- Default → Use tool_default

## Execute Selected Tool
Based on decision:
1. Call appropriate tool
2. Apply tool-specific config
3. Handle tool-specific response

## Explain Choice
Tell user: "Used [tool] because [reason]"
```

**Key techniques:**
- Clear decision criteria
- Fallback options
- Transparency about choices

---

## Pattern 5: Domain-Specific Intelligence

**Use when:** Skill adds specialized knowledge beyond tool access.

```markdown
# [Domain] Processing with [Constraint]

## Pre-Check ([Constraint] Validation)
1. Fetch details via MCP
2. Apply [domain] rules:
   - Rule 1: Check X
   - Rule 2: Verify Y
   - Rule 3: Assess Z
3. Document decision

## Processing
IF validation passed:
  - Execute main action
  - Apply domain-specific handling
  - Complete process
ELSE:
  - Flag for review
  - Create exception case
  - Notify stakeholders

## Audit Trail
- Log all checks performed
- Record decisions made
- Generate audit report
```

**Key techniques:**
- Domain expertise in logic
- Validation before action
- Comprehensive documentation
- Clear governance

---

## Pattern 6: Template-Based Generation

**Use when:** Creating consistent formatted output.

```markdown
# Generate [Output Type]

## Load Template
Use template from: `assets/[template-name].md`

## Gather Data
Required inputs:
- field_1: [description]
- field_2: [description]
- field_3: [description]

## Apply Template
Replace placeholders:
- {{FIELD_1}} → user input
- {{FIELD_2}} → computed value
- {{FIELD_3}} → fetched data

## Quality Checks
Before finalizing:
- [ ] All placeholders replaced
- [ ] Formatting consistent
- [ ] Links valid
- [ ] Spell check passed

## Output
Save to: [location]
Format: [format]
```

**Key techniques:**
- Reusable templates
- Clear placeholder syntax
- Quality checklists
- Consistent output format

---

## Pattern 7: Error Recovery with Retry

**Use when:** Operations may fail transiently.

```markdown
# [Operation] with Retry

## Attempt Operation
```
max_retries = 3
retry_delay = [1s, 5s, 15s]

for attempt in 1..max_retries:
    try:
        result = call_mcp_tool(...)
        if result.success:
            return result
    except TransientError:
        wait(retry_delay[attempt])
        continue
    except PermanentError:
        fail_immediately()

fail_with_all_attempts_exhausted()
```

## Error Classification
**Retry-able errors:**
- Connection timeout
- Rate limit (429)
- Server error (5xx)

**Non-retry-able errors:**
- Authentication failed (401)
- Not found (404)
- Validation error (400)

## Fallback Actions
If all retries exhausted:
1. Log failure details
2. Notify user with context
3. Suggest manual intervention
```

**Key techniques:**
- Exponential backoff
- Error classification
- Clear fallback path
- User notification

---

## Quick Reference: Trigger Phrase Patterns

### Action-Based Triggers
```yaml
description: ... Use when user says "create X", "set up Y", "initialize Z"
```

### Entity-Based Triggers
```yaml
description: ... Use when user mentions "[service name]", "[entity type]", "[domain term]"
```

### File-Based Triggers
```yaml
description: ... Use when user uploads .ext files or asks about "[file type]"
```

### Negative Triggers
```yaml
description: ... Use for X. Do NOT use for Y (use [other-skill] instead).
```

---

## Anti-Patterns to Avoid

### ❌ Vague Description
```yaml
description: Helps with projects
```

### ❌ Missing Triggers
```yaml
description: Creates sophisticated documentation systems
```

### ❌ Too Technical
```yaml
description: Implements Project entity with hierarchical relationships
```

### ❌ Ambiguous Instructions
```markdown
Make sure to validate things properly before proceeding
```

### ❌ No Error Handling
```markdown
1. Call API
2. Process response
3. Done
```

### ❌ Buried Critical Info
```markdown
[500 words of context]
IMPORTANT: Always do X first
[more content]
```
