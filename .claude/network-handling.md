# Network Block Handling Instructions

## When a Network Block Occurs

**STOP IMMEDIATELY** when you encounter a network error with a blocked domain.

## Detection

Network blocks typically appear as:
- HTTP 403 Forbidden errors
- `x-deny-reason` header in error response
- Connection refused to specific domains
- Blocked host messages

## Required Response Format

When a network block is detected, respond with this **exact format**:

```
🚫 NETWORK BLOCK DETECTED

Blocked Domain: [exact domain that was blocked]
Reason: [x-deny-reason or error message]

Why This Domain Is Needed:
[Clear, concise explanation of what this domain provides and why it's necessary for this task]

To Continue:
Please whitelist this domain in your network settings or proxy configuration.

Once whitelisted, I can retry the operation.
```

## Example Response

```
🚫 NETWORK BLOCK DETECTED

Blocked Domain: docs.google.com
Reason: x-deny-reason: external-api-not-whitelisted

Why This Domain Is Needed:
The UBL build process requires downloading spreadsheet data from Google Sheets.
The spreadsheets contain the source data model definitions that are transformed
into XSD schemas and JSON schemas. Without access to docs.google.com, the build
cannot retrieve the current data model and will fail.

To Continue:
Please whitelist docs.google.com in your network settings or proxy configuration.

Once whitelisted, I can retry the operation.
```

## Critical Rules

### ❌ DO NOT:
- Retry the blocked request automatically
- Try alternative domains or workarounds without user approval
- Continue with partial data or cached versions without explaining
- Attempt to bypass the block
- Make multiple retry attempts
- Proceed with the task as if nothing happened

### ✅ DO:
- Stop immediately when block detected
- Report the exact blocked domain
- Explain clearly why the domain is needed
- Provide the whitelist instruction
- Wait for user confirmation before retrying
- Keep the failed command/context in memory for retry

## Storing Context for Retry

When a network block occurs, internally remember:
1. **The exact command** that failed (tool name and parameters)
2. **The blocked domain**
3. **The task context** (what you were trying to accomplish)
4. **The x-deny-reason** if available

This information will be used when the user says "retry" or "try again".

## After User Whitelists

Once the user confirms the domain is whitelisted:
1. Acknowledge the whitelist
2. Retry the EXACT same operation
3. If it succeeds, continue with the task
4. If it fails again with a different domain, repeat this process
5. If it fails with the same error, ask user to verify the whitelist

## Common Blocked Domains in UBL Repository

Domains that may be blocked:
- **docs.google.com** - Google Spreadsheets (critical for build)
- **spreadsheets.google.com** - Alternative Google Sheets domain
- **github.com** - Repository operations (critical)
- **githubusercontent.com** - Raw file access
- **www.realtaonline.com** - Réalta publishing service (optional)
- **anthropic.com** - Documentation access (optional)
- **oasis-open.org** - OASIS resources (documentation only)

## Severity Levels

### 🔴 CRITICAL - Build Cannot Continue
- docs.google.com (spreadsheet data source)
- github.com (repository access)

### 🟡 IMPORTANT - Reduced Functionality
- www.realtaonline.com (publishing service)
- githubusercontent.com (raw file access)

### 🟢 OPTIONAL - Documentation Only
- anthropic.com (Claude Code docs)
- oasis-open.org (external references)

## Network Error vs Network Block

**Network Block** (this guide applies):
- Specific domain blocked by policy
- x-deny-reason present
- 403 Forbidden or similar policy error

**Network Error** (different handling):
- Timeout
- DNS failure
- Connection refused (no policy block)
- Temporary network issues

For network errors (not blocks), use the retry logic from `retry-handling.md`.

## Integration with Retry Handling

When a network block occurs:
1. **This guide applies FIRST** - Stop and report the block
2. Store the failed command for retry (see `retry-handling.md`)
3. Wait for user to whitelist
4. When user says "retry", use `retry-handling.md` to re-execute

## User Communication

Always be:
- **Clear**: Exactly which domain is blocked
- **Informative**: Why this domain is necessary
- **Actionable**: Specific steps to resolve
- **Patient**: Wait for confirmation before retrying

Remember: Network blocks are **policy decisions** by the user's organization or environment. Respect them and work with the user to resolve them properly.

---

**See also:**
- `retry-handling.md` - For retry logic after resolution
- `instructions.md` - Overall workflow
