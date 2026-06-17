from typing import TypedDict
from langgraph.graph import StateGraph, END
import os
from dotenv import load_dotenv

from agents.legal_analyst import LegalAnalystAgent
from agents.system_mapper import SystemMapperAgent
from agents.red_team import RedTeamAgent
from agents.developer_agent import DeveloperAgent

load_dotenv()

class State(TypedDict):
    raw_regulation_text: str
    bank_source_code: str
    extracted_requirements: str
    vulnerabilities_report: str
    attack_plan: str
    fixed_code: str  

def legal_node(state: State):
    legal_agent = LegalAnalystAgent()
    result = legal_agent.analyze_document(state["raw_regulation_text"])
    return {"extracted_requirements": result}

def mapper_node(state: State):
    mapper_agent = SystemMapperAgent()
    # התיקון: קריאה ל-scan_code והעברת המשתנים בסדר הנכון!
    result = mapper_agent.scan_code(state["extracted_requirements"], state["bank_source_code"])
    return {"vulnerabilities_report": result.model_dump_json()}

def red_team_node(state: State):
    red_team = RedTeamAgent()
    # הערה: אם זה יקרוס כאן, זה אומר שגם ב-red_team.py שם הפונקציה שונה מ-generate_payloads
    result = red_team.generate_payloads(state["vulnerabilities_report"])
    return {"attack_plan": result.model_dump_json()}

def developer_node(state: State):
    dev_agent = DeveloperAgent()
    fixed_python_code = dev_agent.fix_code(state["bank_source_code"], state["vulnerabilities_report"])
    return {"fixed_code": fixed_python_code}

# --- בניית הגרף ---
graph_builder = StateGraph(State)

graph_builder.add_node("legal", legal_node)
graph_builder.add_node("mapper", mapper_node)
graph_builder.add_node("red_team", red_team_node)
graph_builder.add_node("developer", developer_node)

# מסלול טורי לחלוטין - מונע התנגשויות זיכרון בשרת
graph_builder.set_entry_point("legal")
graph_builder.add_edge("legal", "mapper")
graph_builder.add_edge("mapper", "red_team")
graph_builder.add_edge("red_team", "developer") # שינוי קריטי: עוברים מסוכן 3 לסוכן 4!
graph_builder.add_edge("developer", END)

app = graph_builder.compile()