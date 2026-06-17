from typing import TypedDict
from langgraph.graph import StateGraph, END
import os
from dotenv import load_dotenv

# ייבוא כל ארבעת הסוכנים שלנו
from agents.legal_analyst import LegalAnalystAgent
from agents.system_mapper import SystemMapperAgent
from agents.red_team import RedTeamAgent
from agents.developer_agent import DeveloperAgent

load_dotenv()

# הגדרת מצב המערכת (State) שעובר מנקודה לנקודה בגרף
class State(TypedDict):
    raw_regulation_text: str
    bank_source_code: str
    extracted_requirements: str
    vulnerabilities_report: str
    attack_plan: str
    fixed_code: str  # התוצר של סוכן התיקון האוטומטי

# צומת 1: החוקר המשפטי (יוצא לאינטרנט להביא רגולציה)
def legal_node(state: State):
    legal_agent = LegalAnalystAgent()
    result = legal_agent.analyze_document(state["raw_regulation_text"])
    # התיקון: מחזירים טקסט נקי
    return {"extracted_requirements": result}

# צומת 2: סורק הקוד (משווה בין הקוד לרגולציה)
def mapper_node(state: State):
    mapper_agent = SystemMapperAgent()
    result = mapper_agent.audit_code(state["bank_source_code"], state["extracted_requirements"])
    return {"vulnerabilities_report": result}

# צומת 3: צוות תקיפה (בונה פיילודים על בסיס החולשות)
def red_team_node(state: State):
    red_team = RedTeamAgent()
    result = red_team.generate_payloads(state["vulnerabilities_report"])
    return {"attack_plan": result}

# צומת 4: מפתח אבטחת מידע (כותב תיקון לקוד במקביל)
def developer_node(state: State):
    dev_agent = DeveloperAgent()
    fixed_python_code = dev_agent.fix_code(state["bank_source_code"], state["vulnerabilities_report"])
    return {"fixed_code": fixed_python_code}

# --- בניית הגרף (המוח של המערכת) ---
graph_builder = StateGraph(State)

# הוספת הצמתים לגרף
graph_builder.add_node("legal", legal_node)
graph_builder.add_node("mapper", mapper_node)
graph_builder.add_node("red_team", red_team_node)
graph_builder.add_node("developer", developer_node)

# הגדרת מסלול הזרימה
graph_builder.set_entry_point("legal")
graph_builder.add_edge("legal", "mapper")

# פיצול: אחרי סריקת הקוד, המערכת מתכננת תקיפה ומפתחת תיקון *במקביל*
graph_builder.add_edge("mapper", "red_team")
graph_builder.add_edge("mapper", "developer")

# סיום המסלולים
graph_builder.add_edge("red_team", END)
graph_builder.add_edge("developer", END)

# קימפול המערכת למוצר עובד
app = graph_builder.compile()