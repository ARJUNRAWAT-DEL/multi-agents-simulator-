"""
Enterprise AI Agent Consortium - Database Models
SQLite database with SQLAlchemy ORM for conversation history, analytics, and user management
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, JSON, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import json
import uuid

Base = declarative_base()

class User(Base):
    """User management and authentication"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), unique=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(String(50), default='user')  # user, admin, enterprise
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    sessions = relationship("ConversationSession", back_populates="user")
    analytics = relationship("UserAnalytics", back_populates="user")

class ConversationSession(Base):
    """Track complete conversation sessions"""
    __tablename__ = 'conversation_sessions'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(50), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    project_title = Column(String(255), nullable=False)
    project_description = Column(Text, nullable=False)
    project_type = Column(String(100))
    industry = Column(String(100))
    
    # Configuration
    selected_agents = Column(JSON)  # Store which agents were selected
    rounds = Column(Integer, default=2)
    model_used = Column(String(100))
    output_format = Column(String(100))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    duration_seconds = Column(Integer)
    status = Column(String(50), default='active')  # active, completed, failed
    
    # Analytics
    total_messages = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    confidence_score = Column(Float)
    quality_score = Column(Float)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    messages = relationship("ConversationMessage", back_populates="session")
    analytics = relationship("SessionAnalytics", back_populates="session")

class ConversationMessage(Base):
    """Individual messages in conversations"""
    __tablename__ = 'conversation_messages'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('conversation_sessions.id'), nullable=False)
    message_id = Column(String(50), default=lambda: str(uuid.uuid4()))
    
    # Content
    role = Column(String(50))  # system, user, assistant
    agent_type = Column(String(100))  # ProductManager, Analyst, etc.
    content = Column(Text, nullable=False)
    
    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow)
    round_number = Column(Integer)
    message_order = Column(Integer)
    
    # Analytics
    token_count = Column(Integer)
    sentiment_score = Column(Float)
    confidence_score = Column(Float)
    topics = Column(JSON)  # Extracted topics/themes
    
    # Relationships
    session = relationship("ConversationSession", back_populates="messages")

class SessionAnalytics(Base):
    """Analytics and insights for conversation sessions"""
    __tablename__ = 'session_analytics'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('conversation_sessions.id'), nullable=False)
    
    # Performance Metrics
    response_time_avg = Column(Float)
    response_time_max = Column(Float)
    agent_participation = Column(JSON)  # Which agents contributed what
    
    # Content Analysis
    key_topics = Column(JSON)
    sentiment_analysis = Column(JSON)
    readability_score = Column(Float)
    technical_complexity = Column(Float)
    
    # Business Metrics
    market_opportunity_score = Column(Float)
    technical_feasibility_score = Column(Float)
    risk_assessment_score = Column(Float)
    innovation_score = Column(Float)
    
    # Recommendations
    success_probability = Column(Float)
    recommended_next_steps = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("ConversationSession", back_populates="analytics")

class UserAnalytics(Base):
    """User behavior and usage analytics"""
    __tablename__ = 'user_analytics'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Usage Statistics
    total_sessions = Column(Integer, default=0)
    total_messages = Column(Integer, default=0)
    avg_session_duration = Column(Float)
    preferred_agents = Column(JSON)
    preferred_industries = Column(JSON)
    
    # Performance Metrics
    avg_quality_score = Column(Float)
    success_rate = Column(Float)
    most_successful_project_type = Column(String(100))
    
    # Engagement
    last_active = Column(DateTime)
    total_active_days = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="analytics")

class ProjectTemplate(Base):
    """Reusable project templates and best practices"""
    __tablename__ = 'project_templates'
    
    id = Column(Integer, primary_key=True)
    template_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    industry = Column(String(100))
    
    # Template Content
    project_template = Column(Text)
    recommended_agents = Column(JSON)
    suggested_rounds = Column(Integer, default=2)
    expected_outcomes = Column(JSON)
    
    # Metadata
    created_by = Column(String(100))
    is_public = Column(Boolean, default=True)
    usage_count = Column(Integer, default=0)
    avg_rating = Column(Float)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DatabaseManager:
    """Database operations and management"""
    
    def __init__(self, database_url="sqlite:///enterprise_agents.db"):
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def create_user(self, username: str, email: str, role: str = "user") -> User:
        """Create new user"""
        session = self.get_session()
        try:
            user = User(
                user_id=str(uuid.uuid4()),
                username=username,
                email=email,
                role=role
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            session.close()
    
    def create_conversation_session(self, user_id: int, project_data: dict) -> ConversationSession:
        """Create new conversation session"""
        session = self.get_session()
        try:
            conv_session = ConversationSession(
                user_id=user_id,
                project_title=project_data.get('title', 'Untitled Project'),
                project_description=project_data.get('description', ''),
                project_type=project_data.get('type'),
                industry=project_data.get('industry'),
                selected_agents=project_data.get('agents', {}),
                rounds=project_data.get('rounds', 2),
                model_used=project_data.get('model', 'llama-3.3-70b-versatile'),
                output_format=project_data.get('output_format', 'Executive Summary')
            )
            session.add(conv_session)
            session.commit()
            session.refresh(conv_session)
            return conv_session
        finally:
            session.close()
    
    def save_message(self, session_id: int, message_data: dict) -> ConversationMessage:
        """Save conversation message"""
        session = self.get_session()
        try:
            message = ConversationMessage(
                session_id=session_id,
                role=message_data.get('role'),
                agent_type=message_data.get('agent_type'),
                content=message_data.get('content'),
                round_number=message_data.get('round_number'),
                message_order=message_data.get('message_order'),
                token_count=len(message_data.get('content', '').split())
            )
            session.add(message)
            session.commit()
            session.refresh(message)
            return message
        finally:
            session.close()
    
    def get_user_sessions(self, user_id: int, limit: int = 50) -> list[ConversationSession]:
        """Get user's conversation sessions"""
        session = self.get_session()
        try:
            return session.query(ConversationSession)\
                         .filter(ConversationSession.user_id == user_id)\
                         .order_by(ConversationSession.created_at.desc())\
                         .limit(limit).all()
        finally:
            session.close()
    
    def get_session_analytics(self, session_id: int) -> SessionAnalytics:
        """Get analytics for specific session"""
        session = self.get_session()
        try:
            return session.query(SessionAnalytics)\
                         .filter(SessionAnalytics.session_id == session_id)\
                         .first()
        finally:
            session.close()

# Global database manager instance
db_manager = DatabaseManager()