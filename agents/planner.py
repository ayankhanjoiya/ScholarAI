from pydantic import BaseModel
class ResearchPlan(BaseModel):
    topic:str
    sub_questions: list[str]
## have chnaged the sub-questions from 4 to 2 but have to undo them
def plan(client,topic):
    response = client.models.generate_content(
        model = "gemini-3.5-flash",
        contents = f"""create a research plan for the topic : {topic}.
                  Generate 2 important sub-questions that should be investigated.""",
        config = {
            "response_mime_type": "application/json",
            "response_schema": ResearchPlan,    
        } 
    )
    return response.parsed


