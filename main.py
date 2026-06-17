# main.py

from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.legal_analyst import LegalAnalystAgent
from agents.system_mapper import SystemMapperAgent
from agents.red_team import RedTeamAgent  # <-- הוספנו את הסוכן החדש
import os

# 1. הזיכרון המשותף עכשיו כולל גם את תוכנית התקיפה
class RegTechState(TypedDict):
    raw_regulation_text: str
    extracted_requirements: str
    bank_source_code: str
    vulnerabilities_report: str
    attack_plan: str  # <-- שדה חדש בזיכרון

def legal_node(state: RegTechState):
    agent = LegalAnalystAgent()
    result = agent.analyze_document(state["raw_regulation_text"])
    return {"extracted_requirements": result}

def mapper_node(state: RegTechState):
    agent = SystemMapperAgent()
    result = agent.scan_code(state["extracted_requirements"], state["bank_source_code"])
    return {"vulnerabilities_report": result.model_dump_json(indent=2)}

# 2. הוספת הצומת של סוכן ה-Red Team
def red_team_node(state: RegTechState):
    agent = RedTeamAgent()
    # הוא מקבל את דוח התקלות מסוכן 2
    result = agent.generate_payloads(state["vulnerabilities_report"])
    return {"attack_plan": result.model_dump_json(indent=2)}

# 3. בניית השרשרת המלאה
workflow = StateGraph(RegTechState)

workflow.add_node("legal_analyst", legal_node)
workflow.add_node("system_mapper", mapper_node)
workflow.add_node("red_team_simulator", red_team_node) # סוכן 3

# הגדרת סדר זרימת המידע
workflow.set_entry_point("legal_analyst")
workflow.add_edge("legal_analyst", "system_mapper")
workflow.add_edge("system_mapper", "red_team_simulator") # מסוכן 2 לסוכן 3
workflow.add_edge("red_team_simulator", END)             # סיום התהליך

app = workflow.compile()