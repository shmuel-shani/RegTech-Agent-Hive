# agents/red_team.py

from pydantic import BaseModel, Field
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

# 1. הגדרת המבנה של "מטען התקיפה" (Payload)
class ExploitPayload(BaseModel):
    target_vulnerability: str = Field(description="The specific rule or section being exploited")
    transfer_amount: int = Field(description="The amount of money to transfer in the simulation")
    account_age_hours: int = Field(description="The simulated age of the account in hours")
    attack_description: str = Field(description="Explanation of why this payload will bypass the system")

class AttackSimulation(BaseModel):
    payloads: List[ExploitPayload] = Field(description="List of attacks to execute against the system")

class RedTeamAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        # כאן אנחנו נותנים למודל קצת יותר יצירתיות (temperature 0.2) כדי שיוכל לחשוב כמו תוקף
        self.llm = ChatOpenAI(model=model_name, temperature=0.2)
        self.structured_llm = self.llm.with_structured_output(AttackSimulation)
        
        # 2. הפרומפט: הסוכן הופך להאקר שצריך לייצר מקרי בדיקה זדוניים
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Red-Team code exploitation AI.
            You will receive a vulnerability report for a financial system.
            Your job is to generate test transactions (payloads) that exploit these EXACT vulnerabilities.
            Generate payloads that SHOULD be blocked by the regulation, but WILL pass successfully because of the bugs described in the report.
            Output exactly in the requested JSON structure."""),
            ("user", "Vulnerability Report:\n{vulnerabilities}")
        ])

        self.attack_chain = self.prompt | self.structured_llm

    def generate_payloads(self, report_json: str) -> AttackSimulation:
        """
        מקבל את דוח התקלות ומייצר מערך תקיפה
        """
        print("Red Team is crafting exploit payloads...")
        result = self.attack_chain.invoke({"vulnerabilities": report_json})
        return result

# ==========================================
# טסט מקומי לסוכן התקיפה
# ==========================================
if __name__ == "__main__":
    # אנחנו מזינים לו דוגמה מקוצרת של דוח תקלות
    sample_report = """
    {
      "vulnerabilities": [
        {
          "rule_violated": "Section 2",
          "description": "The code does not check if the transfer amount exceeds 50,000 ILS."
        },
        {
          "rule_violated": "Section 3",
          "description": "The code does not restrict new accounts under 24 hours from making transfers."
        }
      ]
    }
    """
    
    agent = RedTeamAgent()
    attack_plan = agent.generate_payloads(sample_report)
    
    print("\n--- Red Team Attack Plan (Agent 3) ---")
    print(attack_plan.model_dump_json(indent=2))