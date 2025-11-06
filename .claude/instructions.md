# Claude Code Instructions for UBL Repository

This file contains specific behavioral instructions for Claude Code when working with the UBL repository.

## Network & Retry Handling

### Overview

The UBL build process requires network access to external services, particularly Google Spreadsheets. Network blocks can occur due to firewall policies, proxy configurations, or security restrictions. When this happens, Claude Code must handle the situation properly rather than continuing without required resources.

### Workflow

```
Operation → Network Block Detected → Report & Stop → User Whitelists → Retry → Success/Failure
```

### When Network Blocks Occur

**See: [`network-handling.md`](network-handling.md)** for complete instructions.

**Quick Reference:**

1. **Detect** - Network block indicated by 403 Forbidden, x-deny-reason header
2. **Stop** - Immediately cease the operation
3. **Report** - Use the 🚫 NETWORK BLOCK DETECTED format
4. **Identify** - Specify the exact blocked domain
5. **Explain** - Clearly state why the domain is needed for the UBL build process
6. **Instruct** - Tell user to whitelist the domain
7. **Wait** - Do not retry automatically or find workarounds

**Critical Domains for UBL:**
- **docs.google.com** - Required for spreadsheet data (source of truth for data model)
- **github.com** - Required for repository operations
- **www.realtaonline.com** - Optional for Réalta publishing service

**Example Response:**
```
🚫 NETWORK BLOCK DETECTED

Blocked Domain: docs.google.com
Reason: x-deny-reason: external-api-not-whitelisted

Why This Domain Is Needed:
The UBL build process requires downloading spreadsheet data from Google Sheets.
The spreadsheets contain the source data model definitions that are transformed
into XSD schemas and JSON schemas.

To Continue:
Please whitelist docs.google.com in your network settings.
Once whitelisted, I can retry the operation.
```

### When User Says "Retry"

**See: [`retry-handling.md`](retry-handling.md)** for complete instructions.

**Quick Reference:**

1. **Recognize** - User says "try again", "retry", or similar phrases
2. **Recall** - Retrieve the last failed operation from memory
3. **Acknowledge** - Brief confirmation: "Retrying [operation]..."
4. **Execute** - Run the EXACT same command with EXACT same parameters
5. **Handle Result**:
   - **Success** → Continue with the task
   - **Same Error** → Verify user fixed the issue, provide troubleshooting
   - **Different Error** → Report new error, follow appropriate handling

**DO NOT:**
- ❌ Ask user "What do you want me to retry?"
- ❌ Modify the command or parameters
- ❌ Retry automatically without user instruction
- ❌ Continue without required resources

**DO:**
- ✅ Remember the last failed command automatically
- ✅ Re-execute the exact operation when user says retry
- ✅ Store context: command, parameters, error, task state
- ✅ Distinguish between same error and new error

**Retry Phrases to Recognize:**
- "Try again"
- "Retry"
- "Try that again"
- "Now try it" (after fixing an issue)
- "It should work now"
- "Continue" (after resolution)

### Complete Workflow Example

```
1. User: "Analyze the Google Spreadsheet configuration"

2. Claude: [Attempts WebFetch to docs.google.com]
   Result: 403 Forbidden (network block)

3. Claude: [Follows network-handling.md]
   🚫 NETWORK BLOCK DETECTED

   Blocked Domain: docs.google.com
   Reason: x-deny-reason: external-api-not-whitelisted

   Why This Domain Is Needed:
   [Explanation about spreadsheet data model]

   To Continue:
   Please whitelist docs.google.com in your network settings.

4. User: [Whitelists docs.google.com]
   "OK, I've whitelisted it. Try again."

5. Claude: [Follows retry-handling.md]
   "Retrying spreadsheet fetch..."
   [Executes exact same WebFetch command]

6. Result: Success
   Claude: [Continues with analysis]
   "Successfully fetched spreadsheet data. Analyzing configuration..."
```

### Memory Requirements

**Within a Session:**
Store after ANY failure:
- Last failed command (tool + parameters)
- Error type and message
- Blocked domain (if network block)
- Task context and progress
- Previous successful steps

**Use for Retry:**
When user says "retry", immediately access this stored information and re-execute.

### Integration with Existing Workflow

These instructions work alongside:
- **CLAUDE.md** - Repository context and knowledge
- **Slash commands** - Guided workflows (may encounter network blocks)
- **Hooks** - Safety validations (separate concern)
- **Build process** - May fail due to network blocks on Google Sheets

### Error Types

#### Network Block (This Workflow)
- Domain blocked by policy
- x-deny-reason present
- Follow `network-handling.md` → `retry-handling.md` workflow

#### Network Error (Different Handling)
- Timeout
- DNS failure
- Temporary connection issues
- May retry with exponential backoff (2s, 4s, 8s, 16s per git protocol)

#### Validation Error (Different Handling)
- Schema validation failure
- Sample validation failure
- Follow validation troubleshooting in docs/

#### Build Error (Different Handling)
- Ant build failure
- XSLT transformation error
- Follow build troubleshooting in docs/

### User Communication Principles

1. **Be Clear** - Exactly what is blocked and why
2. **Be Actionable** - Specific steps to resolve
3. **Be Patient** - Wait for user confirmation
4. **Be Efficient** - Quick retry without repetition
5. **Be Contextual** - Remember what happened and why

### Testing Network Block Handling

If you're working with this repository and encounter a network block:
1. Verify you followed `network-handling.md` format
2. Check that you stopped immediately (didn't retry automatically)
3. Confirm you stored the failed command for retry
4. Test that "retry" works without user repeating context

---

## Other Instructions

(Additional instruction sections can be added here as needed)

---

**Related Files:**
- `network-handling.md` - Detailed network block instructions
- `retry-handling.md` - Detailed retry logic
- `CLAUDE.md` - Repository context (auto-loaded)
- `docs/troubleshooting.md` - Build and validation errors
