"""
Enterprise AI Agent Consortium - REST API
FastAPI-based REST API for enterprise integration and programmatic access
"""

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import json

# API Models
class ProjectRequest(BaseModel):
    """Request model for project analysis"""
    project_title: str = Field(..., description="Project title")
    project_description: str = Field(..., description="Detailed project description")
    project_type: str = Field(..., description="Project category")
    industry: str = Field(..., description="Target industry")
    selected_agents: Dict[str, bool] = Field(..., description="Agent selection configuration")
    rounds: int = Field(default=2, ge=1, le=5, description="Number of collaboration rounds")
    model: str = Field(default="llama-3.3-70b-versatile", description="AI model to use")
    output_format: str = Field(default="Executive Summary", description="Report format")

class AgentMessage(BaseModel):
    """Individual agent message model"""
    role: str
    agent_type: str
    content: str
    timestamp: datetime
    round_number: Optional[int] = None
    message_order: Optional[int] = None

class ConversationResponse(BaseModel):
    """Response model for conversation analysis"""
    session_id: str
    status: str
    conversation: List[AgentMessage]
    final_report: str
    analytics: Optional[Dict[str, Any]] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

class AnalyticsResponse(BaseModel):
    """Response model for analytics data"""
    session_id: str
    sentiment_score: float
    confidence_score: float
    quality_score: float
    success_probability: float
    technical_complexity: float
    business_value: float
    key_topics: List[str]
    risk_factors: List[str]
    recommendations: List[str]

class SessionListResponse(BaseModel):
    """Response model for session list"""
    sessions: List[Dict[str, Any]]
    total_count: int
    page: int
    page_size: int

class UserModel(BaseModel):
    """User model for API responses"""
    user_id: str
    username: str
    email: str
    role: str
    created_at: datetime
    last_login: Optional[datetime] = None

class APIKeyModel(BaseModel):
    """API key creation request"""
    name: str
    description: Optional[str] = None
    expires_at: Optional[datetime] = None

# FastAPI app initialization
app = FastAPI(
    title="Enterprise AI Agent Consortium API",
    description="Professional multi-agent collaboration platform for strategic product development",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# In-memory storage (replace with database in production)
api_keys = {
    "demo-key-12345": {
        "user_id": "demo-user",
        "name": "Demo API Key",
        "created_at": datetime.now(),
        "last_used": None,
        "is_active": True
    }
}

active_sessions = {}

# Authentication dependency
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Validate API key and return user information"""
    token = credentials.credentials
    
    if token not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    key_info = api_keys[token]
    if not key_info["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last used timestamp
    api_keys[token]["last_used"] = datetime.now()
    
    return key_info

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }

# Agent information endpoints
@app.get("/agents")
async def list_agents(current_user: dict = Depends(get_current_user)):
    """List all available agents and their capabilities"""
    agents_info = {
        "Product Manager": {
            "description": "Senior Product Manager with strategic planning expertise",
            "capabilities": ["Product strategy", "Stakeholder management", "Requirements engineering"],
            "default_enabled": True
        },
        "Business Analyst": {
            "description": "Senior Business Analyst with market research expertise", 
            "capabilities": ["Market analysis", "Competitive research", "Financial modeling"],
            "default_enabled": True
        },
        "Software Engineer": {
            "description": "Principal Software Engineer with system design expertise",
            "capabilities": ["System architecture", "Technology selection", "Development planning"],
            "default_enabled": True
        },
        "UX Designer": {
            "description": "Senior UX/UI Designer with user-centered design expertise",
            "capabilities": ["User research", "Information architecture", "Design systems"],
            "default_enabled": False
        },
        "Marketing Strategist": {
            "description": "Senior Marketing Strategist with go-to-market expertise",
            "capabilities": ["Go-to-market strategy", "Brand development", "Growth marketing"],
            "default_enabled": False
        },
        "Technical Architect": {
            "description": "Principal Technical Architect with enterprise systems expertise",
            "capabilities": ["Enterprise architecture", "Cloud strategy", "Security architecture"],
            "default_enabled": False
        },
        "Legal Compliance Agent": {
            "description": "Senior Legal & Compliance Officer with regulatory expertise",
            "capabilities": ["Regulatory compliance", "IP protection", "Risk assessment"],
            "default_enabled": False
        },
        "Financial Analyst": {
            "description": "Senior Financial Analyst with investment analysis expertise",
            "capabilities": ["Financial modeling", "Investment analysis", "Risk management"],
            "default_enabled": False
        },
        "Security Expert": {
            "description": "Chief Information Security Officer with cybersecurity expertise",
            "capabilities": ["Security architecture", "Risk assessment", "Compliance"],
            "default_enabled": False
        },
        "Operations Director": {
            "description": "Chief Operations Officer with operational excellence expertise",
            "capabilities": ["Process optimization", "Resource planning", "Quality management"],
            "default_enabled": False
        }
    }
    
    return {
        "agents": agents_info,
        "total_count": len(agents_info)
    }

# Project analysis endpoints
@app.post("/projects/analyze", response_model=ConversationResponse)
async def analyze_project(
    request: ProjectRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Start a new project analysis with selected agents"""
    
    session_id = str(uuid.uuid4())
    
    # Validate agent selection
    valid_agents = [
        "Product Manager", "Business Analyst", "Software Engineer",
        "UX Designer", "Marketing Strategist", "Technical Architect",
        "Legal Compliance Agent", "Financial Analyst", "Security Expert",
        "Operations Director"
    ]
    
    selected_agents = {k: v for k, v in request.selected_agents.items() if k in valid_agents}
    
    if not any(selected_agents.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one agent must be selected"
        )
    
    # Create session data
    session_data = {
        "session_id": session_id,
        "user_id": current_user["user_id"],
        "project_title": request.project_title,
        "project_description": request.project_description,
        "project_type": request.project_type,
        "industry": request.industry,
        "selected_agents": selected_agents,
        "rounds": request.rounds,
        "model": request.model,
        "output_format": request.output_format,
        "status": "processing",
        "created_at": datetime.now(),
        "conversation": [],
        "final_report": "",
        "analytics": None
    }
    
    active_sessions[session_id] = session_data
    
    # Start background processing
    background_tasks.add_task(process_conversation, session_id, request)
    
    return ConversationResponse(
        session_id=session_id,
        status="processing",
        conversation=[],
        final_report="",
        created_at=session_data["created_at"]
    )

async def process_conversation(session_id: str, request: ProjectRequest):
    """Background task to process the conversation"""
    try:
        # Import conversation simulation here to avoid circular imports
        from utils.conversation import simulate_conversation
        from analytics.engine import analytics_engine
        
        # Enhanced context for agents
        enhanced_context = f"""
        Project: {request.project_description}
        Category: {request.project_type}
        Industry: {request.industry}
        Output Format: {request.output_format}
        Selected Agents: {', '.join([k for k, v in request.selected_agents.items() if v])}
        """
        
        # Run conversation simulation
        conversation, report = simulate_conversation(
            enhanced_context,
            turns=request.rounds,
            selected_agents=request.selected_agents,
            model=request.model,
            output_format=request.output_format
        )
        
        # Run analytics
        analytics_result = analytics_engine.analyze_conversation(conversation, report)
        
        # Update session with results
        if session_id in active_sessions:
            active_sessions[session_id].update({
                "status": "completed",
                "completed_at": datetime.now(),
                "conversation": conversation,
                "final_report": report,
                "analytics": {
                    "sentiment_score": analytics_result.sentiment_score,
                    "confidence_score": analytics_result.confidence_score,
                    "quality_score": analytics_result.quality_score,
                    "success_probability": analytics_result.success_probability,
                    "technical_complexity": analytics_result.technical_complexity,
                    "business_value": analytics_result.business_value,
                    "key_topics": analytics_result.key_topics,
                    "risk_factors": analytics_result.risk_factors,
                    "recommendations": analytics_result.recommendations
                }
            })
    
    except Exception as e:
        # Update session with error status
        if session_id in active_sessions:
            active_sessions[session_id].update({
                "status": "failed",
                "error": str(e),
                "completed_at": datetime.now()
            })

@app.get("/projects/{session_id}", response_model=ConversationResponse)
async def get_project_analysis(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get the results of a project analysis"""
    
    if session_id not in active_sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    session_data = active_sessions[session_id]
    
    # Check user authorization
    if session_data["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Convert conversation messages to proper format
    conversation_messages = []
    for msg in session_data["conversation"]:
        conversation_messages.append(AgentMessage(
            role=msg.get("role", "assistant"),
            agent_type=msg.get("agent_type", "Unknown"),
            content=msg.get("content", ""),
            timestamp=datetime.now(),  # In real implementation, store actual timestamps
            round_number=msg.get("round_number"),
            message_order=msg.get("message_order")
        ))
    
    return ConversationResponse(
        session_id=session_id,
        status=session_data["status"],
        conversation=conversation_messages,
        final_report=session_data["final_report"],
        analytics=session_data["analytics"],
        created_at=session_data["created_at"],
        completed_at=session_data.get("completed_at")
    )

@app.get("/projects/{session_id}/analytics", response_model=AnalyticsResponse)
async def get_project_analytics(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get detailed analytics for a project analysis"""
    
    if session_id not in active_sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    session_data = active_sessions[session_id]
    
    if session_data["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    analytics = session_data.get("analytics")
    if not analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analytics not available for this session"
        )
    
    return AnalyticsResponse(
        session_id=session_id,
        **analytics
    )

@app.get("/projects", response_model=SessionListResponse)
async def list_user_projects(
    page: int = 1,
    page_size: int = 20,
    current_user: dict = Depends(get_current_user)
):
    """List user's project analysis sessions"""
    
    user_sessions = [
        session for session in active_sessions.values()
        if session["user_id"] == current_user["user_id"]
    ]
    
    # Sort by creation date (newest first)
    user_sessions.sort(key=lambda x: x["created_at"], reverse=True)
    
    # Pagination
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paginated_sessions = user_sessions[start_idx:end_idx]
    
    # Format for response
    session_summaries = []
    for session in paginated_sessions:
        session_summaries.append({
            "session_id": session["session_id"],
            "project_title": session["project_title"],
            "project_type": session["project_type"],
            "industry": session["industry"],
            "status": session["status"],
            "created_at": session["created_at"],
            "completed_at": session.get("completed_at"),
            "success_probability": session.get("analytics", {}).get("success_probability")
        })
    
    return SessionListResponse(
        sessions=session_summaries,
        total_count=len(user_sessions),
        page=page,
        page_size=page_size
    )

# PDF Report endpoint
@app.get("/projects/{session_id}/report/pdf")
async def download_pdf_report(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Download PDF report for a project analysis"""
    
    if session_id not in active_sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    session_data = active_sessions[session_id]
    
    if session_data["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    try:
        from reports.pdf_generator import pdf_generator
        
        if not pdf_generator:
            raise HTTPException(
                status_code=status.HTTP_501_NOT_IMPLEMENTED,
                detail="PDF generation not available"
            )
        
        pdf_bytes = pdf_generator.generate_executive_report(
            session_data,
            session_data["conversation"],
            session_data["final_report"],
            session_data.get("analytics")
        )
        
        from fastapi.responses import Response
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=project_analysis_{session_id}.pdf"
            }
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate PDF: {str(e)}"
        )

# Configuration endpoints
@app.get("/config/models")
async def list_available_models(current_user: dict = Depends(get_current_user)):
    """List available AI models"""
    return {
        "models": [
            {
                "name": "llama-3.3-70b-versatile",
                "description": "Llama 3 70B - High performance model for complex analysis",
                "recommended": True
            },
            {
                "name": "llama3-8b-8192", 
                "description": "Llama 3 8B - Fast model for quick analysis",
                "recommended": False
            },
            {
                "name": "mixtral-8x7b-32768",
                "description": "Mixtral 8x7B - Specialized model for technical analysis",
                "recommended": False
            }
        ]
    }

@app.get("/config/templates")
async def list_project_templates(current_user: dict = Depends(get_current_user)):
    """List available project templates"""
    templates = {
        "Fintech App": {
            "description": "Build a comprehensive fintech mobile application",
            "category": "Mobile Application",
            "industry": "Finance",
            "recommended_agents": ["Product Manager", "Financial Analyst", "Security Expert"]
        },
        "HealthTech Platform": {
            "description": "Develop a telemedicine platform",
            "category": "Web Platform",
            "industry": "Healthcare", 
            "recommended_agents": ["Product Manager", "Legal Compliance Agent", "Security Expert"]
        },
        "EdTech Solution": {
            "description": "Create an adaptive learning platform",
            "category": "Web Platform",
            "industry": "Education",
            "recommended_agents": ["Product Manager", "UX Designer", "Technical Architect"]
        },
        "E-commerce Platform": {
            "description": "Build a next-generation e-commerce marketplace",
            "category": "Web Platform",
            "industry": "Retail",
            "recommended_agents": ["Product Manager", "Marketing Strategist", "Operations Director"]
        }
    }
    
    return {"templates": templates}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)