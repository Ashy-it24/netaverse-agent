import json
from services.llm_service import LLMService

class ReasoningAgent:
    def __init__(self):
        self.llm_service = LLMService()
        self.client = self.llm_service.get_client()

    async def analyze(self, name, raw_data):
        if not self.client:
            return {"error": "Groq API key not configured. Please set GROQ_API_KEY in .env"}

        # Prepare context from raw data
        wiki_extract = raw_data.get('wikipedia', {}).get('extract', 'No biography available.')
        news_articles = raw_data.get('news', [])
        news_context = "\n".join([f"- {a.get('title', '')}: {a.get('description', '')}" for a in news_articles])

        prompt = f"""
        You are an expert political analyst. Analyze the politician "{name}" based on the following real-time data and your internal knowledge base.

        DATA CONTEXT:
        Biography: {wiki_extract}
        Recent News:
        {news_context}

        TASK:
        Generate a detailed analysis in valid JSON format matching the structure below. 
        Ensure the analysis is neutral, factual, and comprehensive.
        
        REQUIRED JSON STRUCTURE:
        {{
            "politician": "{name}",
            "summary": "2-3 sentence professional summary of their current status and role.",
            "activities": [
                {{
                    "activity": "Description of recent action",
                    "category": "Legislation/Campaign/Diplomacy/Public Statement",
                    "impact": "positive/neutral/controversial"
                }}
            ],
            "promises": [
                {{
                    "promise": "Specific campaign promise",
                    "status": "fulfilled/partially_fulfilled/in_progress/not_fulfilled",
                    "evidence": "Brief evidence or context",
                    "impact": "High/Medium/Low impact description"
                }}
            ],
            "bills": [
                {{
                    "title": "Bill Name",
                    "year": "YYYY",
                    "description": "Short description",
                    "status": "Passed/Introduced/Failed"
                }}
            ]
        }}
        """

        completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-70b-8192",
            response_format={"type": "json_object"},
        )

        try:
            return json.loads(completion.choices[0].message.content)
        except json.JSONDecodeError:
            return {"error": "Failed to parse AI analysis"}