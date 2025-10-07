"""
Integration Module for Enterprise AI Agent Consortium
Handles all system integrations, fixes import issues, and ensures compatibility
"""

import os
import sys
import importlib
import traceback
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SystemIntegrator:
    """Manages system integration and compatibility"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.agents_path = self.base_path / "agents"
        self.utils_path = self.base_path / "utils"
        self.database_path = self.base_path / "database"
        self.ui_path = self.base_path / "ui"
        
        # Ensure all paths exist
        self._create_directories()
        
        # Track loaded modules
        self.loaded_modules = {}
        self.available_agents = {}
        
    def _create_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            self.agents_path,
            self.utils_path,
            self.database_path,
            self.ui_path,
            self.base_path / "reports",
            self.base_path / "static",
            self.base_path / "config"
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            
            # Create __init__.py files for Python packages
            init_file = directory / "__init__.py"
            if not init_file.exists():
                init_file.write_text("# Auto-generated __init__.py\n")
    
    def safe_import(self, module_name: str, class_name: str = None) -> Optional[Any]:
        """Safely import modules with error handling"""
        try:
            if module_name in self.loaded_modules:
                return self.loaded_modules[module_name]
            
            module = importlib.import_module(module_name)
            
            if class_name:
                if hasattr(module, class_name):
                    cls = getattr(module, class_name)
                    self.loaded_modules[f"{module_name}.{class_name}"] = cls
                    return cls
                else:
                    logger.warning(f"Class {class_name} not found in module {module_name}")
                    return None
            else:
                self.loaded_modules[module_name] = module
                return module
                
        except ImportError as e:
            logger.error(f"Failed to import {module_name}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error importing {module_name}: {e}")
            return None
    
    def load_core_agents(self) -> Dict[str, Any]:
        """Load core agents with fallback handling"""
        core_agents = {}
        
        # Core agents mapping
        agent_configs = {
            "ProductManager": ("agents.pm", "ProductManager"),
            "Analyst": ("agents.analyst", "Analyst"),
            "Engineer": ("agents.engineer", "Engineer"),
            "UXDesigner": ("agents.ux_designer", "UXDesigner"),
            "MarketingStrategist": ("agents.marketing_strategist", "MarketingStrategist"),
            "TechnicalArchitect": ("agents.technical_architect", "TechnicalArchitect"),
            "DataScientist": ("agents.data_scientist", "DataScientist"),
            "OperationsDirector": ("agents.operations_director", "OperationsDirector")
        }
        
        for agent_key, (module_name, class_name) in agent_configs.items():
            agent_class = self.safe_import(module_name, class_name)
            if agent_class:
                core_agents[agent_key] = agent_class
                logger.info(f"Loaded agent: {agent_key}")
            else:
                logger.warning(f"Failed to load agent: {agent_key}")
                # Create a fallback dummy agent
                core_agents[agent_key] = self._create_fallback_agent(agent_key)
        
        self.available_agents.update(core_agents)
        return core_agents
    
    def load_specialized_agents(self) -> Dict[str, Any]:
        """Load specialized industry agents with fallback handling"""
        specialized_agents = {}
        
        # Specialized agents mapping - corrected module and class names
        agent_configs = {
            "LegalAgent": ("agents.legal_compliance", "LegalComplianceAgent"),
            "ComplianceAgent": ("agents.legal_compliance", "LegalComplianceAgent"),
            "FinanceAgent": ("agents.financial_analyst", "FinancialAnalyst"),
            "SecurityAgent": ("agents.security_expert", "SecurityExpert")
        }
        
        for agent_key, (module_name, class_name) in agent_configs.items():
            agent_class = self.safe_import(module_name, class_name)
            if agent_class:
                specialized_agents[agent_key] = agent_class
                logger.info(f"Loaded specialized agent: {agent_key}")
            else:
                logger.warning(f"Failed to load specialized agent: {agent_key}")
                # Create a fallback dummy agent
                specialized_agents[agent_key] = self._create_fallback_agent(agent_key)
        
        self.available_agents.update(specialized_agents)
        return specialized_agents
    
    def _create_fallback_agent(self, agent_name: str):
        """Create a fallback agent class when import fails"""
        class FallbackAgent:
            def __init__(self):
                self.name = agent_name
                self.available = False
                
            def handle_message(self, message: str, history: list = None) -> str:
                return f"[{self.name} temporarily unavailable - Please check system configuration]"
        
        return FallbackAgent
    
    def load_utils(self) -> Dict[str, Any]:
        """Load utility modules with error handling"""
        utils = {}
        
        # Core utilities
        util_modules = [
            "utils.conversation",
            "utils.graphs",
            "database.db_manager",
            "analytics.ai_analytics",
            "reports.pdf_generator",
            "ui.advanced_ui"
        ]
        
        for module_name in util_modules:
            module = self.safe_import(module_name)
            if module:
                utils[module_name.split('.')[-1]] = module
                logger.info(f"Loaded utility: {module_name}")
            else:
                logger.warning(f"Failed to load utility: {module_name}")
        
        return utils
    
    def get_safe_conversation_function(self):
        """Get conversation function with fallback"""
        conversation_module = self.safe_import("utils.conversation")
        
        if conversation_module and hasattr(conversation_module, "simulate_conversation"):
            return conversation_module.simulate_conversation
        else:
            # Fallback conversation function
            def fallback_conversation(project_idea: str, turns: int = 2, **kwargs) -> Tuple[List[Dict], str]:
                """Fallback conversation when main module fails"""
                history = [
                    {"role": "system", "content": "System initializing..."},
                    {"role": "assistant", "content": f"Project Analysis: {project_idea}", "agent_type": "System"}
                ]
                
                report = f"""
                # Project Analysis Report
                
                **Project:** {project_idea}
                
                ## Executive Summary
                This is a fallback analysis while the system is being configured.
                
                ## Recommendations
                - Please ensure all agent modules are properly installed
                - Check system configuration and API keys
                - Restart the application for full functionality
                
                ## Next Steps
                1. Verify system requirements
                2. Install missing dependencies
                3. Configure environment variables
                """
                
                return history, report
            
            return fallback_conversation
    
    def get_safe_graph_function(self):
        """Get graph function with fallback"""
        graphs_module = self.safe_import("utils.graphs")
        
        if graphs_module and hasattr(graphs_module, "build_insight_plot"):
            return graphs_module.build_insight_plot
        else:
            # Fallback graph function
            def fallback_graph(conversation_history: List, report: str):
                """Fallback graph when main module fails"""
                try:
                    import matplotlib.pyplot as plt
                    import pandas as pd
                    
                    # Create a simple placeholder chart
                    fig, ax = plt.subplots(figsize=(8, 6))
                    
                    # Sample data
                    categories = ['Planning', 'Analysis', 'Development', 'Testing']
                    values = [25, 30, 35, 10]
                    
                    ax.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
                    ax.set_title('Project Phase Distribution (Sample Data)')
                    
                    return fig
                except ImportError:
                    return None
            
            return fallback_graph
    
    def check_system_health(self) -> Dict[str, Any]:
        """Check system health and return status"""
        health_status = {
            "status": "healthy",
            "agents_loaded": len(self.available_agents),
            "core_agents": [],
            "specialized_agents": [],
            "missing_modules": [],
            "api_status": "unknown",
            "database_status": "unknown"
        }
        
        # Check API availability
        groq_api_key = os.getenv("GROQ_API_KEY")
        health_status["api_status"] = "available" if groq_api_key else "missing"
        
        # Check agents
        core_agent_names = ["ProductManager", "Analyst", "Engineer"]
        specialized_agent_names = ["LegalAgent", "ComplianceAgent", "FinanceAgent", "SecurityAgent"]
        
        for agent_name in core_agent_names:
            if agent_name in self.available_agents:
                agent_instance = self.available_agents[agent_name]()
                if hasattr(agent_instance, 'available') and not agent_instance.available:
                    health_status["missing_modules"].append(agent_name)
                else:
                    health_status["core_agents"].append(agent_name)
        
        for agent_name in specialized_agent_names:
            if agent_name in self.available_agents:
                agent_instance = self.available_agents[agent_name]()
                if hasattr(agent_instance, 'available') and not agent_instance.available:
                    health_status["missing_modules"].append(agent_name)
                else:
                    health_status["specialized_agents"].append(agent_name)
        
        # Overall status
        if health_status["missing_modules"] or health_status["api_status"] == "missing":
            health_status["status"] = "degraded"
        
        if not health_status["core_agents"]:
            health_status["status"] = "critical"
        
        return health_status
    
    def get_available_agents_config(self) -> Dict[str, bool]:
        """Get available agents configuration for UI"""
        health = self.check_system_health()
        
        agent_config = {}
        
        # Core agents
        core_mapping = {
            "ProductManager": "Product Manager",
            "Analyst": "Business Analyst", 
            "Engineer": "Software Engineer"
        }
        
        for internal_name, display_name in core_mapping.items():
            agent_config[display_name] = internal_name in health["core_agents"]
        
        # Extended agents
        extended_mapping = {
            "UXDesigner": "UX Designer",
            "MarketingStrategist": "Marketing Strategist",
            "TechnicalArchitect": "Technical Architect"
        }
        
        for internal_name, display_name in extended_mapping.items():
            # These might not be in health check yet, so check directly
            agent_config[display_name] = internal_name in self.available_agents
        
        # Specialized agents
        specialized_mapping = {
            "LegalAgent": "Legal Consultant",
            "ComplianceAgent": "Compliance Officer",
            "FinanceAgent": "Financial Analyst",
            "SecurityAgent": "Security Specialist"
        }
        
        for internal_name, display_name in specialized_mapping.items():
            agent_config[display_name] = internal_name in health["specialized_agents"]
        
        return agent_config
    
    def initialize_system(self) -> Dict[str, Any]:
        """Initialize the complete system"""
        logger.info("Initializing Enterprise AI Agent Consortium...")
        
        try:
            # Load all components
            core_agents = self.load_core_agents()
            specialized_agents = self.load_specialized_agents()
            utils = self.load_utils()
            
            # Get safe functions
            conversation_func = self.get_safe_conversation_function()
            graph_func = self.get_safe_graph_function()
            
            # Check system health
            health = self.check_system_health()
            
            initialization_result = {
                "success": True,
                "core_agents": core_agents,
                "specialized_agents": specialized_agents,
                "utils": utils,
                "conversation_function": conversation_func,
                "graph_function": graph_func,
                "health": health,
                "agent_config": self.get_available_agents_config()
            }
            
            logger.info(f"System initialized successfully. Status: {health['status']}")
            return initialization_result
            
        except Exception as e:
            logger.error(f"System initialization failed: {e}")
            logger.error(traceback.format_exc())
            
            # Return minimal fallback configuration
            return {
                "success": False,
                "error": str(e),
                "core_agents": {},
                "specialized_agents": {},
                "utils": {},
                "conversation_function": self.get_safe_conversation_function(),
                "graph_function": self.get_safe_graph_function(),
                "health": {"status": "critical", "error": str(e)},
                "agent_config": {}
            }

# Global integrator instance
integrator = SystemIntegrator()