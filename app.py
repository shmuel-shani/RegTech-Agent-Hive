import streamlit as st
import json
from main import app as graph_app 

st.set_page_config(page_title="RegTech Hive", page_icon="🐝", layout="wide")

st.title("🐝 The RegTech Agent Hive - v2.0")
st.markdown("### 🌐 Dynamic Live-Research Compliance System")
st.markdown("---")

# שורת החיפוש הדינמית
st.header("🔍 Research Regulation")
search_query = st.text_input("Enter a regulatory topic to research:", 
                             placeholder="e.g., Anti-money laundering requirements for crypto in Israel 2026")

# טעינת קוד המקור של המערכת
code_path = 'target_system/dummy_bank.py'
try:
    with open(code_path, 'r', encoding='utf-8') as file:
        bank_code = file.read()
except:
    bank_code = "# Bank code not found. Please create target_system/dummy_bank.py"

st.header("💻 Target System Code")
sys_code = st.text_area("💻 Target System Code (Feel free to edit or paste your own code!): "
"כאן ניתן לראות קוד של מערכת דמה של בנק וירטואלי (מערכת עם חורי אבטחה ובעיות ציות מכוונות)"
"תרגישו חופשי להכניס קוד משלכם כדי שהמערכת תסרוק בה את הכשלים", value=bank_code, height=300)

if st.button("🚀 Research & Audit", type="primary", use_container_width=True):
    if not search_query:
        st.warning("Please enter a research topic first!")
    else:
        # אנימציית טעינה וסטטוס של הסוכנים
        with st.status("Agents are working...", expanded=True) as status:
            st.write("🕵️‍♂️ Agent 1 (Legal Researcher) is searching the web...")
            
            initial_state = {
                "raw_regulation_text": search_query, 
                "bank_source_code": sys_code
            }
            
            # הפעלת הגרף הראשי
            final_state = graph_app.invoke(initial_state)
            
            st.write("🧑‍💻 Agent 2 (Mapper) is auditing code against findings...")
            st.write("🥷 Agent 3 (Red Team) is crafting payloads...")
            st.write("🛠️ Agent 4 (Developer) is writing the fix...")
            status.update(label="Analysis Complete!", state="complete", expanded=False)
            
        st.success("Research, Audit, and Auto-Remediation successful!")
        
        # תצוגת התוצאות בשלושה טאבים
        tab1, tab2, tab3 = st.tabs(["📊 Compliance Audit", "🎯 Red Team Plan", "🛠️ Auto-Fixed Code"])
        
        with tab1:
            try:
                st.json(json.loads(final_state["vulnerabilities_report"]))
            except:
                st.write(final_state["vulnerabilities_report"])
                
        with tab2:
            try:
                st.json(json.loads(final_state["attack_plan"]))
            except:
                st.write(final_state["attack_plan"])
                
        with tab3:
            st.markdown("### The system has automatically patched the vulnerabilities:")
            # הצגת הקוד המתוקן מתוך ה-State בפורמט של פייתון
            st.code(final_state.get("fixed_code", "# No code generated."), language="python")