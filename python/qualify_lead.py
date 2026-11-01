from __future__ import annotations
"""
AI Lead Qualification Script
----------------------------
Uses free models from OpenRouter or Groq.
Falls back to rule-based scoring if both APIs fail.
"""

import os
import json
import sys
from dotenv import load_dotenv

load_dotenv()

# ---------- Free AI Providers ----------

def call_openrouter(prompt: str) -> str | None:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        model = os.getenv("OPENROUTER_MODEL", "google/gemma-2-9b-it:free")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a lead qualification expert. "
                        "Score the lead as Hot, Warm, or Cold. "
                        "Reply ONLY with a JSON object like: "
                    '{"score": "Hot", "reason": "one real sentence about this lead", "priority": 1}'
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=800,
        )
        message = response.choices[0].message
        return message.content or getattr(message, "reasoning", None)
    except Exception as e:
        print(f"[OpenRouter Error] {e}", file=sys.stderr)
        return None


def call_groq(prompt: str) -> str | None:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None

    try:
        from openai import OpenAI
        client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key,
        )
        model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a lead qualification expert. "
                        "Score the lead as Hot, Warm, or Cold. "
                        "Reply ONLY with a JSON object like: "
                        '{"score": "Hot", "reason": "short reason", "priority": 1}'
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=150,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"[Groq Error] {e}", file=sys.stderr)
        return None


# ---------- Rule-based Fallback ----------

def rule_based_score(name: str, email: str, message: str, budget: str = "") -> dict:
    text = f"{name} {email} {message} {budget}".lower()

    hot_keywords = ["buy", "purchase", "urgent", "asap", "ready", "budget", "قیمت", "خرید", "فوری"]
    warm_keywords = ["interested", "info", "details", "more", "اطلاعات", "جزئیات"]

    if any(k in text for k in hot_keywords) or (budget and any(c.isdigit() for c in budget)):
        return {"score": "Hot", "reason": "Strong buying signals detected", "priority": 1}
    elif any(k in text for k in warm_keywords):
        return {"score": "Warm", "reason": "Shows interest, needs nurturing", "priority": 2}
    else:
        return {"score": "Cold", "reason": "Low engagement signals", "priority": 3}


# ---------- Main Logic ----------

def _parse_model_json(raw):
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[: text.rfind("```")]
        text = text.strip()
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        result = json.loads(text[start : end + 1])
    except Exception:
        return None
    if isinstance(result, dict) and "score" in result:
        result["source"] = "ai"
        return result
    return None


def qualify(lead):
    prompt = f"""
Lead Information:
- Name: {lead.get('name', 'Unknown')}
- Email: {lead.get('email', 'Unknown')}
- Phone: {lead.get('phone', 'N/A')}
- Message: {lead.get('message', '')}
- Budget: {lead.get('budget', 'Not mentioned')}
- Source: {lead.get('source', 'website')}
"""
    raw = call_openrouter(prompt) or call_groq(prompt)
    if raw:
        parsed = _parse_model_json(raw)
        if parsed:
            return parsed

    fallback = rule_based_score(
        lead.get("name", ""),
        lead.get("email", ""),
        lead.get("message", ""),
        lead.get("budget", ""),
    )
    fallback["source"] = "fallback"
    return fallback


if __name__ == "__main__":
    # Read lead from stdin (n8n will send it this way)
    try:
        input_data = sys.stdin.read()
        lead = json.loads(input_data)
    except Exception:
        # For manual testing
        lead = {
            "name": "Ali Rezaei",
            "email": "ali@example.com",
            "phone": "+98912...",
            "message": "I want to buy your course, what is the price?",
            "budget": "500$",
            "source": "website",
        }

    result = qualify(lead)
    print(json.dumps(result, ensure_ascii=False))