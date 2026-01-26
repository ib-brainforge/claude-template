#!/usr/bin/env python3
"""
LM Studio client for local LLM integration.

LM Studio provides an OpenAI-compatible API, making it easy to integrate.

Handles:
- Health checks (ping)
- Task-specific prompt construction
- Generation via OpenAI-compatible API
- Output validation

Usage:
    python lmstudio-client.py ping --host http://localhost:1234
    python lmstudio-client.py health --host http://localhost:1234
    python lmstudio-client.py generate --task commit --input '{"diff": "..."}'
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


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

DEFAULT_HOST = os.environ.get("LMSTUDIO_HOST", "http://localhost:1234")

# Generation parameters per task (same as Ollama for consistency)
TASK_PARAMS = {
    "commit": {"temperature": 0.3, "top_p": 0.9, "max_tokens": 500},
    "summary": {"temperature": 0.5, "top_p": 0.9, "max_tokens": 1000},
    "docstring": {"temperature": 0.3, "top_p": 0.9, "max_tokens": 500},
    "test": {"temperature": 0.4, "top_p": 0.95, "max_tokens": 2000},
    "review": {"temperature": 0.3, "top_p": 0.9, "max_tokens": 1500},
    "custom": {"temperature": 0.5, "top_p": 0.9, "max_tokens": 1000},
}

# Prompts (same as Ollama for consistency)
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
# LM Studio API Client (OpenAI-compatible)
# -----------------------------------------------------------------------------

def ping(host: str, timeout: int = 5) -> Dict[str, Any]:
    """
    Quick ping to check if LM Studio is running.
    Returns simple available/unavailable status.
    """
    url = f"{host.rstrip('/')}/v1/models"

    try:
        req = Request(url, method="GET")
        with urlopen(req, timeout=timeout) as response:
            return {
                "available": True,
                "host": host,
                "status": "running"
            }
    except URLError as e:
        return {
            "available": False,
            "host": host,
            "status": "unavailable",
            "error": f"Cannot connect: {e.reason}"
        }
    except Exception as e:
        return {
            "available": False,
            "host": host,
            "status": "error",
            "error": str(e)
        }


def check_health(host: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Full health check with model information.
    """
    # First do a quick ping
    ping_result = ping(host, timeout)
    if not ping_result["available"]:
        return {
            "healthy": False,
            "available": False,
            **ping_result
        }

    # Get model info
    url = f"{host.rstrip('/')}/v1/models"

    try:
        req = Request(url, method="GET")
        with urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode())

        models = data.get("data", [])
        model_ids = [m.get("id", "unknown") for m in models]

        return {
            "healthy": True,
            "available": True,
            "host": host,
            "models_loaded": model_ids,
            "model_count": len(model_ids),
            "status": "ready" if model_ids else "no_model_loaded"
        }
    except Exception as e:
        return {
            "healthy": False,
            "available": True,  # Server is up but something's wrong
            "host": host,
            "error": str(e),
            "status": "error"
        }


def generate(
    host: str,
    prompt: str,
    system_prompt: str = "You are a helpful coding assistant.",
    temperature: float = 0.5,
    top_p: float = 0.9,
    max_tokens: int = 1000,
    timeout: int = 120
) -> Dict[str, Any]:
    """Generate text using LM Studio's OpenAI-compatible API."""
    url = f"{host.rstrip('/')}/v1/chat/completions"
    start_time = time.time()

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer lm-studio"  # LM Studio accepts any key
    }

    data = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "stream": False
    }

    try:
        req = Request(
            url,
            data=json.dumps(data).encode(),
            headers=headers,
            method="POST"
        )

        with urlopen(req, timeout=timeout) as response:
            result = json.loads(response.read().decode())

        duration = time.time() - start_time

        # Extract response
        choices = result.get("choices", [])
        content = choices[0]["message"]["content"] if choices else ""

        # Get usage info
        usage = result.get("usage", {})

        return {
            "success": True,
            "available": True,
            "content": content,
            "model": result.get("model", "unknown"),
            "duration_ms": int(duration * 1000),
            "tokens_prompt": usage.get("prompt_tokens", 0),
            "tokens_completion": usage.get("completion_tokens", 0),
            "tokens_total": usage.get("total_tokens", 0),
        }

    except URLError as e:
        return {
            "success": False,
            "available": False,
            "error": f"Cannot connect: {e.reason}",
            "duration_ms": int((time.time() - start_time) * 1000),
        }
    except HTTPError as e:
        return {
            "success": False,
            "available": True,
            "error": f"HTTP {e.code}: {e.read().decode() if e.fp else ''}",
            "duration_ms": int((time.time() - start_time) * 1000),
        }
    except Exception as e:
        return {
            "success": False,
            "available": True,
            "error": str(e),
            "duration_ms": int((time.time() - start_time) * 1000),
        }


# -----------------------------------------------------------------------------
# Task Processing
# -----------------------------------------------------------------------------

def build_prompt(task_type: str, input_data: Dict[str, Any]) -> str:
    """Build prompt from template and input data."""
    template = PROMPTS.get(task_type, PROMPTS.get("custom", "{prompt}"))

    if task_type == "custom" and "prompt" in input_data:
        return input_data["prompt"]

    try:
        return template.format(**input_data)
    except KeyError as e:
        raise ValueError(f"Missing required input field: {e}")


def process_task(
    host: str,
    task_type: str,
    input_data: Dict[str, Any],
    timeout: int = 120
) -> Dict[str, Any]:
    """Process a single task."""
    # Check availability first
    ping_result = ping(host, timeout=5)
    if not ping_result["available"]:
        return {
            "success": False,
            "available": False,
            "error": ping_result.get("error", "LM Studio unavailable"),
            "fallback_recommended": True
        }

    # Get task parameters
    params = TASK_PARAMS.get(task_type, TASK_PARAMS["custom"])

    # Build prompt
    try:
        prompt = build_prompt(task_type, input_data)
    except ValueError as e:
        return {"success": False, "available": True, "error": str(e)}

    # System prompt based on task
    system_prompts = {
        "commit": "You are a git commit message generator. Follow conventional commits format strictly.",
        "summary": "You are a code documentation assistant. Be concise and accurate.",
        "docstring": "You are a documentation generator. Follow standard docstring formats.",
        "test": "You are a test generation assistant. Write comprehensive, runnable tests.",
        "review": "You are a code reviewer. Identify issues clearly with line references.",
    }
    system_prompt = system_prompts.get(task_type, "You are a helpful coding assistant.")

    # Generate
    result = generate(
        host=host,
        prompt=prompt,
        system_prompt=system_prompt,
        temperature=params["temperature"],
        top_p=params["top_p"],
        max_tokens=params["max_tokens"],
        timeout=timeout
    )

    # Add fallback recommendation if failed
    if not result.get("success"):
        result["fallback_recommended"] = True

    return result


def validate_output(task_type: str, content: str) -> Dict[str, Any]:
    """Validate generated output for quality."""
    issues = []

    if not content or not content.strip():
        return {
            "valid": False,
            "issues": ["Empty output"],
            "confidence": "low",
            "fallback_recommended": True
        }

    if task_type == "commit":
        lines = content.strip().split("\n")
        first_line = lines[0]

        valid_types = ["feat", "fix", "refactor", "perf", "test", "docs", "style", "chore", "ci", "build"]
        has_type = any(first_line.startswith(t) for t in valid_types)
        if not has_type:
            issues.append("Missing conventional commit type prefix")

        if len(first_line) > 72:
            issues.append("Subject line too long (>72 chars)")

        if first_line.rstrip().endswith("."):
            issues.append("Subject line ends with period")

    elif task_type == "test":
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
        "fallback_recommended": confidence == "low"
    }


# -----------------------------------------------------------------------------
# CLI
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="LM Studio client")
    parser.add_argument("--host", default=DEFAULT_HOST, help="LM Studio host URL")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # ping (quick availability check)
    ping_parser = subparsers.add_parser("ping")
    ping_parser.add_argument("--output", "-o")

    # health (detailed health check)
    health_parser = subparsers.add_parser("health")
    health_parser.add_argument("--output", "-o")

    # generate
    gen_parser = subparsers.add_parser("generate")
    gen_parser.add_argument("--task", "-t", required=True,
                           choices=["commit", "summary", "docstring", "test", "review", "custom"])
    gen_parser.add_argument("--input", "-i", required=True, help="JSON input data")
    gen_parser.add_argument("--timeout", type=int, default=120)
    gen_parser.add_argument("--output", "-o")

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

    elif args.command == "generate":
        input_data = json.loads(args.input)
        result = process_task(args.host, args.task, input_data, args.timeout)

        # Add validation if successful
        if result.get("success"):
            validation = validate_output(args.task, result.get("content", ""))
            result["validation"] = validation

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
