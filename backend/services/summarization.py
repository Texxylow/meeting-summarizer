from groq import Groq
import json
import time

client = Groq()

MODEL = "llama-3.3-70b-versatile"

def summarize_chunk(chunk_text: str, retries: int = 5) -> dict:
    """
    Summarizes a single transcript chunk into structured JSON.
    Retries automatically if rate-limited.
    """
    prompt = f"""You are analyzing part of a meeting transcript. This is only ONE SECTION of a longer meeting — do not assume it's the whole meeting.

Extract the following from this section, in JSON format only, no markdown, no extra text:

{{
  "discussion_points": ["point 1", "point 2"],
  "decisions": ["decision 1"],
  "action_items": ["who needs to do what"],
  "open_questions": ["unresolved question 1"]
}}

If a category has nothing relevant in this section, return an empty list for it.

TRANSCRIPT SECTION:
{chunk_text}
"""

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            raw = response.choices[0].message.content
            cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
            return json.loads(cleaned)
        except Exception as e:
            error_str = str(e)
            if ("rate_limit" in error_str.lower() or "429" in error_str) and attempt < retries - 1:
                wait_time = 15
                print(f"Rate limited, waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                raise


def combine_summaries(chunk_summaries: list[dict]) -> dict:
    """
    Takes a list of per-chunk summary dicts and merges them into one
    final structured meeting summary, deduplicated and coherent.
    """
    combined_input = json.dumps(chunk_summaries, indent=2)

    prompt = f"""You are given a list of partial summaries extracted from consecutive sections of the same meeting. Merge them into a single, coherent final summary.

Rules:
- Deduplicate repeated or overlapping points across sections.
- Merge related points into single clear statements.
- Write a short "meeting_overview" paragraph (2-4 sentences) describing what the meeting was about overall.
- Keep action items attributed to the correct person where mentioned.

Return ONLY valid JSON in this exact format, no markdown, no extra text:

{{
  "meeting_overview": "short paragraph",
  "discussion_points": ["point 1", "point 2"],
  "decisions": ["decision 1"],
  "action_items": ["who needs to do what"],
  "open_questions": ["unresolved question 1"]
}}

PARTIAL SUMMARIES:
{combined_input}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    raw = response.choices[0].message.content
    cleaned = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    return json.loads(cleaned)