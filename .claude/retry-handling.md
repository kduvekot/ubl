# Retry Handling Instructions

## Purpose

Handle user retry requests intelligently by remembering the last failed operation and re-executing it without requiring the user to repeat context.

## Recognizing Retry Commands

When the user says any of these phrases, they want to retry the last failed operation:

### Explicit Retry Phrases
- "Try again"
- "Retry"
- "Try that again"
- "Retry that"
- "Try again with the last command"
- "Run it again"
- "Retry the last operation"
- "Try the previous command again"

### Implicit Retry Phrases
- "Now try it" (after whitelisting a domain)
- "It should work now"
- "Go ahead now"
- "Continue" (after resolving an issue)

### Context Clues
- User mentions fixing something: "I whitelisted the domain, try again"
- User confirms readiness: "OK, I've updated the settings, retry"
- User provides resolution: "I fixed the issue, continue"

## What to Remember

After ANY operation that fails, store:

### 1. The Exact Command
```
Tool: [tool name]
Parameters: [exact parameters as JSON or structured format]
```

Example:
```
Tool: WebFetch
Parameters: {
  "url": "https://docs.google.com/spreadsheets/d/123...",
  "prompt": "Extract all information about..."
}
```

### 2. The Context
```
Task: [what you were trying to accomplish]
Step: [which step in a larger workflow]
Previous Steps: [what was completed successfully]
```

Example:
```
Task: Analyzing Google Spreadsheet configuration
Step: Fetching spreadsheet data
Previous Steps: Read build.py configuration, extracted spreadsheet URLs
```

### 3. The Error
```
Error Type: [network block, validation error, file not found, etc.]
Error Message: [exact error message]
Blocked Domain: [if network block]
```

Example:
```
Error Type: Network block
Error Message: Request failed with status code 403
Blocked Domain: docs.google.com
```

## Retry Execution Process

### Step 1: Recognize Retry Intent
User says "try again" or similar phrase.

### Step 2: Recall Last Failed Operation
Retrieve from memory:
- What command failed
- Why it failed
- What the task was

### Step 3: Acknowledge
Briefly acknowledge you're retrying:
```
"Retrying [brief description of operation]..."
```

Example:
```
"Retrying fetch from docs.google.com..."
```

### Step 4: Re-Execute EXACTLY
Run the **exact same command** with **exact same parameters**.

**DO NOT:**
- Modify the command
- Change parameters
- Skip steps
- Assume what the user meant

**DO:**
- Execute the identical operation
- Use the same tool with same parameters
- Continue from where it failed

### Step 5: Handle Result

#### Scenario A: Success ✅
- Continue with the task as if the original command had succeeded
- Move to the next step in the workflow
- No need to over-explain the success

Example:
```
"Successfully fetched spreadsheet data. Now analyzing configuration..."
```

#### Scenario B: Same Error 🔄
- Report that the same error occurred
- Verify with user that they completed the fix
- Provide additional troubleshooting

Example:
```
"Still getting the same network block on docs.google.com.

Can you verify:
- The domain is whitelisted in your proxy/firewall?
- No typos in the whitelist entry?
- The whitelist has been saved and applied?
"
```

#### Scenario C: Different Error 🆕
- Report the new error
- This might indicate partial progress
- Follow appropriate error handling for the new error type

Example:
```
"The network block is resolved, but now getting a different error:
HTTP 404 - Spreadsheet not found

This suggests:
- The domain is now accessible ✓
- But the spreadsheet URL may be incorrect or the spreadsheet was deleted
"
```

## Multiple Retries in Sequence

If user retries multiple times:

### First Retry
- Re-execute the command
- Report the result

### Second Retry (Same Error)
- Re-execute the command
- Suggest verification steps
- Ask if user needs help troubleshooting

### Third Retry (Same Error)
- Re-execute the command
- Provide detailed troubleshooting
- Consider if there's a fundamental issue
- Suggest alternative approaches if appropriate

Example:
```
"This is the third retry with the same error. Let's troubleshoot:

1. Can you run this test command in your terminal:
   curl -I https://docs.google.com

2. What response do you get?

This will help determine if the issue is with the whitelist configuration
or something else in your network setup."
```

## DO NOT Ask User to Repeat Information

### ❌ WRONG:
```
User: "Try again"
Assistant: "What command would you like me to retry?"
```

### ✅ CORRECT:
```
User: "Try again"
Assistant: "Retrying fetch from docs.google.com..."
[executes the exact command that failed]
```

### ❌ WRONG:
```
User: "Retry"
Assistant: "What were you trying to do again?"
```

### ✅ CORRECT:
```
User: "Retry"
Assistant: "Retrying the spreadsheet analysis..."
[continues from where it left off]
```

## Context Preservation

Maintain context across retries:

### Working Memory
Store in current session:
- Last command executed
- Last error encountered
- Current task and progress
- Last 3-5 failed operations (for multiple failures)

### After Retry Success
- Clear the error from memory
- Continue the workflow
- Remember that this step is now complete

## Special Cases

### Case 1: Network Block Then Retry
```
1. Network block detected on docs.google.com
2. Report block using network-handling.md format
3. User whitelists domain
4. User says "try again"
5. Retry the exact WebFetch operation
6. On success, continue with task
```

### Case 2: Multiple Sequential Failures
```
1. First operation fails (error A)
2. User says "try again"
3. Retry, different error (error B)
4. User says "try again"
5. Retry, success
6. Continue
```

### Case 3: Retry Different Operation
```
User: "Try again with the build command"
```
This is **specific instruction**, not a generic retry. Follow the explicit instruction.

### Case 4: Ambiguous Retry
```
User: "Retry"
[Multiple operations have failed in the session]
```
Retry the **most recent** failed operation. If truly ambiguous, briefly confirm:
```
"Retrying the last failed operation: [brief description]. Correct?"
```
Then immediately proceed (don't wait for confirmation unless critical).

## Integration with Network Handling

When network blocks occur:
1. `network-handling.md` handles the initial block detection and reporting
2. THIS guide handles the retry after user whitelists
3. Store the failed WebFetch/network operation for retry
4. When user says "try again", retrieve and re-execute

## Error Memory Management

### Short-Term Memory (Current Session)
- Last failed command: Always available
- Last 3 failures: Available for context
- Current task state: Track progress through multi-step tasks

### Long-Term Memory (Across Sessions)
Claude Code sessions are stateless, so:
- Cannot remember across sessions
- User must provide context if referencing old session
- Each session starts fresh

Within a single session, maintain full memory of failures and context.

## Communicating Retry Status

### Good Retry Communication
```
"Retrying spreadsheet fetch..." [brief, action-oriented]
"Attempting the build again..." [clear intent]
"Re-executing validation test..." [specific]
```

### Avoid Over-Explaining
```
❌ "OK, so you want me to retry the operation that failed earlier, which was
the WebFetch to docs.google.com to retrieve the spreadsheet data for the
UBL build process. Let me try that again now..."

✅ "Retrying spreadsheet fetch..."
```

## Success Metrics

A good retry implementation:
- ✅ User never has to repeat what they want retried
- ✅ Retries execute quickly without lengthy preamble
- ✅ Context is preserved across the retry
- ✅ New errors are clearly distinguished from old errors
- ✅ User feels the system "remembered" the context

## Testing Your Memory

If you're unsure if you remember the last failed operation:
- Review the conversation history
- Look for the last error message you received
- Identify the last tool call that failed
- Check the task context at that point

If truly no operation has failed in the session, clarify:
```
"I don't have a record of a failed operation in this session.
What would you like me to retry?"
```

---

**See also:**
- `network-handling.md` - For network block detection and reporting
- `instructions.md` - Overall workflow
