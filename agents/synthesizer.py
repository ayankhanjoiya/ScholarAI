from google.genai import types


def synthesize(client, topic, research_results):

    prompt = f"""
You are ScholarAI, a research assistant.

Research topic:
{topic}

Research results from the investigation:
{research_results}

Using ONLY the research results above, create the final research answer.

IMPORTANT RULES:
- Do not add facts that are not present in the research results.
- Combine information from all relevant sub-questions.
- Remove duplicate information.
- Clearly explain the most important findings.
- Preserve all useful citations from the research results.
- Do not invent authors, papers, page numbers, DOIs, or citations.
- If a claim has a citation in the research results, keep that citation.
- If the evidence is insufficient for a claim, explicitly say so.
- Do not mention the internal agent, tools, or research process.

Use exactly this structure:

## Overview

Give a concise overview answering the main research topic.

## Key Findings

Give the most important findings as bullet points.

## Detailed Analysis

Synthesize the research results into a coherent explanation.
Use subsections when useful.

## Sources

List the sources that were actually referenced in the research results.

For each source, preserve the available:
- paper title
- page number
- paper ID or DOI if available

Do not create missing source information.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text