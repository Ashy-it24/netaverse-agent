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
        You are an expert global political analyst. Analyze the politician "{name}" based on the following real-time data and your comprehensive knowledge base.

        DATA CONTEXT:
        Biography: {wiki_extract}
        Recent News:
        {news_context}

        CRITICAL INSTRUCTIONS:
        1. Generate information SPECIFIC and UNIQUE to "{name}" - do NOT use generic placeholder data
        2. Include REAL activities, promises, and legislative record that this specific politician has been associated with
        3. Use accurate dates, policy positions, and political context specific to this politician and their country
        4. For promises, evaluate their ACTUAL fulfillment status based on real-world outcomes
        5. The analysis must be factual, globally aware, and traceable to real events
        6. Adapt to the political system of their country (parliamentary, presidential, etc.)

        TASK:
        Generate a detailed analysis in valid JSON format matching the structure below.
        Ensure the analysis is neutral, factual, comprehensive, and globally applicable.
        
        REQUIRED JSON STRUCTURE:
        {{
            "politician": "{name}",
            "party": "The political party they belong to (adapt to country's political system)",
            "position": "Their current or most recent political position (Prime Minister, President, MP, etc.)",
            "term_period": "Their term period (e.g., 2019-2024, 2020-present)",
            "summary": "2-3 sentence professional summary of their current status and role, specific to this politician and their country.",
            "activities": [
                {{
                    "activity": "Description of a REAL recent action specific to {name}",
                    "date": "YYYY-MM or approximate date",
                    "category": "Legislation/Campaign/Diplomacy/Public Statement/Executive Action/Policy Initiative",
                    "impact": "positive/neutral/controversial",
                    "details": "Additional context about this specific activity"
                }}
            ],
            "promises": [
                {{
                    "promise": "A SPECIFIC promise or commitment made by {name}",
                    "made_during": "Campaign/Term year or context when promise was made",
                    "status": "fulfilled/partially_fulfilled/in_progress/not_fulfilled/broken",
                    "fulfillment_percentage": 0-100,
                    "evidence": "Specific evidence of progress or lack thereof",
                    "timeline": "Expected or actual completion timeline",
                    "impact": "High/Medium/Low impact description on constituents"
                }}
            ],
            "bills": [
                {{
                    "title": "Actual Bill/Law/Policy Name associated with {name}",
                    "bill_number": "Official bill number if applicable, or N/A",
                    "year": "YYYY",
                    "description": "What this bill/policy does",
                    "status": "Passed/Introduced/Failed/Signed into Law/Enacted/Under Review",
                    "role": "Sponsor/Co-sponsor/Supporter/Opponent/Signed/Voted For",
                    "impact_area": "Healthcare/Economy/Environment/Defense/Education/Infrastructure/etc."
                }}
            ],
            "promise_analysis": {{
                "total_promises_tracked": "Number of major promises tracked",
                "fulfilled_count": "Number of promises fulfilled",
                "partially_fulfilled_count": "Number partially fulfilled",
                "in_progress_count": "Number in progress",
                "not_fulfilled_count": "Number not fulfilled",
                "overall_fulfillment_rate": "Percentage of promises kept",
                "strongest_areas": ["Areas where promises were kept"],
                "weakest_areas": ["Areas where promises were not kept"],
                "analysis_summary": "A 2-3 sentence summary analyzing their promise fulfillment record"
            }},
            "voting_record_summary": {{
                "key_votes": [
                    {{
                        "issue": "Key issue voted on or position taken",
                        "position": "For/Against/Abstained/Supported/Opposed",
                        "year": "YYYY"
                    }}
                ],
                "alignment": "How they typically vote or their political alignment (progressive/moderate/conservative/centrist)"
            }},
            "controversies": [
                {{
                    "issue": "Brief description of controversy or challenge",
                    "year": "YYYY",
                    "resolution": "How it was resolved or current status"
                }}
            ],
            "data_sources": ["List sources used for this analysis"]
        }}
        
        Remember: All data must be SPECIFIC to "{name}" and based on real, verifiable information.
        Include at least 4-6 activities, 5-7 promises with fulfillment analysis, and 4-6 bills/policies.
        Adapt the content to the political system and context of their country.
        """

        try:
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.1-8b-instant",
                response_format={"type": "json_object"},
            )
        except Exception as e:
            return {"error": f"An error occurred while communicating with the AI model: {e}"}

        try:
            result = json.loads(completion.choices[0].message.content)
            # Ensure promise_analysis is calculated even if LLM doesn't provide it
            result = self._ensure_promise_analysis(result)
            return result
        except json.JSONDecodeError:
            return {"error": "Failed to parse AI analysis"}

    def _ensure_promise_analysis(self, data):
        """Calculate promise analysis metrics if not provided or incomplete"""
        promises = data.get('promises', [])
        
        if not promises:
            return data
        
        # Calculate metrics from promises
        fulfilled = sum(1 for p in promises if p.get('status') == 'fulfilled')
        partially = sum(1 for p in promises if p.get('status') == 'partially_fulfilled')
        in_progress = sum(1 for p in promises if p.get('status') == 'in_progress')
        not_fulfilled = sum(1 for p in promises if p.get('status') in ['not_fulfilled', 'broken'])
        
        total = len(promises)
        
        # Calculate fulfillment rate (fulfilled + 0.5 * partially fulfilled)
        fulfillment_rate = round(((fulfilled + 0.5 * partially) / total) * 100, 1) if total > 0 else 0
        
        # Ensure promise_analysis exists and has calculated values
        if 'promise_analysis' not in data:
            data['promise_analysis'] = {}
        
        analysis = data['promise_analysis']
        analysis['total_promises_tracked'] = total
        analysis['fulfilled_count'] = fulfilled
        analysis['partially_fulfilled_count'] = partially
        analysis['in_progress_count'] = in_progress
        analysis['not_fulfilled_count'] = not_fulfilled
        analysis['calculated_fulfillment_rate'] = f"{fulfillment_rate}%"
        
        # Calculate average fulfillment percentage from individual promises
        percentages = [p.get('fulfillment_percentage', 0) for p in promises if isinstance(p.get('fulfillment_percentage'), (int, float))]
        if percentages:
            analysis['average_fulfillment_percentage'] = round(sum(percentages) / len(percentages), 1)
        
        return data