# LLM Provider Configuration Guide

This guide explains the different LLM (Large Language Model) provider options available in MCP Toolkit and how to configure them.

## Overview

MCP Toolkit supports three LLM providers:

| Provider | Cost | Token Limit | Models Available | Best For |
|----------|------|-------------|------------------|----------|
| **GitHub Models** | FREE | 8K tokens | `gpt-4o-mini` only | Quick testing, budget-conscious |
| **OpenAI** | Paid | 128K+ tokens | All GPT models | Production, full features |
| **Anthropic** | Paid | 200K tokens | All Claude models | Advanced reasoning |

## Important: No VS Code Required

**This application runs standalone in your web browser.** You do NOT need:
- VS Code installed
- VS Code open
- VS Code Copilot extension

Just run `./start.sh` and open http://localhost:7860 in any browser.

---

## Option 1: GitHub Models (FREE)

### What is GitHub Models?

GitHub Models is a free API service that allows GitHub users to access AI models through an API endpoint. It's separate from GitHub Copilot (which is IDE-based code completion).

### Requirements

- GitHub account
- GitHub Personal Access Token
- GitHub Copilot subscription (recommended, but basic access may work)

### Limitations

| Limitation | Impact |
|------------|--------|
| **8,000 token limit** | Total tokens (prompt + response) cannot exceed 8K |
| **Model restriction** | Only `gpt-4o-mini` works reliably within token limits |
| **MCP server limit** | Can only use 1 MCP server at a time (each server adds ~2-4K tokens) |
| **Rate limits** | May experience throttling with heavy usage |

### Why Can't I Use Larger Models?

The MCP agent requires:
- System prompt: ~500 tokens
- Tool definitions per MCP server: ~2,000-4,000 tokens
- User query + response: ~1,000-3,000 tokens

With 3 MCP servers enabled:
```
500 + (3 × 3,000) + 2,000 = ~11,500 tokens > 8,000 limit
```

This exceeds GitHub Models' 8K limit, causing the "tokens_limit_reached" error.

### Configuration

```bash
# .env file
LLM_PROVIDER=github
LLM_MODEL=gpt-4o-mini
GITHUB_TOKEN=ghp_your-token-here
```

### Getting a GitHub Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo`, `read:user`, `read:org`
4. Copy the token (starts with `ghp_`)

### Best Practices for GitHub Models

1. **Use only 1 MCP server at a time** - Edit `mcp_config.json` to enable only what you need
2. **Keep queries short** - Avoid complex multi-step requests
3. **Use for testing** - Good for trying out the toolkit before committing to paid options

---

## Option 2: OpenAI API (PAID - Recommended)

### What is OpenAI API?

Direct access to OpenAI's GPT models with no token limits and full model selection.

### Requirements

- OpenAI account
- OpenAI API key
- Payment method on file

### Benefits

| Benefit | Details |
|---------|---------|
| **No token limits** | 128K+ context window |
| **All models available** | gpt-4, gpt-4o, gpt-4-turbo, gpt-3.5-turbo |
| **All MCP servers** | Use postgres + github + filesystem together |
| **Reliable** | Production-ready, consistent performance |

### Pricing (Approximate)

| Model | Input | Output |
|-------|-------|--------|
| gpt-4o | $2.50/1M tokens | $10/1M tokens |
| gpt-4o-mini | $0.15/1M tokens | $0.60/1M tokens |
| gpt-4-turbo | $10/1M tokens | $30/1M tokens |
| gpt-3.5-turbo | $0.50/1M tokens | $1.50/1M tokens |

Typical query cost: **$0.01 - $0.05 per query**

### Configuration

```bash
# .env file
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
OPENAI_API_KEY=sk-your-openai-key-here
GITHUB_TOKEN=ghp_your-token-here  # Still needed for GitHub MCP server
```

### Getting an OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)
4. Add payment method at https://platform.openai.com/account/billing

---

## Option 3: Anthropic API (PAID)

### What is Anthropic API?

Direct access to Anthropic's Claude models, known for strong reasoning and safety.

### Requirements

- Anthropic account
- Anthropic API key
- Payment method on file

### Benefits

| Benefit | Details |
|---------|---------|
| **200K context window** | Largest context of all providers |
| **Strong reasoning** | Excellent for complex analysis |
| **All Claude models** | Sonnet 4, Opus 4, Haiku, etc. |
| **All MCP servers** | Use all servers together |

### Available Models

| Model | Best For |
|-------|----------|
| `claude-sonnet-4-20250514` | Balanced performance/cost |
| `claude-opus-4-20250514` | Most capable, complex tasks |
| `claude-haiku-4-20250514` | Fast, simple tasks |

### Configuration

```bash
# .env file
LLM_PROVIDER=anthropic
LLM_MODEL=claude-sonnet-4-20250514
ANTHROPIC_API_KEY=sk-ant-your-key-here
GITHUB_TOKEN=ghp_your-token-here  # Still needed for GitHub MCP server
```

### Getting an Anthropic API Key

1. Go to https://console.anthropic.com/settings/keys
2. Click "Create Key"
3. Copy the key (starts with `sk-ant-`)
4. Add payment method in account settings

---

## Quick Comparison

### For Developers WITHOUT API Keys (GitHub Copilot Only)

```bash
# .env
LLM_PROVIDER=github
LLM_MODEL=gpt-4o-mini
GITHUB_TOKEN=ghp_your-token
```

**What works:**
- Single MCP server queries
- Simple questions
- Basic testing

**What doesn't work:**
- Multiple MCP servers simultaneously
- Complex multi-step workflows
- Large context queries

### For Developers WITH OpenAI API Key

```bash
# .env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
OPENAI_API_KEY=sk-your-key
GITHUB_TOKEN=ghp_your-token
```

**What works:**
- Everything!
- All 3 MCP servers together
- Complex queries
- Production workloads

---

## Switching Providers

To switch providers, edit your `.env` file:

### Switch to GitHub Models (Free)
```bash
LLM_PROVIDER=github
LLM_MODEL=gpt-4o-mini
# Comment out: OPENAI_API_KEY and ANTHROPIC_API_KEY
```

### Switch to OpenAI
```bash
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o
OPENAI_API_KEY=sk-your-key
```

### Switch to Anthropic
```bash
LLM_PROVIDER=anthropic
LLM_MODEL=claude-sonnet-4-20250514
ANTHROPIC_API_KEY=sk-ant-your-key
```

After changing, restart the application:
```bash
./stop.sh
./start.sh
```

---

## MCP Server Configuration

When using GitHub Models (free tier), you must limit MCP servers due to token constraints.

### Edit `mcp_config.json`

**For GitHub Models (1 server only):**
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    }
  }
}
```

**For OpenAI/Anthropic (all servers):**
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-postgres", "${DATABASE_URL}"],
      "env": {}
    },
    "github": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "${GITHUB_TOKEN}" }
    },
    "filesystem": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-filesystem", "."],
      "env": {}
    }
  }
}
```

---

## Troubleshooting

### Error: "tokens_limit_reached"

**Cause:** Query exceeds GitHub Models' 8K token limit

**Solutions:**
1. Use only 1 MCP server (edit `mcp_config.json`)
2. Use `gpt-4o-mini` model
3. Switch to OpenAI or Anthropic

### Error: "unknown_model"

**Cause:** Model name not recognized by provider

**Solutions:**
- GitHub Models: Use `gpt-4o-mini`
- OpenAI: Use `gpt-4`, `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo`
- Anthropic: Use `claude-sonnet-4-20250514`, `claude-opus-4-20250514`

### Error: "unauthorized" or "invalid_api_key"

**Cause:** API key is missing or invalid

**Solutions:**
1. Check API key is correctly set in `.env`
2. Ensure no extra spaces or quotes around the key
3. Verify key is active in provider's dashboard

### Application won't start

**Cause:** Missing required environment variables

**Solutions:**
1. Check `.env` file exists
2. Ensure `GITHUB_TOKEN` is set (required for GitHub MCP server)
3. Ensure `DATABASE_URL` is set (required for postgres MCP server)

---

## Summary

| If You Have... | Use This Provider | Configuration |
|----------------|-------------------|---------------|
| Only GitHub Copilot | `github` | Limited to gpt-4o-mini, 1 MCP server |
| OpenAI API Key | `openai` | Full access, all models, all servers |
| Anthropic API Key | `anthropic` | Full access, Claude models, all servers |

**Recommendation:** For production use or full functionality, use OpenAI or Anthropic. GitHub Models is great for testing and budget-conscious development.
