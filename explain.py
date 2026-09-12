import os
import re
from pathlib import Path
from dotenv import load_dotenv
import groq

load_dotenv(dotenv_path=Path(__file__).parent / ".env")
client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

_cache = {}


def get_stat_deltas(df, X, target_player, match_name, stat_names, top_k=3):
    target_idx = df.index[df["Name"] == target_player][0]
    match_idx = df.index[df["Name"] == match_name][0]

    target_vec = X[target_idx]
    match_vec = X[match_idx]
    stds = X.std(axis=0)

    deltas = [
        (name, abs(t - m) / (s if s > 0 else 1e-6))
        for name, t, m, s in zip(
            stat_names, target_vec, match_vec, stds
        )
    ]

    deltas.sort(key=lambda x: x[1])

    return (
        [d[0] for d in deltas[:top_k]],
        [d[0] for d in deltas[-2:]]
    )


def clean_explanation(text):
    if not text:
        return ""

    # Remove Qwen thinking blocks
    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE
    ).strip()

    # Remove common visible reasoning prefixes
    text = re.sub(
        r"^Here's a thinking process:.*?(?=(?:\n\s*\n)|$)",
        "",
        text,
        flags=re.DOTALL | re.IGNORECASE
    ).strip()

    # Remove common reasoning headings
    text = re.sub(
        r"^(Thinking|Reasoning|Analysis|Here's the analysis):\s*",
        "",
        text,
        flags=re.IGNORECASE
    ).strip()

    # If model produced numbered reasoning followed by final answer,
    # try to keep the final paragraph.
    paragraphs = [
        p.strip()
        for p in text.split("\n\n")
        if p.strip()
    ]

    if len(paragraphs) > 1:
        # Prefer the last paragraph as the final answer
        candidate = paragraphs[-1]

        if not re.match(
            r"^(1\.|2\.|Step|Analyze|Identify|Reasoning)",
            candidate,
            flags=re.IGNORECASE
        ):
            text = candidate

    return text.strip()


def get_explanation(row, target_player, df, X, stat_names):

    match_name = row["Name"]
    cache_key = f"{target_player}__{match_name}"

    if cache_key in _cache:
        return _cache[cache_key]

    most_similar, most_different = get_stat_deltas(
        df,
        X,
        target_player,
        match_name,
        stat_names
    )

    prompt = f"""
You are a football recruitment analyst.

Write ONLY a concise scouting explanation comparing two centre-backs.

STRICT RULES:
- Exactly 2 sentences.
- Do NOT show your reasoning.
- Do NOT provide a thinking process.
- Do NOT use headings.
- Do NOT use bullet points.
- Do NOT number the sentences.
- Return ONLY the final 2-sentence explanation.
- Use ONLY the data provided below.

Target: {target_player}
Replacement: {match_name}

Overall fit: {row['Overall']:.1f}
Tactical fit: {row['Tactical']:.1f}
Budget fit: {row['Budget']:.1f}
Age fit: {row['Age fit']:.1f}

Most similar statistical dimensions:
{', '.join(most_similar)}

Biggest statistical differences:
{', '.join(most_different)}
"""

    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        max_tokens=200,
        reasoning_format="hidden",
        reasoning_effort="none",
        messages=[
            {
                "role": "user",
                "content": prompt
                
            }
        ]
    )

    raw = response.choices[0].message.content

    # Clean model output before returning it
    explanation = clean_explanation(raw)

    # Store cleaned result
    _cache[cache_key] = explanation

    return explanation