# 🚀 PersonaGym-R AgentBeats Upload - Ready to Submit!

## ✅ What Has Been Created

Your PersonaGym-R project is now fully prepared for AgentBeats submission! Here's what was added:

### 📁 New Directory: `agentbeats/`

Complete integration package with:

1. **`green_agent.py`** (368 lines)
   - A2A-compliant FastAPI web service
   - Implements all required protocol endpoints
   - Orchestrates assessments with white agents
   - Converts PersonaGym-R results to AgentBeats metrics

2. **`controller.py`** (181 lines)
   - State management and reset functionality
   - Ensures assessment isolation
   - Handles white agent reset coordination

3. **`config.yaml`** (223 lines)
   - Complete benchmark configuration
   - 6 task definitions
   - 5 metric definitions with weights
   - Break level specifications
   - Deployment settings

4. **`requirements.txt`**
   - Additional dependencies for A2A protocol
   - FastAPI, uvicorn, httpx

5. **`README.md`**
   - Quick reference for the agentbeats package

6. **`__init__.py`**
   - Package initialization

### 📄 New Documentation Files

1. **`AGENTBEATS_INTEGRATION.md`** (580 lines)
   - Complete integration guide
   - Architecture diagrams
   - API reference
   - Testing instructions
   - Deployment options

2. **`AGENTBEATS_SUBMISSION.md`** (480 lines)
   - Step-by-step submission guide
   - Checklist for all deployment modes
   - Task and metric definitions
   - Resource requirements
   - Post-submission information

3. **`AGENTBEATS_UPLOAD_SUMMARY.md`** (this file)
   - Overview of what was created
   - Next steps

### 🐳 Deployment Files

1. **`Dockerfile`**
   - Container configuration for hosted mode
   - Includes health checks
   - Optimized for AgentBeats platform

2. **`deploy_agentbeats.sh`**
   - Interactive deployment helper script
   - Supports local testing, Docker build, registry push
   - Generates submission packages

---

## 🎯 Three Ways to Deploy

### Option 1: Remote Mode (Your Server)

**Best for**: You have a public server

**Steps**:
1. Deploy on your server: `python -m agentbeats.green_agent`
2. Ensure it's publicly accessible
3. Submit URL: `https://your-server.com:8000`

**Command**:
```bash
./deploy_agentbeats.sh  # Choose option 1
```

### Option 2: Docker Hosted Mode (Recommended)

**Best for**: Easy deployment, let AgentBeats host it

**Steps**:
1. Build: `docker build -t personagym-green-agent .`
2. Push to Docker Hub: `docker push your-username/personagym-green-agent:latest`
3. Submit image name to AgentBeats

**Command**:
```bash
./deploy_agentbeats.sh  # Choose option 3
```

### Option 3: GitHub Repository Mode

**Best for**: Transparent, open-source

**Steps**:
1. Ensure all files are committed
2. Push to GitHub
3. Submit repository URL: `https://github.com/miayen7/personagym`

**Command**:
```bash
git add agentbeats/ Dockerfile AGENTBEATS_*.md deploy_agentbeats.sh
git commit -m "Add AgentBeats integration"
git push
```

---

## 📋 Pre-Submission Checklist

Go through this before submitting:

- [ ] Tested locally: `python -m agentbeats.green_agent`
- [ ] Verified endpoints work:
  - [ ] `curl http://localhost:8000/health`
  - [ ] `curl http://localhost:8000/a2a/card`
  - [ ] `curl http://localhost:8000/a2a/tasks`
- [ ] Chose deployment mode (Remote/Docker/GitHub)
- [ ] Prepared deployment artifacts
- [ ] Reviewed `AGENTBEATS_SUBMISSION.md`
- [ ] Have submission information ready

---

## 🚀 Quick Start Commands

### Test Locally

```bash
# Install dependencies
pip install -r agentbeats/requirements.txt

# Run green agent
python -m agentbeats.green_agent

# In another terminal, test
curl http://localhost:8000/health | python -m json.tool
curl http://localhost:8000/a2a/card | python -m json.tool
curl http://localhost:8000/a2a/tasks | python -m json.tool
```

### Build Docker Image

```bash
# Build
docker build -t personagym-green-agent .

# Test
docker run -p 8000:8000 personagym-green-agent

# Push to Docker Hub
docker tag personagym-green-agent:latest YOUR_USERNAME/personagym-green-agent:latest
docker push YOUR_USERNAME/personagym-green-agent:latest
```

### Use Deployment Script

```bash
# Make executable (if not already)
chmod +x deploy_agentbeats.sh

# Run interactive script
./deploy_agentbeats.sh

# Options:
# 1 - Local testing
# 2 - Docker build and test
# 3 - Deploy to Docker registry
# 4 - Generate submission package
```

---

## 📝 Submission Information Template

When you submit to AgentBeats, use this information:

```
=== AGENTBEATS SUBMISSION ===

Name: PersonaGym-R
Type: Green Agent (Hosting/Evaluator)
Version: 1.0.0
Protocol: A2A-1.0

Description:
Adversarial persona adherence benchmark that tests AI agents' 
ability to maintain assigned personas under social engineering attacks.

Deployment Mode: [Choose one]
□ Remote: https://your-server.com:8000
□ Docker: your-username/personagym-green-agent:latest
□ GitHub: https://github.com/miayen7/personagym

Available Tasks: 6
- travel_yosemite_001 (Medium)
- travel_agent_001 (Easy)
- chef_003 (Medium)
- chef_004 (Hard)
- tech_support_002 (Medium)
- startup_founder_001 (Medium)

Metrics: 5
- Persona Adherence (P) - 35%
- Break Resistance (B) - 35%
- Safety (S) - 20%
- Efficiency (E) - 10%
- Overall Score (R) - Primary

Resource Requirements:
- CPU: 2 cores
- Memory: 512 MB
- GPU: Not required
- Storage: 500 MB

Contact:
- Email: sec+agentbeats@berkeley.edu
- GitHub: https://github.com/miayen7/personagym

Documentation:
- Integration Guide: AGENTBEATS_INTEGRATION.md
- Submission Guide: AGENTBEATS_SUBMISSION.md
- Main README: README.md
```

---

## 📚 Documentation Hierarchy

Read these in order if needed:

1. **Start Here**: `AGENTBEATS_UPLOAD_SUMMARY.md` (this file)
   - Overview of what was created
   - Quick start commands

2. **Next**: `agentbeats/README.md`
   - Package-specific documentation
   - Quick reference

3. **Deep Dive**: `AGENTBEATS_INTEGRATION.md`
   - Complete architecture
   - API reference
   - Testing guide
   - White agent requirements

4. **Before Submission**: `AGENTBEATS_SUBMISSION.md`
   - Detailed submission checklist
   - Task and metric definitions
   - Deployment mode comparison
   - Post-submission info

5. **Reference**: `SYSTEM_EXPLANATION.md` (existing)
   - PersonaGym-R system details
   - Background and motivation

---

## 🔍 File Structure Overview

```
personagym_r/
├── agentbeats/                    [NEW]
│   ├── __init__.py               # Package initialization
│   ├── green_agent.py            # A2A web service (MAIN)
│   ├── controller.py             # State management
│   ├── config.yaml               # Configuration
│   ├── requirements.txt          # Dependencies
│   └── README.md                 # Package docs
│
├── src/personagym_r/             [EXISTING]
│   ├── orchestrator.py           # Core evaluation logic
│   ├── api_schema.py             # Data models
│   ├── attacker/                 # Attack tactics
│   ├── baselines/                # Reference agents
│   └── graders/                  # Scoring components
│
├── tasks/                        [EXISTING]
│   ├── travel_yosemite_001/      # Assessment task
│   ├── chef_003/
│   ├── chef_004/
│   └── ...
│
├── Dockerfile                    [NEW]
├── deploy_agentbeats.sh         [NEW]
├── AGENTBEATS_INTEGRATION.md    [NEW]
├── AGENTBEATS_SUBMISSION.md     [NEW]
├── AGENTBEATS_UPLOAD_SUMMARY.md [NEW - this file]
├── README.md                     [EXISTING]
└── pyproject.toml               [EXISTING]
```

---

## ⚙️ Technical Details

### What the Green Agent Does

1. **Receives task request** from AgentBeats
2. **Loads configuration** from tasks directory
3. **Resets white agents** via A2A protocol
4. **Initializes sessions** with persona assignments
5. **Orchestrates dialog** between attacker and white agent
6. **Monitors for breaks** and safety violations
7. **Computes metrics** (PBSE scoring)
8. **Returns results** to AgentBeats

### Protocol Compliance

✅ A2A-1.0 protocol  
✅ Required endpoints implemented  
✅ Proper error handling  
✅ Health checks  
✅ State reset support  
✅ Session management  

### Key Features

- **6 Assessment Tasks**: Pre-configured persona scenarios
- **8+ Attack Tactics**: Adversarial testing strategies
- **5 Metrics**: Comprehensive PBSE scoring
- **3 Break Levels**: L1 (soft), L2 (meta), L3 (explicit)
- **Safety Checks**: PII, medical/legal advice, harassment
- **Reproducible**: Seed-based deterministic evaluation

---

## 🐛 Troubleshooting

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
pip install -r agentbeats/requirements.txt
```

### Port Already in Use

**Problem**: `Address already in use: 8000`

**Solution**:
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Or use different port
# Edit green_agent.py: uvicorn.run(app, port=8001)
```

### Docker Build Fails

**Problem**: Build errors

**Solution**:
```bash
# Ensure Docker is running
docker info

# Clear cache and rebuild
docker build --no-cache -t personagym-green-agent .
```

### Connection Timeout

**Problem**: Can't reach white agent

**Solution**:
- Verify white agent is running
- Check firewall rules
- Ensure A2A endpoints are implemented
- Test with: `curl http://white-agent-url/a2a/card`

---

## 📧 Getting Help

**Questions?**
- Read: `AGENTBEATS_INTEGRATION.md`
- Read: `AGENTBEATS_SUBMISSION.md`
- Email: sec+agentbeats@berkeley.edu
- GitHub: https://github.com/miayen7/personagym/issues

**Ready to Submit?**
- Use deployment script: `./deploy_agentbeats.sh`
- Follow checklist in `AGENTBEATS_SUBMISSION.md`
- Contact AgentBeats team with deployment info

---

## 🎉 Next Steps

1. **✅ Test locally**:
   ```bash
   python -m agentbeats.green_agent
   curl http://localhost:8000/health
   ```

2. **✅ Choose deployment mode**:
   - Remote, Docker, or GitHub?
   - See `AGENTBEATS_SUBMISSION.md` for comparison

3. **✅ Deploy**:
   ```bash
   ./deploy_agentbeats.sh
   ```

4. **✅ Submit to AgentBeats**:
   - Use template above
   - Include deployment details
   - Reference documentation

5. **🚀 Go live**:
   - Monitor leaderboards
   - Track submissions
   - Iterate and improve

---

## 🏆 You're Ready!

Your PersonaGym-R benchmark is now:
- ✅ A2A protocol compliant
- ✅ Fully documented
- ✅ Docker-ready
- ✅ Production-ready
- ✅ AgentBeats-ready

**Time to upload and share your benchmark with the world!** 🌍

Good luck! 🚀
