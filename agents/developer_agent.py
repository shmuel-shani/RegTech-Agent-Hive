# agents/developer_agent.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class DeveloperAgent:
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.1) # טמפרטורה נמוכה לכתיבת קוד מדויקת
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Python Security Developer.
            Your task is to fix the target source code based on the provided vulnerability report.
            You must apply the 'suggested_fix' into the code.
            Return ONLY the raw, functional Python code without any markdown formatting or explanations."""),
            ("human", "Original Code:\n{code}\n\nVulnerabilities:\n{vulnerabilities}")
        ])
        
        self.chain = self.prompt | self.llm

    def fix_code(self, original_code: str, vulnerabilities_json: str):
        result = self.chain.invoke({
            "code": original_code, 
            "vulnerabilities": vulnerabilities_json
        })
        
        # ניקוי פורמט של מארקדוון במידה והמודל התעקש להוסיף
        clean_code = result.content
        if "```python" in clean_code:
            clean_code = clean_code.split("```python")[1].split("```")[0].strip()
        elif "```" in clean_code:
            clean_code = clean_code.split("```")[1].split("```")[0].strip()
            
        return clean_code