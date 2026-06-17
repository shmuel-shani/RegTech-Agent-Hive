from pydantic import BaseModel, Field
from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# טעינת מפתח ה-API מקובץ ה-.env שיצרנו
load_dotenv()

# 1. הגדרת הסכמה (Schema) - איך ייראה ה-JSON שנפלוט לסוכן 2
class ActionableRequirement(BaseModel):
    article_number: str = Field(description="The section or article number in the regulation")
    legal_description: str = Field(description="A brief description of the legal requirement")
    technical_action: str = Field(description="The specific operational/technical requirement needed in the code (e.g., 'Verify transaction limit under 10000')")

class RegulationExtraction(BaseModel):
    requirements: List[ActionableRequirement] = Field(description="List of all actionable items found in the text")

class LegalAnalystAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        # אתחול המודל עם חוקים נוקשים לפלוט רק את המבנה שהגדרנו
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.structured_llm = self.llm.with_structured_output(RegulationExtraction)
        
        # 2. כתיבת הפרומפט לסוכן
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Legal & Compliance Analyst in the financial sector. 
            Your task is to read regulation text and extract ONLY the actionable, technical, or operational rules.
            Ignore general statements. Focus on constraints, limits, required checks, and data protection rules.
            Output exactly in the requested JSON structure."""),
            ("user", "Here is the regulation text:\n\n{regulation_text}")
        ])

        # חיבור הפרומפט למודל
        self.extractor_chain = self.prompt | self.structured_llm

    def analyze_document(self, text: str) -> RegulationExtraction:
        """
        מקבל טקסט של רגולציה ומחזיר JSON מובנה
        """
        print("Legal Analyst is reviewing the regulation...")
        result = self.extractor_chain.invoke({"regulation_text": text})
        return result

# ==========================================
# קוד לבדיקה מקומית (טסט קצר)
# ==========================================
if __name__ == "__main__":
    sample_regulation = """
    Directive 45: Anti-Money Laundering Controls
    Section 1: General Purpose
    This directive aims to secure the financial system.
    
    Section 2: Transaction Limits
    Any domestic transfer exceeding 50,000 ILS must be flagged and undergo manual review.
    
    Section 3: Account Verification
    New accounts cannot initiate outgoing transfers for the first 24 hours after creation.
    """
    
    agent = LegalAnalystAgent()
    extracted_json = agent.analyze_document(sample_regulation)
    
    print("\n--- Extracted JSON Output for Agent 2 ---")
    print(extracted_json.model_dump_json(indent=2))