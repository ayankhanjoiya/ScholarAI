from google.genai import types


def synthesize(client, topic, research_results):

    prompt = f"""
You are ScholarAI, a research assistant.

Research topic:
{topic}

The following research was performed for this topic:

{research_results}

Using ONLY the research results above, create a coherent final research answer.

Requirements:
- Directly answer the research topic.
- Combine findings from the different sub-questions.
- Remove repetition.
- Clearly distinguish important findings.
- Do not invent information that is not present in the research results.
- Preserve citations that appear in the research results.
- If the research results are insufficient to answer something, say so.

Structure the answer as:

## Overview

A concise overview of the topic.

## Key Findings

Important findings from the research.

## Detailed Analysis

A synthesized explanation combining the research results.

## Sources

List the papers/sources referenced in the research results.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    return response.text