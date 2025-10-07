import streamlit as st
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from utils.conversation import simulate_conversation
from utils.graphs import build_insight_plot

# ---------- Setup ----------
load_dotenv()
API_OK = bool(os.getenv("GROQ_API_KEY"))

st.set_page_config(
    page_title="🏢 Enterprise AI Agent Consortium", 
    page_icon="🏢", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        text-align: center;
        margin: 0;
        font-weight: 600;
    }
    .main-header p {
        color: #e2e8f0;
        text-align: center;
        margin-top: 0.5rem;
        font-size: 1.1rem;
    }
    .agent-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3b82f6;
        margin: 0.5rem 0;
    }
    .metric-card {
        background: #f0f9ff;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        border: 1px solid #0ea5e9;
    }
    .stButton > button {
        background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🏢 Enterprise AI Agent Consortium</h1>
    <p>Advanced Multi-Agent Collaboration Platform for Strategic Product Development</p>
</div>
""", unsafe_allow_html=True)

if not API_OK:
    st.error("🔑 GROQ_API_KEY not found in environment. Create a .env with GROQ_API_KEY=... and restart.")

# ---------- Sidebar Configuration ----------
with st.sidebar:
    st.header("🎛️ Configuration Panel")
    
    # Agent Selection
    st.subheader("👥 Agent Team Selection")
    
    # Core agents
    st.markdown("**Core Team**")
    agent_config = {
        "Product Manager": st.checkbox("Product Manager", value=True),
        "Business Analyst": st.checkbox("Business Analyst", value=True),
        "Software Engineer": st.checkbox("Software Engineer", value=True),
    }
    
    # Specialized agents
    st.markdown("**Specialized Experts**")
    agent_config.update({
        "UX Designer": st.checkbox("UX Designer", value=False),
        "Marketing Strategist": st.checkbox("Marketing Strategist", value=False),
        "Technical Architect": st.checkbox("Technical Architect", value=False),
    })
    
    # Industry-specific agents
    st.markdown("**Industry Specialists**")
    agent_config.update({
        "Legal Compliance": st.checkbox("Legal & Compliance", value=False),
        "Financial Analyst": st.checkbox("Financial Analyst", value=False),
        "Security Expert": st.checkbox("Security Expert", value=False),
        "Operations Director": st.checkbox("Operations Director", value=False),
    })
    
    # Simulation Settings
    st.subheader("⚙️ Simulation Settings")
    turns = st.slider("Collaboration Rounds", min_value=1, max_value=5, value=2,
                      help="Number of complete PM→Analyst→Engineer cycles")
    
    model_option = st.selectbox(
        "AI Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
        index=0,
        help="Select the AI model for agent responses"
    )
    
    output_format = st.selectbox(
        "Report Format",
        ["Executive Summary", "Detailed Analysis", "Technical Specification"],
        index=0
    )
    
    # Professional metrics
    st.subheader("📊 Session Metrics")
    if "conversation" in st.session_state and st.session_state.conversation:
        st.metric("Messages Generated", len(st.session_state.conversation))
        st.metric("Active Agents", sum(agent_config.values()))
        if "report" in st.session_state and st.session_state.report:
            st.metric("Report Length", f"{len(st.session_state.report.split())} words")

# ---------- User Input ----------
with st.container():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("🚀 Project Initiative")
        project = st.text_area(
            "Describe your product or business initiative:",
            placeholder="e.g., Develop an AI-powered fintech application for Gen Z users that provides personalized budgeting, investment recommendations, and financial literacy content through a gamified mobile experience.",
            height=100,
            help="Provide a detailed description of your project idea, target market, and key objectives."
        )
        
        # Project type selection
        project_type = st.selectbox(
            "Project Category",
            ["Mobile Application", "Web Platform", "Enterprise Software", "AI/ML Product", 
             "E-commerce Solution", "SaaS Platform", "IoT Solution", "Blockchain/Web3"],
            help="Select the primary category that best describes your project"
        )
        
        # Industry selection
        industry = st.selectbox(
            "Target Industry",
            ["Technology", "Finance", "Healthcare", "Education", "Retail", "Manufacturing", 
             "Entertainment", "Travel", "Real Estate", "Other"],
            help="Primary industry vertical for your product"
        )
    
    with col2:
        st.subheader("🎯 Quick Start Templates")
        if st.button("💰 Fintech App", use_container_width=True):
            project = "Build a comprehensive fintech mobile application targeting millennials and Gen Z users, featuring budgeting tools, investment tracking, cryptocurrency integration, and AI-powered financial insights."
        
        if st.button("🏥 HealthTech Platform", use_container_width=True):
            project = "Develop a telemedicine platform that connects patients with healthcare providers, includes appointment scheduling, medical records management, prescription tracking, and AI-powered symptom assessment."
        
        if st.button("🎓 EdTech Solution", use_container_width=True):
            project = "Create an adaptive learning platform for K-12 education with personalized curriculum, progress tracking, gamification elements, and AI-powered tutoring assistance."
        
        if st.button("🛒 E-commerce Platform", use_container_width=True):
            project = "Build a next-generation e-commerce marketplace with AR product visualization, AI-powered recommendations, social commerce features, and sustainable shopping analytics."

    st.markdown("---")
    
    # Enhanced run button with progress
    col_run1, col_run2, col_run3 = st.columns([1, 2, 1])
    with col_run2:
        run_btn = st.button(
            "🚀 Initiate Agent Collaboration", 
            type="primary", 
            use_container_width=True,
            help="Start the multi-agent analysis and planning process"
        )

if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "report" not in st.session_state:
    st.session_state.report = None

# ---------- Run ----------
if run_btn and project.strip():
    with st.spinner("Agents collaborating…"):
        convo, report = simulate_conversation(project.strip(), turns=turns)
        st.session_state.conversation = convo
        st.session_state.report = report

# ---------- Results ----------
left, right = st.columns([2, 1])

with left:
    st.subheader("📄 Final Consolidated Report")
    if st.session_state.report:
        st.markdown(st.session_state.report)
    else:
        st.info("Enter a project idea and click Run Simulation.")

    st.subheader("📊 Insight Plot")
    fig = build_insight_plot(st.session_state.conversation, st.session_state.report)
    if fig:
        st.pyplot(fig, use_container_width=True)
    else:
        st.info("No plot available yet — try a more data‑driven project prompt.")

with right:
    st.subheader("🗂️ Options")
    show_convo = st.toggle("Show agent conversation", value=False)
    st.caption("Conversation is hidden by default.")

    if show_convo:
        st.divider()
        st.subheader("🧵 Agent Conversation (raw)")
        if st.session_state.conversation:
            for m in st.session_state.conversation:
                role = m.get("role", "unknown").title()
                content = m.get("content", "")
                st.markdown(f"**{role}:**\n\n{content}")
        else:
            st.info("No conversation yet.")

st.divider()
st.caption("Tip: Increase ‘Agent rounds’ for deeper analysis.")