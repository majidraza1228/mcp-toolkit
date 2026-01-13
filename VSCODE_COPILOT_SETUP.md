# VS Code Copilot / GitHub Models Setup Guide

This guide shows you how to use **VS Code Copilot** or **GitHub Models** as the LLM provider for your AI Agent.

## What is GitHub Models?

GitHub Models provides access to various AI models (GPT-4, GPT-3.5, Claude, Llama, etc.) through:
- **GitHub Copilot subscription** (if you have VS Code Copilot)
- **GitHub Models API** (free tier available)
- **Azure OpenAI Service** (enterprise)

## Benefits

- ✅ **Free or Low Cost**: Use your existing Copilot subscription or free GitHub Models tier
- ✅ **Multiple Models**: Access GPT-4o, GPT-4, Claude, Llama, and more
- ✅ **Same Interface**: Works seamlessly with your agent
- ✅ **No OpenAI Account**: Use GitHub token instead of OpenAI API key

---

## Setup Options

### Option 1: Use Your GitHub Token (Easiest)

If you have GitHub Copilot or want to use GitHub Models:

1. **Get Your GitHub Token:**
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select scopes: `repo`, `read:user`, `read:org`
   - Copy the token (starts with `ghp_...`)

2. **Configure `.env`:**
   ```bash
   # Set provider to github
   LLM_PROVIDER=github

   # Use your GitHub token for both MCP server AND LLM
   GITHUB_TOKEN=ghp_your_token_here
   GITHUB_MODELS_API_KEY=${GITHUB_TOKEN}

   # Choose your model
   LLM_MODEL=gpt-4o
   ```

3. **Run the agent:**
   ```bash
   python run.py
   ```

### Option 2: Get a Dedicated GitHub Models Token

For production use, get a dedicated token:

1. **Sign up for GitHub Models:**
   - Visit https://github.com/marketplace/models
   - Or use Azure OpenAI: https://azure.microsoft.com/products/ai-services/openai-service

2. **Get your API key** and configure `.env`:
   ```bash
   LLM_PROVIDER=github
   GITHUB_MODELS_API_KEY=your_models_token_here
   GITHUB_TOKEN=ghp_your_github_token_here  # For GitHub MCP server
   LLM_MODEL=gpt-4o
   ```

### Option 3: Use OpenAI Directly (Traditional)

If you prefer standard OpenAI:

```bash
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-your_openai_key_here
GITHUB_TOKEN=ghp_your_token_here  # Still needed for GitHub MCP server
LLM_MODEL=gpt-4
```

---

## Available Models

When using `LLM_PROVIDER=github`, you can use these models:

### GPT Models (OpenAI)
- `gpt-4o` - Latest GPT-4 Omni (recommended)
- `gpt-4` - GPT-4 standard
- `gpt-4-turbo` - GPT-4 Turbo
- `gpt-3.5-turbo` - Faster, cheaper

### Claude Models (Anthropic)
- `claude-3-5-sonnet` - Latest Claude
- `claude-3-opus` - Most capable
- `claude-3-sonnet` - Balanced

### Other Models
- `llama-3.1-405b` - Meta Llama 3.1
- `mistral-large` - Mistral AI
- `phi-3` - Microsoft Phi-3

Check GitHub Models marketplace for the full list: https://github.com/marketplace/models

---

## Configuration Examples

### Example 1: VS Code Copilot User (Free/Included)

```bash
# .env
LLM_PROVIDER=github
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
GITHUB_MODELS_API_KEY=${GITHUB_TOKEN}
LLM_MODEL=gpt-4o
DATABASE_URL=postgresql://localhost/mydb
```

### Example 2: Mix GitHub Models + OpenAI

```bash
# .env
LLM_PROVIDER=github  # or openai
GITHUB_MODELS_API_KEY=ghp_xxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxx  # Fallback
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
LLM_MODEL=gpt-4o
DATABASE_URL=postgresql://localhost/mydb
```

### Example 3: Production with Anthropic Claude

```bash
# .env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
LLM_MODEL=claude-3-5-sonnet-20241022
DATABASE_URL=postgresql://user:pass@prod-db.com/mydb
```

---

## Verifying Your Setup

### Test 1: Check Environment Variables

```bash
# In your terminal
cd mcp-toolkit
cat .env | grep -E "LLM_PROVIDER|GITHUB|OPENAI"
```

Should show your configured provider and tokens.

### Test 2: Test the Agent

```python
# test_agent.py
import asyncio
from agent_service import AgentService

async def test():
    service = AgentService()
    await service.initialize()

    result = await service.run("What is 2 + 2?")
    print(result)

    await service.cleanup()

asyncio.run(test())
```

Run:
```bash
python test_agent.py
```

### Test 3: Check Which Model is Being Used

The agent will print during initialization:
```
✓ Agent service initialized
Using LLM Provider: github
Model: gpt-4o
```

---

## Switching Between Providers

You can easily switch providers by changing `LLM_PROVIDER` in `.env`:

```bash
# Use GitHub Models (VS Code Copilot)
LLM_PROVIDER=github

# Use Standard OpenAI
LLM_PROVIDER=openai

# Use Anthropic Claude
LLM_PROVIDER=anthropic
```

No code changes needed! Just restart the application.

---

## Cost Comparison

| Provider | Free Tier | Paid Pricing | Best For |
|----------|-----------|--------------|----------|
| **GitHub Models** | Limited free usage | Varies by model | Copilot users, testing |
| **OpenAI** | $5 credit (new users) | $0.03/1K tokens (GPT-4) | Production, reliability |
| **Anthropic** | No free tier | $0.015/1K tokens (Claude 3.5) | Advanced reasoning |
| **Groq** | Free tier available | Very competitive | Speed, testing |

---

## Troubleshooting

### Error: "GitHub Models requires GITHUB_MODELS_API_KEY"

**Solution:** Set the token in `.env`:
```bash
GITHUB_MODELS_API_KEY=ghp_your_token_here
```

Or use your existing GitHub token:
```bash
GITHUB_MODELS_API_KEY=${GITHUB_TOKEN}
```

### Error: "No LLM provider configured"

**Solution:** Ensure `.env` has `LLM_PROVIDER` set:
```bash
LLM_PROVIDER=github  # or openai, or anthropic
```

### Error: "Rate limit exceeded"

**Solutions:**
1. **GitHub Models**: You may have hit the free tier limit
   - Wait or upgrade to paid tier
   - Switch to `LLM_PROVIDER=openai` temporarily

2. **OpenAI**: You've exceeded your quota
   - Add credits to your OpenAI account
   - Reduce `LLM_TEMPERATURE` to use fewer tokens

### Agent responses are slow

**Solutions:**
1. Use faster models:
   ```bash
   LLM_MODEL=gpt-3.5-turbo  # Much faster than GPT-4
   ```

2. Use Groq for ultra-fast inference:
   ```bash
   LLM_PROVIDER=groq
   GROQ_API_KEY=gsk_your_key_here
   LLM_MODEL=llama-3.1-70b-versatile
   ```

### VS Code Copilot not working

GitHub Models API is separate from VS Code Copilot. You need:
- A GitHub account
- A GitHub Personal Access Token
- Access to GitHub Models (sign up at https://github.com/marketplace/models)

---

## Advanced: Using Multiple Models

You can programmatically switch models:

```python
from agent_service import AgentService

# Use GPT-4o for complex tasks
complex_agent = AgentService(model="gpt-4o")

# Use GPT-3.5 for simple queries (faster, cheaper)
simple_agent = AgentService(model="gpt-3.5-turbo")

# Use Claude for reasoning tasks
reasoning_agent = AgentService(model="claude-3-5-sonnet")
```

---

## Best Practices

### 1. Development vs Production

**Development:**
```bash
LLM_PROVIDER=github
LLM_MODEL=gpt-3.5-turbo  # Fast and cheap for testing
```

**Production:**
```bash
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o  # More reliable, better results
```

### 2. Cost Optimization

- Use `gpt-3.5-turbo` for simple queries
- Use `gpt-4o` only for complex reasoning
- Set `LLM_TEMPERATURE=0` for consistent, cheaper responses
- Cache frequently asked questions

### 3. Security

- Never commit `.env` to git (already in `.gitignore`)
- Rotate tokens regularly
- Use separate tokens for dev/staging/prod
- Monitor API usage for anomalies

---

## Resources

- **GitHub Models Marketplace**: https://github.com/marketplace/models
- **GitHub Models Docs**: https://docs.github.com/en/rest/models
- **OpenAI API Docs**: https://platform.openai.com/docs
- **Anthropic API Docs**: https://docs.anthropic.com
- **LangChain Docs**: https://python.langchain.com

---

## Need Help?

1. Check this guide
2. Read [QUICKSTART.md](QUICKSTART.md)
3. Review [README.md](README.md)
4. Open an issue: https://github.com/majidraza1228/mcp-toolkit/issues

---

**You're all set!** 🚀

Your AI agent can now use:
- ✅ GitHub Models (VS Code Copilot)
- ✅ Standard OpenAI
- ✅ Anthropic Claude
- ✅ Any other LangChain-compatible LLM

Just configure `.env` and run!
