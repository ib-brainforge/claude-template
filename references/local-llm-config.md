# Local LLM Configuration

Configuration for local LLM workers (Ollama, LM Studio).

## Ollama Setup

### Installation
```bash
# Ubuntu
curl -fsSL https://ollama.com/install.sh | sh

# Start server (if not running as service)
ollama serve
```

### Network Access (for remote machines)
```bash
# Edit systemd service to allow network access
sudo systemctl edit ollama

# Add:
[Service]
Environment="OLLAMA_HOST=0.0.0.0"

# Restart
sudo systemctl restart ollama
```

### Recommended Models for RTX 5090 (32GB VRAM)

| Model | Size | VRAM | Speed | Quality | Use Case |
|-------|------|------|-------|---------|----------|
| codestral:22b-v0.1-q4_K_M | ~13GB | ~14GB | Fast | Good | Commits, docs |
| deepseek-coder:33b-instruct-q4_K_M | ~20GB | ~22GB | Medium | Better | Code review |
| qwen2.5-coder:32b-q4_K_M | ~19GB | ~21GB | Medium | Better | Complex tasks |
| codellama:34b-q4_K_M | ~20GB | ~22GB | Medium | Good | General coding |

### Pull Models
```bash
ollama pull codestral:22b-v0.1-q4_K_M
ollama pull deepseek-coder:33b-instruct-q4_K_M
```

## LM Studio Setup

### Server Mode
1. Open LM Studio
2. Go to "Local Server" tab
3. Load your model
4. Start server (default: http://localhost:1234)

### API Compatibility
LM Studio provides OpenAI-compatible API:
- Endpoint: `http://localhost:1234/v1/chat/completions`
- No API key required (use any string)

### Recommended Models
Same as Ollama, but use GGUF format from HuggingFace.

## Environment Variables

```bash
# Ollama (Ubuntu machine with 5090)
export OLLAMA_HOST="http://192.168.1.XXX:11434"

# LM Studio (if using)
export LMSTUDIO_HOST="http://localhost:1234"

# Which backend to prefer
export LOCAL_LLM_BACKEND="ollama"  # or "lmstudio"
```

## Task-Model Mapping

<!-- TODO: Customize based on your testing -->

```json
{
  "task_models": {
    "commit": {
      "primary": "codestral:22b-v0.1-q4_K_M",
      "fallback": "deepseek-coder:6.7b",
      "quality_threshold": 0.9
    },
    "summary": {
      "primary": "codestral:22b-v0.1-q4_K_M",
      "fallback": "deepseek-coder:6.7b",
      "quality_threshold": 0.85
    },
    "docstring": {
      "primary": "codestral:22b-v0.1-q4_K_M",
      "fallback": "codellama:7b",
      "quality_threshold": 0.9
    },
    "test": {
      "primary": "deepseek-coder:33b-instruct-q4_K_M",
      "fallback": "codestral:22b-v0.1-q4_K_M",
      "quality_threshold": 0.8
    },
    "review": {
      "primary": "deepseek-coder:33b-instruct-q4_K_M",
      "fallback": "qwen2.5-coder:32b-q4_K_M",
      "quality_threshold": 0.85
    }
  }
}
```

## Generation Parameters

```json
{
  "parameters": {
    "commit": {
      "temperature": 0.3,
      "top_p": 0.9,
      "max_tokens": 500,
      "stop": ["\\n\\n\\n"]
    },
    "summary": {
      "temperature": 0.5,
      "top_p": 0.9,
      "max_tokens": 1000
    },
    "docstring": {
      "temperature": 0.3,
      "top_p": 0.9,
      "max_tokens": 500
    },
    "test": {
      "temperature": 0.4,
      "top_p": 0.95,
      "max_tokens": 2000
    },
    "review": {
      "temperature": 0.3,
      "top_p": 0.9,
      "max_tokens": 1500
    }
  }
}
```

## Cost Comparison

| Task | Claude Sonnet | Local (electricity) | Savings |
|------|--------------|---------------------|---------|
| Commit (per repo) | ~$0.01 | ~$0.001 | 90% |
| Batch 40 repos | ~$0.40 | ~$0.04 | 90% |
| Monthly (100 runs) | ~$40 | ~$4 + hardware | ~$36/mo |

Break-even on hardware cost depends on usage volume.

## Fallback Strategy

```
1. Try preferred local model
2. If unavailable → try fallback local model
3. If all local fail → fall back to Claude Haiku (cheapest)
4. For critical tasks → always use Claude Sonnet/Opus
```

## Quality Assurance

Tasks that SHOULD use local:
- Commit message drafts (human reviews anyway)
- Code summaries (informational)
- Docstring generation (human reviews)
- Boilerplate test generation

Tasks that SHOULD use Claude:
- Architecture decisions
- Security reviews
- Complex multi-file analysis
- Final approval decisions
