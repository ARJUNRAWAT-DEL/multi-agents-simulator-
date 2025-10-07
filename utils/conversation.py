from agents.pm import ProductManager
from agents.analyst import Analyst
from agents.engineer import Engineer
from agents.ux_designer import UXDesigner
from agents.marketing_strategist import MarketingStrategist
from agents.technical_architect import TechnicalArchitect

# Optional agents - import with try/except to handle missing modules gracefully
try:
    from agents.legal_compliance import LegalComplianceAgent
except ImportError:
    LegalComplianceAgent = None

try:
    from agents.financial_analyst import FinancialAnalyst
except ImportError:
    FinancialAnalyst = None

try:
    from agents.security_expert import SecurityExpert
except ImportError:
    SecurityExpert = None

try:
    from agents.operations_director import OperationsDirector
except ImportError:
    OperationsDirector = None
from typing import List, Dict, Tuple

def simulate_conversation(project_idea: str, turns: int = 2, selected_agents: dict = None, 
                         model: str = "llama-3.3-70b-versatile", output_format: str = "Executive Summary") -> Tuple[List[Dict[str, str]], str]:
    """Run an enhanced multi-agent collaboration and return (history, final_report)."""
    
    # Default agent selection if none provided
    if selected_agents is None:
        selected_agents = {
            "Product Manager": True,
            "Business Analyst": True,
            "Software Engineer": True,
            "UX Designer": False,
            "Marketing Strategist": False,
            "Technical Architect": False,
            "Legal Compliance": False,
            "Financial Analyst": False,
            "Security Expert": False,
            "Operations Director": False
        }
    
    ENHANCED_HEADER = (
        f"You are part of an elite enterprise consulting team working on: {project_idea}\n\n"
        f"Active team members: {', '.join([k for k, v in selected_agents.items() if v])}\n"
        f"Output format required: {output_format}\n"
        f"Collaboration depth: {turns} rounds\n\n"
        "Provide professional, actionable insights with specific recommendations, "
        "quantified metrics, and implementation roadmaps. Each agent should leverage "
        "their specialized expertise while maintaining alignment with business objectives."
    )
    
    history: List[dict] = [{"role": "system", "content": ENHANCED_HEADER}]

    # Initialize selected agents
    agents = {}
    if selected_agents.get("Product Manager", False):
        agents["pm"] = ProductManager()
    if selected_agents.get("Business Analyst", False):
        agents["analyst"] = Analyst()
    if selected_agents.get("Software Engineer", False):
        agents["engineer"] = Engineer()
    if selected_agents.get("UX Designer", False):
        agents["ux_designer"] = UXDesigner()
    if selected_agents.get("Marketing Strategist", False):
        agents["marketing"] = MarketingStrategist()
    if selected_agents.get("Technical Architect", False):
        agents["tech_architect"] = TechnicalArchitect()
    if selected_agents.get("Legal Compliance", False) and LegalComplianceAgent:
        agents["legal"] = LegalComplianceAgent()
    if selected_agents.get("Financial Analyst", False) and FinancialAnalyst:
        agents["financial"] = FinancialAnalyst()
    if selected_agents.get("Security Expert", False) and SecurityExpert:
        agents["security"] = SecurityExpert()
    if selected_agents.get("Operations Director", False) and OperationsDirector:
        agents["operations"] = OperationsDirector()

    # Enhanced conversation flow with separate histories
    api_history = [{"role": "user", "content": project_idea}]  # Clean history for API calls
    display_history = [{"role": "user", "content": project_idea}]  # Full history for display
    current_context = project_idea
    
    for round_num in range(turns):
        round_messages = []
        
        # PM initiates or synthesizes (if available)
        if "pm" in agents:
            pm_msg = agents["pm"].handle_message(current_context, api_history)
            api_history.append({"role": "assistant", "content": pm_msg})
            display_history.append({"role": "assistant", "content": pm_msg, "agent_type": "Product Manager"})
            round_messages.append(pm_msg)
            current_context = pm_msg

        # Analyst provides data-driven insights (if available)
        if "analyst" in agents:
            analyst_msg = agents["analyst"].handle_message(current_context, api_history)
            api_history.append({"role": "assistant", "content": analyst_msg})
            display_history.append({"role": "assistant", "content": analyst_msg, "agent_type": "Business Analyst"})
            round_messages.append(analyst_msg)
            current_context = analyst_msg

        # UX Designer adds user experience perspective (if available)
        if "ux_designer" in agents:
            ux_msg = agents["ux_designer"].handle_message(current_context, api_history)
            api_history.append({"role": "assistant", "content": ux_msg})
            display_history.append({"role": "assistant", "content": ux_msg, "agent_type": "UX Designer"})
            round_messages.append(ux_msg)

        # Marketing adds go-to-market strategy (if available)
        if "marketing" in agents:
            marketing_msg = agents["marketing"].handle_message(current_context, api_history)
            api_history.append({"role": "assistant", "content": marketing_msg})
            display_history.append({"role": "assistant", "content": marketing_msg, "agent_type": "Marketing Strategist"})
            round_messages.append(marketing_msg)

        # Technical Architect provides high-level architecture (if available)
        if "tech_architect" in agents:
            arch_msg = agents["tech_architect"].handle_message(current_context, api_history)
            api_history.append({"role": "assistant", "content": arch_msg})
            display_history.append({"role": "assistant", "content": arch_msg, "agent_type": "Technical Architect"})
            round_messages.append(arch_msg)

        # Engineer provides implementation details (if available)
        if "engineer" in agents:
            engineer_msg = agents["engineer"].handle_message(current_context, api_history)
            api_history.append({"role": "assistant", "content": engineer_msg})
            display_history.append({"role": "assistant", "content": engineer_msg, "agent_type": "Software Engineer"})
            round_messages.append(engineer_msg)
            current_context = engineer_msg

        # Industry specialist agents (if available)
        if "legal" in agents:
            legal_msg = agents["legal"].handle_message(current_context, api_history)
            api_history.append({"role": "assistant", "content": legal_msg})
            display_history.append({"role": "assistant", "content": legal_msg, "agent_type": "Legal Compliance"})
            round_messages.append(legal_msg)

        if "financial" in agents:
            financial_msg = agents["financial"].handle_message(current_context, api_history)
            api_history.append({"role": "assistant", "content": financial_msg})
            display_history.append({"role": "assistant", "content": financial_msg, "agent_type": "Financial Analyst"})
            round_messages.append(financial_msg)

        if "security" in agents:
            security_msg = agents["security"].handle_message(current_context, api_history)
            api_history.append({"role": "assistant", "content": security_msg})
            display_history.append({"role": "assistant", "content": security_msg, "agent_type": "Security Expert"})
            round_messages.append(security_msg)

        if "operations" in agents:
            ops_msg = agents["operations"].handle_message(current_context, api_history)
            api_history.append({"role": "assistant", "content": ops_msg})
            display_history.append({"role": "assistant", "content": ops_msg, "agent_type": "Operations Director"})
            round_messages.append(ops_msg)

        # Update context with round synthesis
        if round_messages:
            current_context = f"Round {round_num + 1} synthesis: " + " | ".join(round_messages[:2])

    # Generate enhanced final report based on output format
    report_prompts = {
        "Executive Summary": (
            "Create a comprehensive executive summary including:\n"
            "• Strategic Overview & Value Proposition\n"
            "• Market Opportunity & Target Segments\n"
            "• Key Success Metrics & KPIs\n"
            "• Implementation Timeline & Milestones\n"
            "• Resource Requirements & Budget Estimates\n"
            "• Risk Assessment & Mitigation Strategies\n"
            "• Competitive Positioning\n"
            "• ROI Projections & Success Criteria\n\n"
            "Format as a professional business document with clear sections and actionable recommendations."
        ),
        "Detailed Analysis": (
            "Provide an in-depth analysis covering:\n"
            "• Comprehensive market research and competitive landscape\n"
            "• Detailed technical architecture and implementation plan\n"
            "• User experience strategy and design recommendations\n"
            "• Go-to-market strategy and marketing plan\n"
            "• Financial projections and business model analysis\n"
            "• Risk assessment and contingency planning\n"
            "• Success metrics and measurement framework\n\n"
            "Include supporting data, methodologies, and detailed recommendations."
        ),
        "Technical Specification": (
            "Generate a technical specification document including:\n"
            "• System architecture and technical requirements\n"
            "• Technology stack recommendations with justifications\n"
            "• API specifications and integration requirements\n"
            "• Security and compliance considerations\n"
            "• Performance and scalability requirements\n"
            "• Development timeline and resource allocation\n"
            "• Testing strategy and quality assurance plan\n"
            "• Deployment and operational considerations\n\n"
            "Focus on technical implementation details and engineering best practices."
        )
    }
    
    final_prompt = report_prompts.get(output_format, report_prompts["Executive Summary"])
    
    # Use PM for final synthesis if available, otherwise use first available agent
    synthesizer = agents.get("pm") or next(iter(agents.values()))
    final_report = synthesizer.handle_message(final_prompt, api_history)

    return display_history, final_report


# Legacy header for backward compatibility
HEADER = (
    "You are a team of professional agents collaborating on strategic product development. "
    "Each agent brings specialized expertise to create comprehensive, actionable business solutions. "
    "Maintain professional standards and provide quantified, implementable recommendations."
)