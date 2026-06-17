import streamlit as st
import json
from main import app as graph_app 

st.set_page_config(page_title="RegTech Hive", page_icon="🐝", layout="wide")

st.title("🐝 The RegTech Agent Hive - v2.0")
st.markdown("### 🌐 Dynamic Live-Research Compliance System")
st.markdown("---")

# שינוי: במקום תיבת טקסט גדולה, אנחנו נותנים למשתמש לבקש נושא למחקר
st.header("🔍 Research Regulation")
search_query = st.text_input("Enter a regulatory topic to research:", 
                             placeholder="e.g., Anti-money laundering requirements for crypto in Israel 2026")

code_path = 'target_system/dummy_bank.py'
try:
    with open(code_path, 'r', encoding='utf-8') as file:
        bank_code = file.read()
except:
    bank_code = "# Bank code not found."

st.header("💻 Target System Code")
sys_code = st.text_area("Source Code to Audit:", value=bank_code, height=200)

if st.button("🚀 Research & Audit", type="primary", use_container_width=True):
    if not search_query:
        st.warning("Please enter a research topic first!")
    else:
        with st.status("Agents are working...", expanded=True) as status:
            st.write("🕵️‍♂️ Agent 1 (Legal Researcher) is searching the web...")
            
            # העברת שאילתת החיפוש לתוך ה-State של הגרף
            initial_state = {
                "raw_regulation_text": search_query, 
                "bank_source_code": sys_code
            }
            
            final_state = graph_app.invoke(initial_state)
            
            st.write("🧑‍💻 Agent 2 (Mapper) is auditing code against findings...")
            st.write("🥷 Agent 3 (Red Team) is crafting payloads...")
            status.update(label="Analysis Complete!", state="complete", expanded=False)
            
        st.success("Research and Audit successful!")
        
        tab1, tab2 = st.tabs(["📊 Compliance Audit", "🎯 Red Team Plan"])
        with tab1:
            st.json(json.loads(final_state["vulnerabilities_report"]))
        with tab2:
            st.json(json.loads(final_state["attack_plan"]))