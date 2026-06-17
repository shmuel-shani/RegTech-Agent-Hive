# agents/legal_analyst.py
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class LegalAnalystAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        # זה הכלי שמאפשר לסוכן "לצאת" לאינטרנט
        self.search_tool = TavilySearchResults(max_results=3)
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Legal Compliance Analyst.
            Your task is to research regulations online using the search tool.
            After gathering information, extract the requirements into a specific JSON format:
            {
                "requirements": [
                    {"article_number": "...", "legal_description": "...", "technical_action": "..."}
                ]
            }
            Ensure the output is strictly valid JSON."""),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}"),
        ])
        
        self.agent = create_tool_calling_agent(self.llm, [self.search_tool], self.prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=[self.search_tool], verbose=True)

    def analyze_document(self, topic: str):
        # במקום לקבל טקסט סטטי, הסוכן מבצע חיפוש חי
        result = self.executor.invoke({"input": f"Research: {topic}. Then extract requirements into JSON."})
        
        # אנחנו מחלצים את ה-JSON מתוך התשובה המילולית של הסוכן
        # (זה טריק קטן כדי להבטיח שהתוצאה תהיה נקייה)
        raw_output = result['output']
        if "```json" in raw_output:
            raw_output = raw_output.split("```json")[1].split("```")[0]
        elif "```" in raw_output:
            raw_output = raw_output.split("```")[1].split("```")[0]
            
        return raw_output