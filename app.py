# app.py

import streamlit as st
import json
import os
from main import app as graph_app 

st.set_page_config(page_title="RegTech Hive", page_icon="🐝", layout="wide")

st.title("🐝 The RegTech Agent Hive")
st.markdown("### Multi-Agent Compliance & Security Management System")
st.markdown("---")

sample_regulation = """
Directive 45: Anti-Money Laundering Controls
Section 2: Transaction Limits
Any domestic transfer exceeding 50,000 ILS must be flagged and undergo manual review.
Section 3: Account Verification
New accounts cannot initiate outgoing transfers for the first 24 hours after creation.
"""

code_path = os.path.join(os.path.dirname(__file__), 'target_system', 'dummy_bank.py')
try:
    with open(code_path, 'r', encoding='utf-8') as file:
        bank_code = file.read()
except FileNotFoundError:
    bank_code = "# Error: File not found."

col1, col2 = st.columns(2)

with col1:
    st.header("📄 Regulation Input")
    st.caption("Agent 1 (Legal) analyzes this text.")
    reg_text = st.text_area("Upload Regulation Text:", value=sample_regulation, height=300)

with col2:
    st.header("💻 Target System Code")
    st.caption("Agent 2 (Mapper) scans this code.")
    sys_code = st.text_area("Bank Source Code:", value=bank_code, height=300)

st.markdown("---")

if st.button("🚀 Run Complete AI Pipeline", type="primary", use_container_width=True):
    
    with st.status("Agents are communicating...", expanded=True) as status:
        st.write("🕵️‍♂️ Agent 1 (Legal Analyst) is extracting rules...")
        
        initial_state = {
            "raw_regulation_text": reg_text,
            "bank_source_code": sys_code
        }
        
        # הרצת כל הסוכנים יחד!
        final_state = graph_app.invoke(initial_state)
        
        st.write("🧑‍💻 Agent 2 (System Mapper) is auditing the code...")
        st.write("🥷 Agent 3 (Red Team) is crafting exploit payloads...")
        status.update(label="System Analysis Complete!", state="complete", expanded=False)
        
    st.success("Multi-Agent pipeline executed successfully!")
    
    # חלוקה ללשוניות כדי להציג את התוצאות של סוכן 2 וסוכן 3
    tab1, tab2 = st.tabs(["📊 Compliance Audit Report (Agent 2)", "🎯 Red Team Attack Plan (Agent 3)"])
    
    with tab1:
        try:
            st.json(json.loads(final_state["vulnerabilities_report"]))
        except:
            st.code(final_state["vulnerabilities_report"], language="json")
            
    with tab2:
        try:
            st.json(json.loads(final_state["attack_plan"]))
        except:
            st.code(final_state["attack_plan"], language="json")
            