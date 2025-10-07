"""
Enterprise AI Agent Consortium - Main Application
Advanced Multi-Agent Collaboration Platform for Strategic Product Development
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import system integrator first
try:
    from integration.system_integrator import integrator
    system_ready = True
except ImportError:
    system_ready = False
    st.error("System integration module not found. Please check installation.")

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

def initialize_streamlit_config():
    """Initialize Streamlit configuration"""
    st.set_page_config(
        page_title="🏢 Enterprise AI Agent Consortium", 
        page_icon="🏢", 
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/your-repo/help',
            'Report a bug': 'https://github.com/your-repo/issues',
            'About': "Enterprise AI Agent Consortium v2.0 - Advanced Multi-Agent Collaboration Platform"
        }
    )

def render_system_status(health_status):
    """Render system status indicator"""
    status = health_status.get("status", "unknown")
    
    # Import here to avoid circular imports
    try:
        from utils.rate_limiter import groq_manager
        usage_stats = groq_manager.get_usage_dashboard()
    except ImportError:
        usage_stats = None
    
    # Check multi-model manager status
    try:
        from utils.multi_model_manager import multi_model_manager
        provider_status = multi_model_manager.get_provider_status()
    except ImportError:
        provider_status = None
    
    if status == "healthy":
        st.success("🟢 System Status: All systems operational")
    elif status == "degraded":
        st.warning("🟡 System Status: Some features may be limited")
        if health_status.get("missing_modules"):
            st.warning(f"Missing modules: {', '.join(health_status['missing_modules'])}")
    else:
        st.error("🔴 System Status: Critical issues detected")
        if "error" in health_status:
            st.error(f"Error: {health_status['error']}")
    
    # Display AI Model Providers Status
    if provider_status:
        with st.expander("🤖 AI Model Providers", expanded=True):
            active_providers = [p for p, info in provider_status.items() if info['active']]
            inactive_providers = [p for p, info in provider_status.items() if not info['active']]
            
            if active_providers:
                # Check if Ollama is active and show special success message
                ollama_active = any('ollama' in p for p in active_providers)
                if ollama_active:
                    st.success(f"🎉 Active Providers: {len(active_providers)} - **Unlimited Free AI Ready!**")
                else:
                    st.success(f"✅ Active Providers: {len(active_providers)}")
                
                cols = st.columns(min(len(active_providers), 3))
                for i, provider_id in enumerate(active_providers):
                    info = provider_status[provider_id]
                    with cols[i % 3]:
                        # Special styling for Ollama
                        if 'ollama' in provider_id:
                            st.metric(
                                info['name'],
                                "🚀 Unlimited",
                                f"🎯 {len(info['models'])} models"
                            )
                        else:
                            st.metric(
                                info['name'],
                                "Ready",
                                f"{len(info['models'])} models"
                            )
            
            if inactive_providers:
                # Check if Ollama is active - if so, show this as optional backup providers
                if any('ollama' in p for p in active_providers):
                    st.info(f"💡 Optional backup providers available: {len(inactive_providers)} (Ollama provides unlimited free usage)")
                    
                    # Show providers in a collapsible section without nested expander
                    show_backup = st.checkbox("🔧 Show backup provider details", key="backup_providers")
                    if show_backup:
                        st.markdown("**These are backup providers - not needed since Ollama is working:**")
                        for provider_id in inactive_providers:
                            info = provider_status[provider_id]
                            st.write(f"• {info['name']} - {len(info['models'])} models")
                        if st.button("🚀 Setup Backup Providers"):
                            st.info("Run: `python setup_free_models.py` in terminal for API keys setup")
                else:
                    st.warning(f"⚠️ Available but not configured: {len(inactive_providers)}")
                    if st.button("🚀 Setup Free Models"):
                        st.info("Run: `python setup_free_models.py` in terminal for setup instructions")
    
    # Display API Usage Statistics (Groq fallback)
    if usage_stats:
        with st.expander("📊 Groq API Usage (Fallback)", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Tokens Used Today",
                    f"{usage_stats['tokens_used_today']:,}",
                    f"{usage_stats['daily_limit'] - usage_stats['tokens_used_today']:,} remaining"
                )
            
            with col2:
                usage_pct = usage_stats['usage_percentage']
                color = "🟢" if usage_pct < 70 else "🟡" if usage_pct < 90 else "🔴"
                st.metric(
                    "Daily Usage",
                    f"{usage_pct:.1f}%",
                    f"{color} of {usage_stats['daily_limit']:,} limit"
                )
            
            with col3:
                can_request = "✅ Ready" if usage_stats['can_make_request'] else "⚠️ Limited"
                st.metric(
                    "API Status",
                    can_request,
                    f"Recent requests: {usage_stats['requests_last_minute']}"
                )
            
            # Progress bar for visual representation
            progress_value = min(usage_stats['usage_percentage'] / 100, 1.0)
            st.progress(progress_value)
            
            if usage_stats['usage_percentage'] > 80:
                st.warning("⚠️ High Groq usage. System now using free unlimited models as primary.")

def render_professional_header():
    """Render professional header with theming"""
    # Enhanced CSS with professional styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #0ea5e9 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        position: relative;
        overflow: hidden;
        text-align: center;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='10' cy='10' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        opacity: 0.3;
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-weight: 700;
        font-size: 3rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
        letter-spacing: -1px;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.95);
        margin-top: 1rem;
        font-size: 1.3rem;
        font-weight: 300;
        position: relative;
        z-index: 2;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .professional-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .professional-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(59, 130, 246, 0.4);
    }
    
    .metric-display {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #0ea5e9;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    @media (max-width: 768px) {
        .main-header h1 { font-size: 2rem; }
        .main-header p { font-size: 1.1rem; }
        .professional-card { padding: 1.5rem; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-header">
        <h1>🏢 Enterprise AI Agent Consortium</h1>
        <p>Advanced Multi-Agent Collaboration Platform for Strategic Product Development</p>
    </div>
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    # Initialize Streamlit
    initialize_streamlit_config()
    
    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    if "report" not in st.session_state:
        st.session_state.report = None
    if "system_initialized" not in st.session_state:
        st.session_state.system_initialized = False
    
    # Initialize system if not already done
    if not st.session_state.system_initialized and system_ready:
        with st.spinner("🔄 Initializing Enterprise AI Agent Consortium..."):
            system_config = integrator.initialize_system()
            st.session_state.system_config = system_config
            st.session_state.system_initialized = True
    
    # Render header
    render_professional_header()
    
    # Check system health and render status
    if system_ready and st.session_state.system_initialized:
        health_status = st.session_state.system_config.get("health", {})
        render_system_status(health_status)
        
        # Get available agents
        agent_config = st.session_state.system_config.get("agent_config", {})
        conversation_func = st.session_state.system_config.get("conversation_function")
        graph_func = st.session_state.system_config.get("graph_function")
    else:
        st.error("❌ System initialization failed. Running in fallback mode.")
        agent_config = {
            "Product Manager": True,
            "Business Analyst": True,
            "Software Engineer": True,
            "UX Designer": False,
            "Marketing Strategist": False,
            "Technical Architect": False
        }
        conversation_func = None
        graph_func = None
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("🎛️ Configuration Panel")
        
        # Agent Selection
        st.subheader("👥 Agent Team Selection")
        selected_agents = {}
        
        # Core agents (always show)
        st.markdown("**Core Team:**")
        for agent_name in ["Product Manager", "Business Analyst", "Software Engineer"]:
            available = agent_config.get(agent_name, False)
            default_value = available
            if available:
                selected_agents[agent_name] = st.checkbox(
                    f"✅ {agent_name}", 
                    value=default_value,
                    help=f"{agent_name} is available and ready"
                )
            else:
                selected_agents[agent_name] = st.checkbox(
                    f"⚠️ {agent_name} (Limited)", 
                    value=False,
                    help=f"{agent_name} is running in fallback mode"
                )
        
        # Extended team
        st.markdown("**Extended Team:**")
        for agent_name in ["UX Designer", "Marketing Strategist", "Technical Architect"]:
            available = agent_config.get(agent_name, False)
            if available:
                selected_agents[agent_name] = st.checkbox(
                    f"✅ {agent_name}", 
                    value=False,
                    help=f"{agent_name} is available"
                )
            else:
                selected_agents[agent_name] = st.checkbox(
                    f"⚠️ {agent_name} (Limited)", 
                    value=False,
                    help=f"{agent_name} is running in fallback mode"
                )
        
        # Specialized consultants
        if any(agent_config.get(name, False) for name in ["Legal Consultant", "Compliance Officer", "Financial Analyst", "Security Specialist"]):
            st.markdown("**Specialized Consultants:**")
            for agent_name in ["Legal Consultant", "Compliance Officer", "Financial Analyst", "Security Specialist"]:
                available = agent_config.get(agent_name, False)
                if available:
                    selected_agents[agent_name] = st.checkbox(
                        f"✅ {agent_name}", 
                        value=False,
                        help=f"{agent_name} is available"
                    )
        
        st.divider()
        
        # Simulation Settings
        st.subheader("⚙️ Simulation Settings")
        turns = st.slider("Collaboration Rounds", min_value=3, max_value=15, value=10,
                          help="Number of complete discussion cycles (Recommended: 8-10 for comprehensive analysis)")
        
        model_option = st.selectbox(
            "AI Model",
            ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
            index=0,
            help="Select the AI model for agent responses"
        )
        
        output_format = st.selectbox(
            "Report Format",
            ["Executive Summary", "Detailed Analysis", "Technical Specification"],
            index=0,
            help="Choose the format for the final report"
        )
        
        st.divider()
        
        # Session Metrics
        st.subheader("📊 Session Metrics")
        col1, col2 = st.columns(2)
        
        with col1:
            active_agents = sum(selected_agents.values())
            st.markdown(f"""
            <div class="metric-display">
                <div style="font-size: 1.5rem; font-weight: bold; color: #0ea5e9;">{active_agents}</div>
                <div style="font-size: 0.9rem; color: #64748b;">Active Agents</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if st.session_state.conversation:
                message_count = len(st.session_state.conversation)
            else:
                message_count = 0
            st.markdown(f"""
            <div class="metric-display">
                <div style="font-size: 1.5rem; font-weight: bold; color: #10b981;">{message_count}</div>
                <div style="font-size: 0.9rem; color: #64748b;">Messages</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Main Content Area
    st.markdown("## 🚀 Project Initiative")
    
    # Project input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        project = st.text_area(
            "Describe your product or business initiative:",
            placeholder="e.g., Develop an AI-powered fintech application for Gen Z users that provides personalized budgeting, investment recommendations, and financial literacy content through a gamified mobile experience.",
            height=120,
            help="Provide a detailed description of your project idea, target market, and key objectives."
        )
        
        # Project categorization
        col_type, col_industry = st.columns(2)
        
        with col_type:
            project_type = st.selectbox(
                "Project Category",
                ["Mobile Application", "Web Platform", "Enterprise Software", "AI/ML Product", 
                 "E-commerce Solution", "SaaS Platform", "IoT Solution", "Blockchain/Web3"],
                help="Select the primary category that best describes your project"
            )
        
        with col_industry:
            industry = st.selectbox(
                "Target Industry",
                ["Technology", "Finance", "Healthcare", "Education", "Retail", "Manufacturing", 
                 "Entertainment", "Travel", "Real Estate", "Other"],
                help="Primary industry vertical for your product"
            )
    
    with col2:
        st.subheader("🎯 Quick Templates")
        
        templates = {
            "💰 Fintech App": "Build a comprehensive fintech mobile application targeting millennials and Gen Z users, featuring budgeting tools, investment tracking, cryptocurrency integration, and AI-powered financial insights.",
            "🏥 HealthTech Platform": "Develop a telemedicine platform that connects patients with healthcare providers, includes appointment scheduling, medical records management, prescription tracking, and AI-powered symptom assessment.",
            "🎓 EdTech Solution": "Create an adaptive learning platform for K-12 education with personalized curriculum, progress tracking, gamification elements, and AI-powered tutoring assistance.",
            "🛒 E-commerce Platform": "Build a next-generation e-commerce marketplace with AR product visualization, AI-powered recommendations, social commerce features, and sustainable shopping analytics."
        }
        
        for template_name, template_text in templates.items():
            if st.button(template_name, use_container_width=True):
                st.session_state.template_selected = template_text
                st.rerun()
        
        # Apply selected template
        if hasattr(st.session_state, 'template_selected'):
            project = st.session_state.template_selected
            delattr(st.session_state, 'template_selected')
    
    st.markdown("---")
    
    # Enhanced run button
    col_run1, col_run2, col_run3 = st.columns([1, 2, 1])
    with col_run2:
        run_btn = st.button(
            "🚀 Initiate Agent Collaboration", 
            type="primary", 
            use_container_width=True,
            help="Start the multi-agent analysis and planning process"
        )
    
    # Run simulation
    if run_btn and project.strip():
        if not any(selected_agents.values()):
            st.error("⚠️ Please select at least one agent from the sidebar configuration.")
        elif not conversation_func:
            st.error("❌ Conversation system not available. Please check system configuration.")
        else:
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            with st.spinner("🤖 Agents are collaborating on your project..."):
                try:
                    status_text.text("🔄 Initializing agent collaboration...")
                    progress_bar.progress(20)
                    
                    # Enhanced context for agents
                    enhanced_context = f"""
                    Project: {project}
                    Category: {project_type}
                    Industry: {industry}
                    Output Format: {output_format}
                    Selected Agents: {', '.join([k for k, v in selected_agents.items() if v])}
                    Analysis Depth: {turns} rounds
                    """
                    
                    status_text.text("🚀 Agents analyzing requirements... (⏱️ ~15 seconds)")
                    progress_bar.progress(60)
                    
                    # Add a countdown timer visual
                    import time
                    start_time = time.time()
                    
                    # Run conversation
                    convo, report = conversation_func(
                        enhanced_context, 
                        turns=turns, 
                        selected_agents=selected_agents,
                        model=model_option,
                        output_format=output_format
                    )
                    
                    elapsed_time = time.time() - start_time
                    progress_bar.progress(100)
                    status_text.text(f"✅ Analysis complete in {elapsed_time:.1f}s!")
                    
                    st.session_state.conversation = convo
                    st.session_state.report = report
                    st.session_state.project_info = {
                        "project": project,
                        "type": project_type,
                        "industry": industry,
                        "agents": selected_agents,
                        "turns": turns,
                        "model": model_option,
                        "format": output_format
                    }
                    
                    # Clear progress indicators after success
                    progress_bar.empty()
                    status_text.empty()
                    
                except Exception as e:
                    st.error(f"❌ Error during agent collaboration: {str(e)}")
                    progress_bar.empty()
                    status_text.empty()
    
    # Results Section
    if st.session_state.get("report"):
        st.markdown("---")
        st.markdown("## 📋 Analysis Results")
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Executive Summary", "🔍 Detailed Analysis", "📈 Insights & Metrics", "💾 Export Options"])
        
        with tab1:
            st.markdown("### 🎯 Strategic Overview")
            
            # Project info display
            if st.session_state.get("project_info"):
                info = st.session_state.project_info
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-display">
                        <div style="font-weight: bold; color: #3b82f6;">Project Type</div>
                        <div>{info['type']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-display">
                        <div style="font-weight: bold; color: #3b82f6;">Industry</div>
                        <div>{info['industry']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    active_count = sum(info['agents'].values())
                    st.markdown(f"""
                    <div class="metric-display">
                        <div style="font-weight: bold; color: #3b82f6;">Active Agents</div>
                        <div>{active_count}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown(f"""
                    <div class="metric-display">
                        <div style="font-weight: bold; color: #3b82f6;">Analysis Depth</div>
                        <div>{info['turns']} rounds</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown("### 📄 Executive Report")
            st.markdown(st.session_state.report)
        
        with tab2:
            st.markdown("### 🗣️ Agent Conversation Timeline")
            
            if st.session_state.conversation:
                for i, msg in enumerate(st.session_state.conversation, 1):
                    role = msg.get("role", "Unknown").title()
                    content = msg.get("content", "")
                    agent_type = msg.get("agent_type", "System")
                    
                    # Color coding by agent type
                    colors = {
                        "Product Manager": "#3b82f6",
                        "Business Analyst": "#10b981", 
                        "Software Engineer": "#f59e0b",
                        "UX Designer": "#ec4899",
                        "Marketing Strategist": "#8b5cf6",
                        "Technical Architect": "#ef4444",
                        "System": "#6b7280"
                    }
                    
                    color = colors.get(agent_type, "#6b7280")
                    
                    with st.expander(f"💬 {i}. {agent_type} - {role}", expanded=False):
                        st.markdown(f"""
                        <div style="border-left: 4px solid {color}; padding-left: 1rem; margin: 1rem 0;">
                            {content}
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.info("No detailed conversation available.")
        
        with tab3:
            st.markdown("### 📊 Analysis Insights")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("📈 Project Visualization")
                if graph_func:
                    try:
                        fig = graph_func(st.session_state.conversation, st.session_state.report)
                        if fig:
                            st.pyplot(fig, use_container_width=True)
                        else:
                            st.info("💡 Visualization will appear for data-rich project descriptions.")
                    except Exception as e:
                        st.warning(f"Visualization unavailable: {str(e)}")
                else:
                    st.info("📊 Graph functionality not available in current mode.")
            
            with col2:
                st.subheader("🎯 Key Metrics")
                
                # Calculate metrics
                conversation_length = len(st.session_state.conversation) if st.session_state.conversation else 0
                report_words = len(st.session_state.report.split()) if st.session_state.report else 0
                
                metrics = [
                    ("Messages", conversation_length, "💬"),
                    ("Report Words", report_words, "📝"),
                    ("Analysis Rounds", st.session_state.project_info.get('turns', 0) if st.session_state.get('project_info') else 0, "🔄"),
                    ("Confidence", "85%", "🎯")
                ]
                
                for metric_name, metric_value, icon in metrics:
                    st.markdown(f"""
                    <div class="metric-display">
                        <div style="font-size: 1.5rem;">{icon}</div>
                        <div style="font-weight: bold; margin: 0.5rem 0;">{metric_name}</div>
                        <div style="font-size: 1.2rem; color: #3b82f6;">{metric_value}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with tab4:
            st.markdown("### 💾 Export & Integration Options")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("#### 📄 Document Export")
                if st.button("📄 Download PDF Report", use_container_width=True):
                    st.info("🚧 PDF export functionality will be available in the next update!")
                
                if st.button("📊 Export to Excel", use_container_width=True):
                    st.info("🚧 Excel export functionality will be available in the next update!")
            
            with col2:
                st.markdown("#### 🔗 Share & Collaborate")
                if st.button("🔗 Generate Share Link", use_container_width=True):
                    st.info("🚧 Share link generation will be available in the next update!")
                
                if st.button("📧 Email Report", use_container_width=True):
                    st.info("🚧 Email functionality will be available in the next update!")
            
            with col3:
                st.markdown("#### ⚙️ Integration")
                if st.button("📋 Export to Jira", use_container_width=True):
                    st.info("🚧 Jira integration will be available in the next update!")
                
                if st.button("📁 Save to SharePoint", use_container_width=True):
                    st.info("🚧 SharePoint integration will be available in the next update!")
            
            st.markdown("---")
            
            # Raw data download (currently available)
            st.markdown("#### 📦 Raw Data Export")
            
            if st.session_state.conversation and st.session_state.report:
                import json
                from datetime import datetime
                
                export_data = {
                    "timestamp": datetime.now().isoformat(),
                    "project_info": st.session_state.get("project_info", {}),
                    "report": st.session_state.report,
                    "conversation": st.session_state.conversation,
                    "metadata": {
                        "version": "2.0",
                        "export_format": "json"
                    }
                }
                
                st.download_button(
                    label="💾 Download Complete Analysis (JSON)",
                    data=json.dumps(export_data, indent=2),
                    file_name=f"enterprise_analysis_{project_type.lower().replace(' ', '_')}.json",
                    mime="application/json",
                    use_container_width=True
                )
    
    else:
        # Welcome screen
        st.markdown("---")
        st.markdown("## 🚀 Welcome to Enterprise AI Agent Consortium")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="professional-card">
                <h3>🎯 Strategic Planning</h3>
                <p>Our AI agents collaborate to provide comprehensive strategic analysis, market research, and implementation roadmaps for your business initiatives.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="professional-card">
                <h3>🤖 Multi-Agent Intelligence</h3>
                <p>Choose from specialized agents including Product Managers, Analysts, Engineers, Designers, and Industry Experts to build your perfect team.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="professional-card">
                <h3>📊 Professional Reports</h3>
                <p>Receive executive-ready reports with detailed analysis, visualizations, and actionable recommendations tailored to your industry and objectives.</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.info("👆 **Get Started:** Configure your agent team in the sidebar, enter your project details above, and click 'Initiate Agent Collaboration' to begin the analysis.")

if __name__ == "__main__":
    main()