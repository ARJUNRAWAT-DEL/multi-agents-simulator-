"""
Enterprise AI Agent Consortium - Configuration Settings
Professional-grade configuration management for multi-agent collaboration
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class AgentConfig:
    """Configuration for individual agents"""
    name: str
    enabled: bool = False
    model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.7
    max_tokens: int = 1000

@dataclass
class SimulationConfig:
    """Configuration for simulation parameters"""
    max_rounds: int = 5
    default_rounds: int = 2
    output_formats: List[str] = None
    models: List[str] = None
    
    def __post_init__(self):
        if self.output_formats is None:
            self.output_formats = [
                "Executive Summary",
                "Detailed Analysis", 
                "Technical Specification"
            ]
        
        if self.models is None:
            self.models = [
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant", 
                "mixtral-8x7b-32768"
            ]

@dataclass
class ProjectConfig:
    """Configuration for project categorization"""
    project_types: List[str] = None
    industries: List[str] = None
    
    def __post_init__(self):
        if self.project_types is None:
            self.project_types = [
                "Mobile Application",
                "Web Platform", 
                "Enterprise Software",
                "AI/ML Product",
                "E-commerce Solution",
                "SaaS Platform",
                "IoT Solution",
                "Blockchain/Web3"
            ]
        
        if self.industries is None:
            self.industries = [
                "Technology",
                "Finance", 
                "Healthcare",
                "Education",
                "Retail",
                "Manufacturing",
                "Entertainment",
                "Travel",
                "Real Estate",
                "Other"
            ]

class EnterpriseConfig:
    """Main configuration class for the Enterprise AI Agent Consortium"""
    
    def __init__(self):
        self.agents = {
            "Product Manager": AgentConfig("Product Manager", enabled=True),
            "Business Analyst": AgentConfig("Business Analyst", enabled=True),
            "Software Engineer": AgentConfig("Software Engineer", enabled=True),
            "UX Designer": AgentConfig("UX Designer", enabled=False),
            "Marketing Strategist": AgentConfig("Marketing Strategist", enabled=False),
            "Technical Architect": AgentConfig("Technical Architect", enabled=False)
        }
        
        self.simulation = SimulationConfig()
        self.project = ProjectConfig()
        
        # API Configuration
        self.api_key = os.getenv("GROQ_API_KEY")
        self.api_available = bool(self.api_key)
        
        # UI Configuration
        self.app_title = "🏢 Enterprise AI Agent Consortium"
        self.app_description = "Advanced Multi-Agent Collaboration Platform for Strategic Product Development"
        
        # Professional templates
        self.templates = {
            "💰 Fintech App": (
                "Build a comprehensive fintech mobile application targeting millennials and Gen Z users, "
                "featuring budgeting tools, investment tracking, cryptocurrency integration, and AI-powered financial insights."
            ),
            "🏥 HealthTech Platform": (
                "Develop a telemedicine platform that connects patients with healthcare providers, "
                "includes appointment scheduling, medical records management, prescription tracking, and AI-powered symptom assessment."
            ),
            "🎓 EdTech Solution": (
                "Create an adaptive learning platform for K-12 education with personalized curriculum, "
                "progress tracking, gamification elements, and AI-powered tutoring assistance."
            ),
            "🛒 E-commerce Platform": (
                "Build a next-generation e-commerce marketplace with AR product visualization, "
                "AI-powered recommendations, social commerce features, and sustainable shopping analytics."
            )
        }
    
    def get_enabled_agents(self) -> Dict[str, bool]:
        """Return dictionary of agent enablement status"""
        return {name: config.enabled for name, config in self.agents.items()}
    
    def update_agent_status(self, agent_name: str, enabled: bool):
        """Update agent enablement status"""
        if agent_name in self.agents:
            self.agents[agent_name].enabled = enabled
    
    def get_agent_count(self) -> int:
        """Return number of enabled agents"""
        return sum(1 for config in self.agents.values() if config.enabled)
    
    def validate_configuration(self) -> tuple[bool, List[str]]:
        """Validate current configuration and return status with any error messages"""
        errors = []
        
        if not self.api_available:
            errors.append("GROQ_API_KEY not found in environment variables")
        
        if self.get_agent_count() == 0:
            errors.append("At least one agent must be enabled")
        
        return len(errors) == 0, errors

# Global configuration instance
config = EnterpriseConfig()