# Quick Domain Whitelist Check

Copy and paste this into a new Claude Code session:

---

**Prompt:**

```
Check what domains are whitelisted in this environment. Run this command and show me the output:

python3 -c "
import base64, json, os
jwt = os.environ['GLOBAL_AGENT_HTTP_PROXY'].split(':jwt_')[1].split('@')[0]
payload = jwt.split('.')[1] + '=' * (4 - len(jwt.split('.')[1]) % 4)
data = json.loads(base64.urlsafe_b64decode(payload))
print('Current allowed_hosts:')
for host in data.get('allowed_hosts', '').split(','):
    print(f'  - {host}')
print(f\"\\nJWT issued: {data.get('iat')}\\nJWT expires: {data.get('exp')}\")
"
```

---

**Expected domains in updated whitelist:**
- docs.google.com
- *.googleusercontent.com
- *.claude.com
- *.claude.ai
- archive.ubuntu.com
- security.ubuntu.com
- *.realtaonline.com
