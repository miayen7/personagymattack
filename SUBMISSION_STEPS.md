# 📋 AgentBeats Submission Guide - Step by Step

This guide will walk you through submitting PersonaGym-R to AgentBeats.

---

## Overview: 3 Main Steps

1. **Deploy** your agent with the controller
2. **Test** that it's accessible
3. **Submit** the controller URL to AgentBeats

---

## Step 1: Deploy Your Agent

### Option A: Google Cloud Run (Easiest - Recommended)

**Prerequisites:**
- Google Cloud account ([Sign up free](https://cloud.google.com/free))
- gcloud CLI installed ([Install guide](https://cloud.google.com/sdk/docs/install))

**Deploy in one command:**

```bash
./deploy_to_cloud_run.sh
```

This script will:
1. Generate requirements.txt
2. Build container image
3. Deploy to Cloud Run
4. Give you the controller URL

**Manual deployment:**

```bash
# 1. Set your project
gcloud config set project YOUR_PROJECT_ID

# 2. Generate requirements.txt (buildpacks need it)
pip freeze > requirements.txt

# 3. Build image
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/personagym-green

# 4. Deploy
gcloud run deploy personagym-green \
    --image gcr.io/YOUR_PROJECT_ID/personagym-green \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 1Gi

# 5. Get URL
gcloud run services describe personagym-green \
    --platform managed \
    --region us-central1 \
    --format 'value(status.url)'
```

**Cost:** Free tier includes 2 million requests/month!

---

### Option B: Local with ngrok (For Testing)

**Prerequisites:**
- ngrok account ([Sign up free](https://ngrok.com))

**Steps:**

```bash
# 1. Install dependencies
pip install earthshaker a2a-python

# 2. Start controller in one terminal
agentbeats run_ctrl

# 3. In another terminal, expose with ngrok
ngrok http 8000

# 4. Use the ngrok HTTPS URL
# Example: https://abc123.ngrok.io
```

**Note:** Free ngrok URLs change on restart. Good for testing only!

---

### Option C: Your Own Server/VM

**Prerequisites:**
- Linux server with public IP
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt)

**Steps:**

```bash
# 1. SSH to your server
ssh user@your-server.com

# 2. Clone repo
git clone https://github.com/miayen7/personagym.git
cd personagym

# 3. Install dependencies
pip install earthshaker a2a-python
pip install -e .
pip install -r agentbeats/requirements.txt

# 4. Start controller (use screen/tmux for persistence)
screen -S agentbeats
agentbeats run_ctrl
# Detach: Ctrl+A, D

# 5. Setup SSL with Nginx (recommended)
# See: https://letsencrypt.org/getting-started/
```

---

## Step 2: Test Your Deployment

Once deployed, verify your agent is accessible:

### Test 1: Agent Card

```bash
curl https://your-controller-url/.well-known/agent-card.json
```

**Expected response:**
```json
{
  "name": "PersonaGym-R Green Agent",
  "version": "1.0.0",
  "description": "Adversarial persona adherence benchmark for AI agents",
  ...
}
```

### Test 2: Health Check

```bash
curl https://your-controller-url/health
```

### Test 3: Controller Management UI

Visit in browser:
```
https://your-controller-url
```

You should see the earthshaker management interface.

---

## Step 3: Submit to AgentBeats

### Where to Submit

Based on the AgentBeats documentation, you submit through their platform. The exact URL isn't public yet, so:

**Contact AgentBeats:**
- Email: **sec+agentbeats@berkeley.edu**
- Subject: `[Submission] PersonaGym-R Green Agent`

### Submission Information

Include this information in your email:

```
Subject: [Submission] PersonaGym-R Green Agent

Hi AgentBeats Team,

I would like to submit PersonaGym-R as a green agent to the AgentBeats platform.

=== Agent Information ===
Name: PersonaGym-R
Type: Green Agent (Assessment Orchestrator)
Version: 1.0.0
Description: Adversarial persona adherence benchmark for testing AI agents

=== Deployment Details ===
Controller URL: [YOUR_HTTPS_URL_HERE]
Deployment Method: [Google Cloud Run / Own Server / Other]

=== Capabilities ===
- 6 Assessment Tasks (personas: travel agent, chef, tech support, startup founder)
- PBSE Metrics: Persona, Break Resistance, Safety, Efficiency
- A2A Protocol compliant
- Adversarial testing with 8+ attack tactics
- Break detection (3 levels: L1, L2, L3)
- Safety checks (PII, harmful content)

=== Technical Details ===
Protocol: A2A-1.0
Controller: earthshaker
Repository: https://github.com/miayen7/personagym
Documentation: See AGENTBEATS_OFFICIAL_GUIDE.md in repo

=== Test Results ===
✅ Agent card accessible at: [URL]/.well-known/agent-card.json
✅ Controller management UI working
✅ A2A message handling verified

=== White Agent Requirements ===
- Must implement A2A protocol
- Accept persona assignment
- Maintain character throughout conversation
- See AGENTBEATS_OFFICIAL_GUIDE.md for details

=== Contact ===
Name: [Your Name]
Email: [Your Email]
GitHub: [Your GitHub username]
Affiliation: [University/Company if applicable]

Please let me know if you need any additional information or testing.

Thank you!
```

---

## Alternative: Submit via Platform Form

If AgentBeats has a web submission form (check their platform when you get access), fill it out with:

### Basic Info
- **Agent Name:** PersonaGym-R
- **Agent Type:** Green Agent
- **Version:** 1.0.0

### Description
```
Adversarial persona adherence benchmark that tests AI agents' ability 
to maintain assigned personas under social engineering attacks.

Features:
• 6 pre-configured persona scenarios
• PBSE metrics (Persona, Break, Safety, Efficiency)
• 8+ adversarial attack tactics
• Break detection (L1/L2/L3 severity levels)
• Comprehensive safety checks
```

### Technical
- **Controller URL:** [Your HTTPS URL]
- **Protocol:** A2A-1.0
- **Repository:** https://github.com/miayen7/personagym
- **Documentation:** AGENTBEATS_OFFICIAL_GUIDE.md

### Tags
```
persona-testing, adversarial-evaluation, safety, social-engineering, 
security-testing, chatbot-evaluation, role-playing
```

### Requirements for White Agents
```
- A2A protocol support
- Context ID handling
- Message-based interaction
- No special tools required
```

---

## What Happens After Submission?

### 1. Verification (1-2 days)
AgentBeats will:
- Access your controller URL
- Check agent card
- Test basic A2A communication
- Verify management interface

### 2. Testing (2-3 days)
They may:
- Run test assessments
- Verify metrics are computed correctly
- Check reproducibility
- Test with sample white agents

### 3. Approval
Once verified:
- ✅ Your agent goes live on the platform
- ✅ Appears in the AgentBeats catalog
- ✅ Other users can run assessments
- ✅ Results populate leaderboards

### 4. Monitoring
After going live:
- View usage statistics
- See which agents are being tested
- Monitor assessment results
- Track leaderboard positions
- Receive notifications

---

## Troubleshooting

### "Agent card not accessible"

**Problem:** Can't access `/.well-known/agent-card.json`

**Solutions:**
1. Check if controller is running: `curl https://your-url/health`
2. Verify run.sh is executable: `chmod +x run.sh`
3. Check logs in controller management UI
4. Ensure port 8080 is exposed (Cloud Run) or 8000 (local)

### "Connection refused"

**Problem:** Can't connect to controller URL

**Solutions:**
1. Verify URL is correct and uses HTTPS
2. Check firewall rules allow incoming connections
3. For Cloud Run: ensure service is deployed and running
4. For VM: check if controller process is running

### "A2A message handling fails"

**Problem:** Agent doesn't respond to messages

**Solutions:**
1. Check green_agent_a2a.py is running
2. Verify a2a-python is installed: `pip list | grep a2a`
3. Check logs for Python errors
4. Test with simple message first

---

## Quick Reference: Deployment Commands

### Cloud Run (Fastest)
```bash
./deploy_to_cloud_run.sh
```

### Local Testing
```bash
pip install earthshaker a2a-python
agentbeats run_ctrl
```

### Test Deployment
```bash
# Get your URL from deployment output, then:
curl https://YOUR_URL/.well-known/agent-card.json
```

### Submit
```bash
# Email to: sec+agentbeats@berkeley.edu
# Subject: [Submission] PersonaGym-R Green Agent
# Include: Controller URL and agent details
```

---

## Cost Estimates

### Google Cloud Run (Recommended)
- **Free Tier:** 2M requests/month, plenty for testing
- **Beyond Free:** ~$0.40 per million requests
- **Storage:** Minimal (~$0.01/month)
- **Total:** Likely **$0-5/month** for moderate use

### Own Server/VM
- **Small VM:** $5-10/month (DigitalOcean, Linode)
- **Bandwidth:** Usually included
- **SSL:** Free (Let's Encrypt)
- **Total:** ~**$5-10/month**

### ngrok (Testing Only)
- **Free Tier:** Limited, URL changes
- **Paid:** $8/month for fixed URL
- **Not recommended for production**

---

## Support

**Need Help?**
- 📧 Email: sec+agentbeats@berkeley.edu
- 📖 Docs: AGENTBEATS_OFFICIAL_GUIDE.md
- 🐙 GitHub: https://github.com/miayen7/personagym/issues

**Before Submitting:**
- ✅ Test agent card is accessible
- ✅ Verify controller management UI works
- ✅ Ensure HTTPS is enabled
- ✅ Have controller URL ready

---

## Checklist: Ready to Submit?

- [ ] ✅ Agent deployed and publicly accessible
- [ ] ✅ Controller URL is HTTPS (required)
- [ ] ✅ Agent card accessible: `/.well-known/agent-card.json`
- [ ] ✅ Tested with curl commands above
- [ ] ✅ Controller management UI works
- [ ] ✅ Prepared submission email/form
- [ ] ✅ Have GitHub repo URL
- [ ] ✅ Documentation is up to date
- [ ] 🚀 **Ready to submit!**

---

## Example: Complete Submission Flow

```bash
# 1. Deploy (choose one option)
./deploy_to_cloud_run.sh
# Note the URL: https://personagym-green-xyz.run.app

# 2. Test
curl https://personagym-green-xyz.run.app/.well-known/agent-card.json
# ✅ Returns agent card

# 3. Email submission
# To: sec+agentbeats@berkeley.edu
# Subject: [Submission] PersonaGym-R Green Agent
# Body: Use template above with your URL

# 4. Wait for verification (1-2 days)
# You'll receive confirmation email

# 5. Go live! 🎉
# Your agent appears on AgentBeats platform
```

---

**Ready to submit? Let's go! 🚀**

If you need any help during deployment or submission, just ask!
