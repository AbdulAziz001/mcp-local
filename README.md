## Installation

```bash
npm install crash-mcp
```

Or use directly with npx:

```bash
npx crash-mcp
```

### Quick Setup

Most MCP clients use this JSON configuration:

```json
{
  "mcpServers": {
    "crash": {
      "command": "npx",
      "args": ["-y", "crash-mcp"]
    }
  }
}
```

### Configuration by Client

| Client | Setup Method |
|--------|-------------|
| **Claude Code** | `claude mcp add crash -- npx -y crash-mcp` |
| **Cursor** | Add to `~/.cursor/mcp.json` |
| **VS Code** | Add to settings JSON under `mcp.servers` |
| **Claude Desktop** | Add to `claude_desktop_config.json` |
| **Windsurf** | Add to MCP config file |
| **JetBrains** | Settings > Tools > AI Assistant > MCP |
| **Others** | Use standard MCP JSON config above |

<details>
<summary><b>Windows Users</b></summary>

Use the cmd wrapper:

```json
{
  "mcpServers": {
    "crash": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "crash-mcp"]
    }
  }
}
```

</details>

<details>
<summary><b>With Environment Variables</b></summary>

```json
{
  "mcpServers": {
    "crash": {
      "command": "npx",
      "args": ["-y", "crash-mcp"],
      "env": {
        "CRASH_STRICT_MODE": "false",
        "MAX_HISTORY_SIZE": "100",
        "CRASH_OUTPUT_FORMAT": "console",
        "CRASH_SESSION_TIMEOUT": "60",
        "CRASH_MAX_BRANCH_DEPTH": "5"
      }
    }
  }
}
```

</details>

<details>
<summary><b>Using Docker</b></summary>

```dockerfile
FROM node:18-alpine
WORKDIR /app
RUN npm install -g crash-mcp
CMD ["crash-mcp"]
```

```json
{
  "mcpServers": {
    "crash": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "crash-mcp"]
    }
  }
}
```

</details>

<details>
<summary><b>Alternative Runtimes</b></summary>

**Bun:**
```json
{ "command": "bunx", "args": ["-y", "crash-mcp"] }
```

**Deno:**
```json
{
  "command": "deno",
  "args": ["run", "--allow-env", "--allow-net", "npm:crash-mcp"]
}
```

</details>

---

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `CRASH_STRICT_MODE` | `false` | Enable strict validation (requires specific prefixes) |
| `MAX_HISTORY_SIZE` | `100` | Maximum steps to retain in history |
| `CRASH_OUTPUT_FORMAT` | `console` | Output format: `console`, `json`, `markdown` |
| `CRASH_NO_COLOR` | `false` | Disable colored console output |
| `CRASH_SESSION_TIMEOUT` | `60` | Session timeout in minutes |
| `CRASH_MAX_BRANCH_DEPTH` | `5` | Maximum branch nesting depth |
| `CRASH_ENABLE_SESSIONS` | `false` | Enable session management |

---

## Usage

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `step_number` | integer | Sequential step number (starts at 1) |
| `estimated_total` | integer | Estimated total steps (adjustable) |
| `purpose` | string | Step category: analysis, action, validation, exploration, hypothesis, correction, planning, or custom |
| `context` | string | What's already known to avoid redundancy |
| `thought` | string | Current reasoning process |
| `outcome` | string | Expected or actual result |
| `next_action` | string/object | Next action (simple string or structured with tool details) |
| `rationale` | string | Why this next action was chosen |

### Optional Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `is_final_step` | boolean | Mark as final step to complete reasoning |
| `confidence` | number | Confidence level 0-1 (warnings below 0.5) |
| `uncertainty_notes` | string | Describe doubts or assumptions |
| `revises_step` | integer | Step number being corrected |
| `revision_reason` | string | Why revision is needed |
| `branch_from` | integer | Step to branch from |
| `branch_id` | string | Unique branch identifier |
| `branch_name` | string | Human-readable branch name |
| `dependencies` | integer[] | Step numbers this depends on |
| `session_id` | string | Group related reasoning chains |
| `tools_used` | string[] | Tools used in this step |
| `external_context` | object | External data relevant to step |

---

## Examples

### Basic Usage

```json
{
  "step_number": 1,
  "estimated_total": 3,
  "purpose": "analysis",
  "context": "User requested optimization of database queries",
  "thought": "I need to first understand the current query patterns before proposing changes",
  "outcome": "Identified slow queries for optimization",
  "next_action": "analyze query execution plans",
  "rationale": "Understanding execution plans will reveal bottlenecks"
}
```

### With Confidence and Final Step

```json
{
  "step_number": 3,
  "estimated_total": 3,
  "purpose": "summary",
  "context": "Analyzed queries and tested index optimizations",
  "thought": "The index on user_id reduced query time from 2s to 50ms",
  "outcome": "Performance issue resolved with new index",
  "next_action": "document the change",
  "rationale": "Team should know about the optimization",
  "confidence": 0.9,
  "is_final_step": true
}
```

### Revision Example

```json
{
  "step_number": 4,
  "estimated_total": 5,
  "purpose": "correction",
  "context": "Previous analysis missed a critical join condition",
  "thought": "The join was causing a cartesian product, not the index",
  "outcome": "Corrected root cause identification",
  "next_action": "fix the join condition",
  "rationale": "This is the actual performance issue",
  "revises_step": 2,
  "revision_reason": "Overlooked critical join in initial analysis"
}
```

### Branching Example

```json
{
  "step_number": 3,
  "estimated_total": 6,
  "purpose": "exploration",
  "context": "Two optimization approaches identified",
  "thought": "Exploring the indexing approach first as it's lower risk",
  "outcome": "Branch created for index optimization testing",
  "next_action": "test index performance",
  "rationale": "This approach has lower risk than query rewrite",
  "branch_from": 2,
  "branch_id": "index-optimization",
  "branch_name": "Index-based optimization"
}
```

---

## When to Use CRASH

**Good fit:**
- Complex multi-step problem solving
- Code analysis and optimization
- System design with multiple considerations
- Debugging requiring systematic investigation
- Exploring multiple solution paths
- Tasks where you need to track confidence

**Not needed:**
- Simple, single-step tasks
- Pure information retrieval
- Deterministic procedures with no uncertainty

---

## Development

```bash
npm install        # Install dependencies
npm run build      # Build TypeScript
npm run dev        # Run with MCP inspector
npm start          # Start built server
```

---

## Troubleshooting

<details>
<summary><b>Module Not Found Errors</b></summary>

Try using `bunx` instead of `npx`:

```json
{ "command": "bunx", "args": ["-y", "crash-mcp"] }
```

</details>

<details>
<summary><b>ESM Resolution Issues</b></summary>

Try the experimental VM modules flag:

```json
{ "args": ["-y", "--node-options=--experimental-vm-modules", "crash-mcp"] }
```

</details>

---

## Credits

- [MCP Sequential Thinking Server](https://github.com/modelcontextprotocol/servers/blob/main/src/sequentialthinking) - Primary inspiration
- [MCP Protocol Specification](https://modelcontextprotocol.io/)

## Author

**Nikko Gonzales** - [nikkoxgonzales](https://github.com/nikkoxgonzales)

## License

MIT