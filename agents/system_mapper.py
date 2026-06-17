# agents/system_mapper.py

from pydantic import BaseModel, Field
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import json

load_dotenv()

# הגדרת המבנה של דוח התקלות שהסוכן ייצר
class Vulnerability(BaseModel):
    rule_violated: str = Field(description="The regulation rule that was violated")
    function_name: str = Field(description="The name of the function where the issue was found")
    description: str = Field(description="Explanation of why the code fails to meet the regulation")
    suggested_fix: str = Field(description="How to fix the code")

class AuditReport(BaseModel):
    vulnerabilities: List[Vulnerability] = Field(description="List of all compliance vulnerabilities found in the code")

class SystemMapperAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.structured_llm = self.llm.with_structured_output(AuditReport)
        
        # הפרומפט: הסוכן מקבל את החוקים מסוכן 1, ואת הקוד של הבנק
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Security and Compliance Code Auditor.
            You will receive a set of regulatory requirements (in JSON) and the source code of a financial system.
            Your job is to read the code and identify if and where the system fails to enforce the regulations.
            Return a detailed audit report in the requested JSON structure."""),
            ("user", "Regulatory Requirements:\n{requirements}\n\nSystem Source Code:\n{source_code}")
        ])

        self.auditor_chain = self.prompt | self.structured_llm

    def scan_code(self, requirements_json: str, code_text: str) -> AuditReport:
        print("System Mapper is analyzing the code against the regulations...")
        result = self.auditor_chain.invoke({
            "requirements": requirements_json,
            "source_code": code_text
        })
        return result

# ==========================================
# טסט מקומי לסוכן המיפוי
# ==========================================
if __name__ == "__main__":
    import os
    
    # 1. קריאת הקוד של הבנק שיצרנו
    code_path = os.path.join(os.path.dirname(__file__), '..', 'target_system', 'dummy_bank.py')
    with open(code_path, 'r', encoding='utf-8') as file:
        bank_code = file.read()
        
    # 2. ה-JSON שקיבלנו מהסוכן הראשון (העתקתי אותו ישירות מהתוצאה שלך!)
    agent_1_output = """
    {
      "requirements": [
        {
          "article_number": "Section 2",
          "legal_description": "Domestic transfers exceeding 50,000 ILS must be flagged and reviewed.",
          "technical_action": "Implement a system to flag and queue for manual review any domestic transfer exceeding 50,000 ILS."
        },
        {
          "article_number": "Section 3",
          "legal_description": "New accounts are restricted from initiating outgoing transfers for 24 hours after creation.",
          "technical_action": "Restrict new accounts from initiating outgoing transfers for the first 24 hours after account creation."
        }
      ]
    }
    """
    
    agent = SystemMapperAgent()
    audit_results = agent.scan_code(agent_1_output, bank_code)
    
    print("\n--- Compliance Audit Report (Agent 2) ---")
    print(audit_results.model_dump_json(indent=2))