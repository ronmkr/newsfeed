# Prompt template for the Summarizer Node
SUMMARIZER_PROMPT = """
You are a neutral, objective news editor.
Summarize the following collection of articles into exactly 3 concise, neutral bullet points.
Focus on the factual events and avoid any subjective commentary.

Articles:
{article_content}
"""

# Prompt template for the Auditor Node
AUDITOR_PROMPT = """
You are an expert media analyst focusing on the Indian news landscape.
Analyze the following collection of articles for ideological bias and framing.
Use the provided SOURCE METADATA (Ownership/Funding) to contextualize the framing.

Articles:
{article_details}

Task:
1. Determine an overall political bias score for this cluster (-2 for Left, 0 for Center, +2 for Right).
2. Explain IF and HOW the ownership (e.g., corporate-owned, independent) influenced the framing of this story.
3. Are there any critical perspectives missing from this cluster?

Respond ONLY with a valid JSON object in the following format:
{{
    "bias_score": float,
    "ownership_influence_note": "string",
    "missing_perspectives": "string"
}}
"""
