# 🚀 GitHub Codespaces Deployment Guide

Deploy PersonaGym-R to AgentBeats using **GitHub Codespaces** - completely free!

---

## Why GitHub Codespaces?

✅ **Free**: 60 hours/month free for all GitHub users  
✅ **Simple**: One-click deployment from your repo  
✅ **HTTPS**: Automatic public HTTPS URL  
✅ **No Config**: Works out of the box  

---

## Step-by-Step Deployment

### 1. Push Your Changes to GitHub

```bash
# Add new files
git add .devcontainer/ start_codespaces.sh railway.json requirements.txt

# Commit
git commit -m "Add Codespaces deployment configuration"

# Push
git push origin main
```

### 2. Create a Codespace

1. Go to your GitHub repo: **https://github.com/miayen7/personagym**
2. Click the green **"Code"** button
3. Click **"Codespaces"** tab
4. Click **"Create codespace on main"**

That's it! GitHub will:
- ✅ Create a cloud development environment
- ✅ Install all dependencies automatically
- ✅ Give you a public HTTPS URL

### 3. Start the Controller

Once your Codespace opens:

```bash
# Run the start script
./start_codespaces.sh
```

Or manually:
```bash
agentbeats run_ctrl
```

### 4. Get Your Public URL

1. In the **PORTS** tab at the bottom of VS Code, you'll see port **8000**
2. Right-click on port 8000 → **"Port Visibility"** → **"Public"**
3. Copy the URL (looks like: `https://username-personagym-abc123-8000.app.github.dev`)

### 5. Test Your Agent

```bash
curl https://YOUR-CODESPACE-URL/.well-known/agent-card.json
```

You should see your agent card!

### 6. Submit to AgentBeats

Email **sec+agentbeats@berkeley.edu** with your Codespace URL:

```
Subject: [Submission] PersonaGym-R Green Agent

Controller URL: https://YOUR-CODESPACE-URL
```

---

## Alternative: GitHub Actions (Auto-Deploy on Push)

If you want automatic deployment, I can also set up GitHub Actions to deploy to a free hosting service on every push. Let me know!

---

## Managing Your Codespace

### Keep It Running
- Codespaces sleep after 30 minutes of inactivity
- To keep it alive: Click in the terminal occasionally
- Or: Set retention in Settings (up to 4 hours)

### Stop/Start
- **Stop**: Click your username → "Stop Codespace"
- **Start**: Go to repo → Code → Codespaces → Click your codespace name

### Cost
- **Free**: 60 hours/month (plenty for testing)
- **Beyond**: ~$0.18/hour for 2-core machine

---

## Troubleshooting

### Port Not Public
1. Open **PORTS** tab (bottom of VS Code)
2. Right-click port 8000
3. Select **"Port Visibility"** → **"Public"**

### Can't Access URL
Make sure:
- Controller is running (`agentbeats run_ctrl`)
- Port 8000 is forwarded
- Port visibility is set to "Public"

### Dependencies Missing
```bash
pip install -e .
pip install -r requirements.txt
```

---

## Quick Commands

```bash
# Start controller
./start_codespaces.sh

# Or manually
agentbeats run_ctrl

# Test locally
curl http://localhost:8000/.well-known/agent-card.json

# Test public URL
curl https://YOUR-CODESPACE-URL/.well-known/agent-card.json

# Stop controller
# Press Ctrl+C
```

---

## What's Next?

1. **Push to GitHub** ✅ (you've already done this)
2. **Create Codespace** → One click on GitHub
3. **Start controller** → `./start_codespaces.sh`
4. **Get public URL** → From PORTS tab
5. **Submit** → Email to AgentBeats

**Total time: ~5 minutes!** 🎉

---

## Other Free Options

If you need something more permanent, I can also help you deploy to:

1. **Render** - Free tier with 750 hours/month
2. **Railway** - $5 credit/month free
3. **Fly.io** - Free tier with 3 shared-CPU VMs
4. **Hugging Face Spaces** - Free for public projects

Let me know which you prefer!
