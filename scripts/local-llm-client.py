#!/usr/bin/env python3
"""
Local LLM client for Ollama integration.

Handles:
- Health checks and model availability
- Task-specific prompt construction
- Generation with retry/fallback logic
- Batch processing for efficiency
- Output validation

TODO: Configure OLLAMA_HOST and preferred models.

Usage:
    python local-llm-client.py ping --host http://192.168.1.x:11434
    python local-llm-client.py health --host http://192.168.1.x:11434
    python local-llm-client.py generate --task commit --input '{"diff": "..."}'
    python local-llm-client.py batch --task commit --input-file batch.json
"""

import os
import sys
import json
import argparse
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from concurrent.futures import ThreadPoolExecutor, as_completed


# -----------------------------------------------------------------------------
# Configuration
# TODO: Set your Ollama host and preferred models
# -----------------------------------------------------------------------------

DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

# Model recommendations per task type
# TODO: Adjust based on your hardware and quality needs
TASK_MODELS = {
    "commit": "codestral:22b-v0.1-q4_K_M",      # Good balance for commit msgs
    "summary": "codestral:22b-v0.1-q4_K_M",     # Code understanding
    "docstring": "codestral:22b-v0.1-q4_K_M",   # Documentation
    "test": "codestral:22b-v0.1-q4_K_M",        # Test generation
    "review": "deepseek-coder:33b-instruct-q4_K_M",  # Deeper analysis
    "custom": "codestral:22b-v0.1-q4_K_M",      # Default for custom
}

# Fallback chain if primary model unavailable
MODEL_FALLBACKS = {
    "codestral:22b-v0.1-q4_K_M": ["codestral:latest", "deepseek-coder:6.7b"],
    "deepseek-coder:33b-instruct-q4_K_M": ["deepseek-coder:latest", "codestral:latest"],
}

# Generation parameters per task
TASK_PARAMS = {
    "commit": {"temperature": 0.3, "top_p": 0.9, "max_tokens": 500},
    "summary": {"temperature": 0.5, "top_p": 0.9, "max_tokens": 1000},
    "docstring": {"temperature": 0.3, "top_p": 0.9, "max_tokens": 500},
    "test": {"temperature": 0.4, "top_p": 0.95, "max_tokens": 2000},
    "review": {"temperature": 0.3, "top_p": 0.9, "max_tokens": 1500},
    "custom": {"temperature": 0.5, "top_p": 0.9, "max_tokens": 1000},
}


# -----------------------------------------------------------------------------
# Prompt Templates
# TODO: Customize prompts for your conventions
# -----------------------------------------------------------------------------

PROMPTS = {
    "commit": """Generate a conventional commit message for the following changes.

Rules:
- Use format: <type>(<scope>): <subject>
- Types: feat, fix, refactor, perf, test, docs, style, chore, ci, build
- Subject: imperative mood, lowercase, no period, max 50 chars
- Add body only if needed to explain WHY

Repository: {repo}
Files changed: {files_changed}
Categories: {categories}

Diff summary:
{diff_summary}

Respond with ONLY the commit message, nothing else.""",

    "summary": """Summarize the following code/changes concisely.

Focus on:
- What the code does (purpose)
- Key components/functions
- Important patterns used

Code:
{code}

Provide a brief summary (2-4 sentences).""",

    "docstring": """Generate a docstring for the following function/class.

Use this format:
- Brief description (one line)
- Args: parameter descriptions
- Returns: return value description
- Raises: exceptions if applicable

Code:
{code}

Respond with ONLY the docstring content.""",

    "test": """Generate unit tests for the following code.

Requirements:
- Use the testing framework: {framework}
- Cover main functionality
- Include edge cases
- Use descriptive test names

Code:
{code}

Generate complete, runnable test code.""",

    "review": """Review the following code changes for issues.

Check for:
- Bugs or logic errors
- Security concerns
- Performance issues
- Code style problems
- Missing error handling

Changes:
{diff}

List any issues found with line references. If no issues, say "No issues found".""",
}


# -----------------------------------------------------------------------------
# Ollama API Client
# -----------------------------------------------------------------------------

def ping(host: str, timeout: int = 5) -> Dict[str, Any]:
    """
    Quick ping to check if Ollama is running.
    Returns simple available/unavailable status for fast checks.
    """
    try:
        ollama_request(host, "/api/tags", timeout=timeout)
        return {
            "available": True,
            "host": host,
            "status": "running"
        }
    except Exception as e:
        return {
            "available": False,
            "host": host,
            "status": "unavailable",
            "error": str(e)
        }


def ollama_request(
    host: str,
    endpoint: str,
    data: Optional[Dict] = None,
    method: str = "GET",
    timeout: int = 120
) -> Dict[str, Any]:
    """Make request to Ollama API."""
    url = f"{host.rstrip('/')}{endpoint}"
    headers = {"Content-Type": "application/json"}

    body = json.dumps(data).encode() if data else None
    req = Request(url, data=body, headers=headers, method=method)

    try:
        with urlopen(req, timeout=timeout) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        raise Exception(f"Ollama API error {e.code}: {error_body}")
    except URLError as e:
        raise Exception(f"Cannot connect to Ollama: {e.reason}")


def check_health(host: str) -> Dict[str, Any]:
    """Check Ollama server health and available models."""
    try:
        # Check server is running
        ollama_request(host, "/api/tags", timeout=5)

        # Get available models
        models_response = ollama_request(host, "/api/tags", timeout=10)
        models = [m["name"] for m in models_response.get("models", [])]

        return {
            "healthy": True,
            "available": True,
            "host": host,
            "models_available": models,
            "model_count": len(models),
            "status": "ready" if models else "no_models"
        }
    except Exception as e:
        return {
            "healthy": False,
            "available": False,
            "host": host,
            "error": str(e),
            "status": "unavailable"
            "models_available": [],
        }


def ensure_model(host: str, model: str) -> Dict[str, Any]:
    """Ensure model is available, pull if needed."""
    health = check_health(host)

    if not health["healthy"]:
        return {"success": False, "error": health["error"]}

    # Check if model is available
    model_base = model.split(":")[0]
    available = any(
        m.startswith(model_base)
        for m in health["models_available"]
    )

    if available:
        return {"success": True, "model": model, "pulled": False}

    # Try to pull the model
    try:
        print(f"Pulling model {model}...", file=sys.stderr)
        # Note: This is a streaming endpoint, simplified here
        ollama_request(
            host,
            "/api/pull",
            data={"name": model},
            method="POST",
            timeout=600  # Models can take a while to download
        )
        return {"success": True, "model": model, "pulled": True}
    except Exception as e:
        return {"success": False, "error": f"Failed to pull model: {e}"}


def generate(
    host: str,
    model: str,
    prompt: str,
    temperature: float = 0.5,
    top_p: float = 0.9,
    max_tokens: int = 1000,
    timeout: int = 120
) -> Dict[str, Any]:
    """Generate text using Ollama."""
    start_time = time.time()

    try:
        response = ollama_request(
            host,
            "/api/generate",
            data={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "top_p": top_p,
                    "num_predict": max_tokens,
                }
            },
            method="POST",
            timeout=timeout
        )

        duration = time.time() - start_time

        return {
            "success": True,
            "content": response.get("response", ""),
            "model": model,
            "duration_ms": int(duration * 1000),
            "eval_count": response.get("eval_count", 0),
            "prompt_eval_count": response.get("prompt_eval_count", 0),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "model": model,
            "duration_ms": int((time.time() - start_time) * 1000),
        }


# -----------------------------------------------------------------------------
# Task Processing
# -----------------------------------------------------------------------------

def build_prompt(task_type: str, input_data: Dict[str, Any]) -> str:
    """Build prompt from template and input data."""
    template = PROMPTS.get(task_type, PROMPTS["custom"])

    # Handle custom prompts
    if task_type == "custom" and "prompt" in input_data:
        return input_data["prompt"]

    try:
        return template.format(**input_data)
    except KeyError as e:
        raise ValueError(f"Missing required input field: {e}")


def process_task(
    host: str,
    model: str,
    task_type: str,
    input_data: Dict[str, Any],
    timeout: int = 120
) -> Dict[str, Any]:
    """Process a single task."""
    # Get task parameters
    params = TASK_PARAMS.get(task_type, TASK_PARAMS["custom"])

    # Build prompt
    try:
        prompt = build_prompt(task_type, input_data)
    except ValueError as e:
        return {"success": False, "error": str(e)}

    # Generate
    result = generate(
        host=host,
        model=model,
        prompt=prompt,
        temperature=params["temperature"],
        top_p=params["top_p"],
        max_tokens=params["max_tokens"],
        timeout=timeout
    )

    return result


def process_batch(
    host: str,
    model: str,
    task_type: str,
    inputs: List[Dict[str, Any]],
    concurrency: int = 2,
    timeout: int = 120
) -> Dict[str, Any]:
    """Process multiple tasks with controlled concurrency."""
    results = []
    start_time = time.time()

    # Note: Ollama handles one request at a time, but we can queue them
    # For true parallel, you'd need multiple Ollama instances
    for i, input_data in enumerate(inputs):
        result = process_task(host, model, task_type, input_data, timeout)
        result["index"] = i
        result["input_id"] = input_data.get("id", i)
        results.append(result)

        # Progress indicator
        print(f"Processed {i+1}/{len(inputs)}", file=sys.stderr)

    total_duration = time.time() - start_time
    successful = sum(1 for r in results if r.get("success", False))

    return {
        "success": successful == len(inputs),
        "total": len(inputs),
        "successful": successful,
        "failed": len(inputs) - successful,
        "total_duration_ms": int(total_duration * 1000),
        "results": results,
    }


# -----------------------------------------------------------------------------
# Output Validation
# -----------------------------------------------------------------------------

def validate_output(task_type: str, content: str) -> Dict[str, Any]:
    """Validate generated output for quality."""
    issues = []

    if not content or not content.strip():
        return {"valid": False, "issues": ["Empty output"], "confidence": "low"}

    if task_type == "commit":
        # Check commit message format
        lines = content.strip().split("\n")
        first_line = lines[0]

        # Check for type prefix
        valid_types = ["feat", "fix", "refactor", "perf", "test", "docs", "style", "chore", "ci", "build"]
        has_type = any(first_line.startswith(t) for t in valid_types)
        if not has_type:
            issues.append("Missing conventional commit type prefix")

        # Check length
        if len(first_line) > 72:
            issues.append("Subject line too long (>72 chars)")

        # Check for period
        if first_line.rstrip().endswith("."):
            issues.append("Subject line ends with period")

    elif task_type == "docstring":
        # Basic docstring validation
        if '"""' not in content and "'''" not in content:
            # Might be raw docstring content without quotes
            pass
        if len(content) < 10:
            issues.append("Docstring too short")

    elif task_type == "test":
        # Check for test patterns
        if "def test_" not in content and "it(" not in content and "[Test]" not in content:
            issues.append("No recognizable test patterns found")

    # Determine confidence
    if len(issues) == 0:
        confidence = "high"
    elif len(issues) <= 2:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "confidence": confidence,
        "content_length": len(content),
    }


# -----------------------------------------------------------------------------
# Model Selection
# -----------------------------------------------------------------------------

def select_model(
    host: str,
    task_type: str,
    prefer_quality: bool = False
) -> Dict[str, Any]:
    """Select best available model for task."""
    health = check_health(host)

    if not health["healthy"]:
        return {"success": False, "error": health["error"]}

    available = health["models_available"]

    # Get preferred model for task
    preferred = TASK_MODELS.get(task_type, TASK_MODELS["custom"])

    # Check if preferred is available
    preferred_base = preferred.split(":")[0]
    for model in available:
        if model.startswith(preferred_base):
            return {"success": True, "model": model, "reason": "preferred_available"}

    # Try fallbacks
    fallbacks = MODEL_FALLBACKS.get(preferred, [])
    for fallback in fallbacks:
        fallback_base = fallback.split(":")[0]
        for model in available:
            if model.startswith(fallback_base):
                return {"success": True, "model": model, "reason": "fallback_used"}

    # Use any available coding model
    coding_models = ["codestral", "deepseek", "starcoder", "codellama", "qwen"]
    for model in available:
        if any(cm in model.lower() for cm in coding_models):
            return {"success": True, "model": model, "reason": "any_coding_model"}

    # Last resort: use first available
    if available:
        return {"success": True, "model": available[0], "reason": "first_available"}

    return {"success": False, "error": "No models available"}


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Local LLM client for Ollama")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Ollama host URL")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ping (quick availability check)
    ping_parser = subparsers.add_parser("ping")
    ping_parser.add_argument("--output", "-o")

    # health (detailed check)
    health_parser = subparsers.add_parser("health")
    health_parser.add_argument("--output", "-o")

    # select-model
    select_parser = subparsers.add_parser("select-model")
    select_parser.add_argument("--task-type", "-t", required=True)
    select_parser.add_argument("--output", "-o")

    # ensure-model
    ensure_parser = subparsers.add_parser("ensure-model")
    ensure_parser.add_argument("--model", "-m", required=True)
    ensure_parser.add_argument("--output", "-o")

    # generate
    gen_parser = subparsers.add_parser("generate")
    gen_parser.add_argument("--model", "-m")
    gen_parser.add_argument("--task", "-t", required=True,
                           choices=["commit", "summary", "docstring", "test", "review", "custom"])
    gen_parser.add_argument("--input", "-i", required=True, help="JSON input data")
    gen_parser.add_argument("--timeout", type=int, default=120)
    gen_parser.add_argument("--output", "-o")

    # batch
    batch_parser = subparsers.add_parser("batch")
    batch_parser.add_argument("--model", "-m")
    batch_parser.add_argument("--task", "-t", required=True)
    batch_parser.add_argument("--input-file", "-i", required=True)
    batch_parser.add_argument("--concurrency", type=int, default=2)
    batch_parser.add_argument("--timeout", type=int, default=120)
    batch_parser.add_argument("--output", "-o")

    # validate
    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--task-type", "-t", required=True)
    validate_parser.add_argument("--content", "-c", help="Content to validate")
    validate_parser.add_argument("--result", "-r", help="Result JSON file to validate")
    validate_parser.add_argument("--output", "-o")

    args = parser.parse_args()
    result = None

    if args.command == "ping":
        result = ping(args.host)

    elif args.command == "health":
        result = check_health(args.host)

    elif args.command == "select-model":
        result = select_model(args.host, args.task_type)

    elif args.command == "ensure-model":
        result = ensure_model(args.host, args.model)

    elif args.command == "generate":
        # Select model if not specified
        model = args.model
        if not model:
            selection = select_model(args.host, args.task)
            if not selection["success"]:
                result = {"success": False, "error": selection["error"]}
            else:
                model = selection["model"]

        if model:
            input_data = json.loads(args.input)
            result = process_task(args.host, model, args.task, input_data, args.timeout)

            # Add validation
            if result.get("success"):
                validation = validate_output(args.task, result.get("content", ""))
                result["validation"] = validation

    elif args.command == "batch":
        model = args.model
        if not model:
            selection = select_model(args.host, args.task)
            if not selection["success"]:
                result = {"success": False, "error": selection["error"]}
            else:
                model = selection["model"]

        if model:
            with open(args.input_file) as f:
                inputs = json.load(f)
            result = process_batch(args.host, model, args.task, inputs,
                                  args.concurrency, args.timeout)

    elif args.command == "validate":
        if args.content:
            content = args.content
        elif args.result:
            with open(args.result) as f:
                data = json.load(f)
                content = data.get("content", "")
        else:
            parser.error("--content or --result required")
            return

        result = validate_output(args.task_type, content)

    # Output
    if result:
        output = json.dumps(result, indent=2)
        if hasattr(args, 'output') and args.output:
            with open(args.output, "w") as f:
                f.write(output)
        else:
            print(output)


if __name__ == "__main__":
    main()
