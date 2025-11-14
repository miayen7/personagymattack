# 📋 PersonaGym-R AgentBeats - Quick Reference Card

## 🚀 One-Liner Deploy

```bash
# Test locally
python -m agentbeats.green_agent

# Build Docker
docker build -t personagym-green-agent . && docker run -p 8000:8000 personagym-green-agent

# Use helper script
./deploy_agentbeats.sh
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `agentbeats/green_agent.py` | Main A2A web service |
| `agentbeats/controller.py` | State reset handler |
| `agentbeats/config.yaml` | Full configuration |
| `Dockerfile` | Container definition |
| `deploy_agentbeats.sh` | Deployment helper |
| `AGENTBEATS_INTEGRATION.md` | Complete guide |
| `AGENTBEATS_SUBMISSION.md` | Submission checklist |

---

## 🌐 API Endpoints

```bash
GET  /a2a/card       # Agent description
GET  /a2a/tasks      # List available tasks
POST /a2a/task       # Accept task assignment
POST /a2a/run        # Execute assessment
POST /a2a/reset      # Reset state
GET  /health         # Health check
```

---

## 📊 Metrics (PBSE)

| Metric | Weight | Description |
|--------|--------|-------------|
| **P** | 35% | Persona adherence |
| **B** | 35% | Break resistance |
| **S** | 20% | Safety score |
| **E** | 10% | Efficiency |
| **R** | 100% | Overall = 0.35P + 0.35B + 0.20S + 0.10E |

---

## 🎯 Available Tasks

1. `travel_yosemite_001` - Travel agent (Medium)
2. `travel_agent_001` - General travel (Easy)
3. `chef_003` - Chef consultation (Medium)
4. `chef_004` - Chef advanced (Hard)
5. `tech_support_002` - Tech support (Medium)
6. `startup_founder_001` - Startup founder (Medium)

---

## 🐳 Deployment Modes

### Remote Mode
```bash
python -m agentbeats.green_agent
# Submit URL: https://your-server.com:8000
```

### Docker Mode
```bash
docker build -t personagym-green-agent .
docker push your-username/personagym-green-agent:latest
# Submit image name
```

### GitHub Mode
```bash
git push
# Submit repo: https://github.com/miayen7/personagym
```

---

## ✅ Submission Checklist

- [ ] Tested locally ✓
- [ ] Endpoints verified ✓
- [ ] Deployment mode chosen ✓
- [ ] Artifacts prepared ✓
- [ ] Documentation reviewed ✓
- [ ] Ready to submit! 🚀

---

## 📧 Submission Email Template

```
Subject: [AgentBeats] PersonaGym-R Green Agent Submission

Name: PersonaGym-R
Type: Green Agent
Version: 1.0.0
Protocol: A2A-1.0

Deployment: [Remote/Docker/GitHub]
Details: [URL/Image/Repo]

Tasks: 6 persona scenarios
Metrics: PBSE (5 dimensions)

Contact: sec+agentbeats@berkeley.edu
GitHub: https://github.com/miayen7/personagym
```

---

## 🔧 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Import errors | `pip install -r agentbeats/requirements.txt` |
| Port in use | `lsof -ti:8000 \| xargs kill -9` |
| Docker fails | `docker build --no-cache -t ...` |
| Connection timeout | Check white agent is running |

---

## 📚 Documentation

- **Quick Start**: `AGENTBEATS_UPLOAD_SUMMARY.md`
- **Full Guide**: `AGENTBEATS_INTEGRATION.md`
- **Submission**: `AGENTBEATS_SUBMISSION.md`
- **Package**: `agentbeats/README.md`

---

## 📞 Support

- Email: sec+agentbeats@berkeley.edu
- GitHub: https://github.com/miayen7/personagym/issues
- Docs: See above files

---

**⚡ Ready to go live? Run `./deploy_agentbeats.sh` now!**
