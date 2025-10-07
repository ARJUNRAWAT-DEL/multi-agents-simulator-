"""
AI Analytics Engine for Enterprise AI Agent Consortium
Provides analytics and insights for agent interactions and system performance
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

class AIAnalyticsEngine:
    """Provides analytics and insights for the multi-agent system"""
    
    def __init__(self):
        self.interaction_history = []
        self.agent_performance = {}
        self.system_metrics = {
            "total_interactions": 0,
            "successful_completions": 0,
            "average_response_time": 0.0,
            "agent_utilization": {}
        }
    
    def log_interaction(self, agent_name: str, message: str, response: str, 
                       response_time: float = 0.0, success: bool = True):
        """Log an agent interaction for analytics"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "agent_name": agent_name,
            "message_length": len(message),
            "response_length": len(response),
            "response_time": response_time,
            "success": success
        }
        
        self.interaction_history.append(interaction)
        self.update_metrics(agent_name, response_time, success)
        
        # Keep only last 1000 interactions to prevent memory issues
        if len(self.interaction_history) > 1000:
            self.interaction_history = self.interaction_history[-1000:]
    
    def update_metrics(self, agent_name: str, response_time: float, success: bool):
        """Update system metrics"""
        self.system_metrics["total_interactions"] += 1
        
        if success:
            self.system_metrics["successful_completions"] += 1
        
        # Update average response time
        current_avg = self.system_metrics["average_response_time"]
        total = self.system_metrics["total_interactions"]
        self.system_metrics["average_response_time"] = (
            (current_avg * (total - 1) + response_time) / total
        )
        
        # Update agent utilization
        if agent_name not in self.system_metrics["agent_utilization"]:
            self.system_metrics["agent_utilization"][agent_name] = 0
        self.system_metrics["agent_utilization"][agent_name] += 1
        
        # Update agent performance
        if agent_name not in self.agent_performance:
            self.agent_performance[agent_name] = {
                "total_requests": 0,
                "successful_requests": 0,
                "average_response_time": 0.0,
                "success_rate": 0.0
            }
        
        perf = self.agent_performance[agent_name]
        perf["total_requests"] += 1
        
        if success:
            perf["successful_requests"] += 1
        
        # Update average response time for this agent
        prev_avg = perf["average_response_time"]
        total_requests = perf["total_requests"]
        perf["average_response_time"] = (
            (prev_avg * (total_requests - 1) + response_time) / total_requests
        )
        
        # Update success rate
        perf["success_rate"] = perf["successful_requests"] / perf["total_requests"]
    
    def get_system_analytics(self) -> Dict[str, Any]:
        """Get comprehensive system analytics"""
        return {
            "system_metrics": self.system_metrics,
            "agent_performance": self.agent_performance,
            "recent_activity": self.get_recent_activity(),
            "top_performing_agents": self.get_top_agents(),
            "analytics_timestamp": datetime.now().isoformat()
        }
    
    def get_recent_activity(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get recent activity within specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent = []
        
        for interaction in self.interaction_history:
            interaction_time = datetime.fromisoformat(interaction["timestamp"])
            if interaction_time >= cutoff_time:
                recent.append(interaction)
        
        return recent
    
    def get_top_agents(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top performing agents"""
        agents = []
        
        for agent_name, perf in self.agent_performance.items():
            agents.append({
                "agent_name": agent_name,
                "success_rate": perf["success_rate"],
                "total_requests": perf["total_requests"],
                "average_response_time": perf["average_response_time"]
            })
        
        # Sort by success rate and total requests
        agents.sort(key=lambda x: (x["success_rate"], x["total_requests"]), reverse=True)
        return agents[:limit]
    
    def generate_insights(self) -> List[str]:
        """Generate actionable insights from analytics data"""
        insights = []
        
        if self.system_metrics["total_interactions"] == 0:
            insights.append("No interactions recorded yet. System is ready for use.")
            return insights
        
        # Success rate insights
        success_rate = (self.system_metrics["successful_completions"] / 
                       self.system_metrics["total_interactions"])
        
        if success_rate > 0.95:
            insights.append("Excellent system performance with >95% success rate.")
        elif success_rate > 0.85:
            insights.append("Good system performance. Minor optimizations possible.")
        else:
            insights.append("System performance needs attention. Check error logs.")
        
        # Response time insights
        avg_time = self.system_metrics["average_response_time"]
        if avg_time > 10.0:
            insights.append("High response times detected. Consider system optimization.")
        elif avg_time < 2.0:
            insights.append("Excellent response times. System is well-optimized.")
        
        # Agent utilization insights
        utilization = self.system_metrics["agent_utilization"]
        if utilization:
            most_used = max(utilization, key=utilization.get)
            least_used = min(utilization, key=utilization.get)
            
            if utilization[most_used] > utilization[least_used] * 3:
                insights.append(f"Uneven agent usage. {most_used} is heavily utilized.")
        
        return insights
    
    def export_analytics(self) -> str:
        """Export analytics data as JSON string"""
        analytics_data = self.get_system_analytics()
        analytics_data["insights"] = self.generate_insights()
        return json.dumps(analytics_data, indent=2)

# Global analytics engine instance
ai_analytics = AIAnalyticsEngine()