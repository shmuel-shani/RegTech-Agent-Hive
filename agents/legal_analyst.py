# agents/legal_analyst.py
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

load_dotenv()

class LegalAnalystAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.search_tool = TavilySearchResults(max_results=3)
        
        # אנחנו עוקפים לחלוטין את langchain.agents התקול
        # ומשתמשים במנוע החדשני של LangGraph כדי להריץ את הסוכן!
        self.agent_executor = create_react_agent(
            self.llm,
            tools=[self.search_tool]
        )

    def analyze_document(self, topic: str):
        system_prompt = """You are an expert Legal Compliance Analyst.
        Your task is to research regulations online using the search tool.
        After gathering information, extract the requirements into a specific JSON format:
        {
            "requirements": [
                {"article_number": "...", "legal_description": "...", "technical_action": "..."}
            ]
        }
        Ensure the output is strictly valid JSON."""
        
        # סוכני LangGraph מקבלים רשימה של הודעות
        inputs = {
            "messages": [
                ("system", system_prompt),
                ("user", f"Research: {topic}. Then extract requirements into JSON.")
            ]
        }
        
        result = self.agent_executor.invoke(inputs)
        
        # התוצאה הסופית היא התוכן של ההודעה האחרונה שהסוכן ייצר
        raw_output = result["messages"][-1].content
        
        if "```json" in raw_output:
            raw_output = raw_output.split("```json")[1].split("```")[0]
        elif "```" in raw_output:
            raw_output = raw_output.split("```")[1].split("```")[0]
            
        return raw_output