
---
name: service-workflow
description: |
  [SERVICE] integration for [DOMAIN] workflows.
  Use when user mentions "[trigger1]", "[trigger2]", or asks to "[action]".
  Requires [SERVICE] MCP server connected.
metadata:
  author: Your Name
  version: 1.0.0
  mcp-server: service-name
---

# [Service] Workflow Skill

Orchestrates [SERVICE] MCP tools for common [DOMAIN] workflows.

---

## Prerequisites

- [SERVICE] MCP server connected (Settings > Extensions)
- Valid API credentials configured
- Required permissions: [list permissions]

---

## Workflows

### Workflow 1: [Primary Workflow Name]

**Trigger:** User says "X" or "Y"

#### Phase 1: [Setup Phase]

```
Call MCP tool: `service_tool_name`
Parameters:
  - param1: {user_input}
  - param2: default_value
```

**Validate:** Check response contains expected_field

#### Phase 2: [Execution Phase]

```
Call MCP tool: `another_tool`
Parameters:
  - id: {from_phase_1}
  - config: {...}
```

**Validate:** Confirm action completed

#### Phase 3: [Completion Phase]

```
Call MCP tool: `notification_tool`
Parameters:
  - message: "Workflow complete"
  - link: {result_url}
```

**Result:** Summarize outcome with link

---

### Workflow 2: [Secondary Workflow]

**Trigger:** User says "A" or "B"

[Similar structure...]

---

## Multi-MCP Coordination

### Cross-Service Workflow

When data needs to flow between services:

#### Phase 1: [Source Service] (MCP: source-server)
1. Fetch data
2. Transform format
3. Stage for transfer

#### Phase 2: [Target Service] (MCP: target-server)
1. Receive data
2. Create resources
3. Confirm completion

#### Phase 3: Notification (MCP: notification-server)
1. Send confirmation
2. Include links from both services

---

## Error Handling

### MCP Connection Failed

**Symptoms:** "Connection refused" or timeout

**Resolution:**
1. Check Settings > Extensions > [Service]
2. Verify status shows "Connected"
3. If disconnected, click Reconnect
4. Verify API key is valid and not expired

### Tool Not Found

**Symptoms:** "Unknown tool: tool_name"

**Resolution:**
1. Verify MCP server version matches expected
2. Check tool name spelling (case-sensitive)
3. Consult MCP server documentation

### Rate Limited

**Symptoms:** "429 Too Many Requests"

**Resolution:**
1. Wait for rate limit window to reset
2. Reduce batch size if applicable
3. Add delays between sequential calls

---

## Best Practices

- Always validate MCP response before proceeding
- Store intermediate results for rollback capability
- Log all MCP calls for audit trail
- Handle partial failures gracefully

---

## References

- MCP Server Docs: [link]
- API Reference: `references/api-guide.md`
- Error Codes: `references/error-codes.md`
