"""
Database Manager for Enterprise AI Agent Consortium
Handles database connections and operations
"""

import os
import logging
from typing import Optional, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Manages database connections and operations"""
    
    def __init__(self):
        self.engine = None
        self.session_factory = None
        self.connected = False
        
    def initialize(self, database_url: str = None) -> bool:
        """Initialize database connection"""
        try:
            if not database_url:
                # Use SQLite as default for local development
                database_url = "sqlite:///enterprise_ai.db"
            
            self.engine = create_engine(database_url, echo=False)
            self.session_factory = sessionmaker(bind=self.engine)
            
            # Test connection
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            self.connected = True
            logger.info("Database connection established successfully")
            return True
            
        except SQLAlchemyError as e:
            logger.error(f"Database connection failed: {e}")
            self.connected = False
            return False
    
    def get_session(self):
        """Get a database session"""
        if not self.connected:
            return None
        return self.session_factory()
    
    def execute_query(self, query: str, params: Dict[str, Any] = None) -> Optional[Any]:
        """Execute a query safely"""
        if not self.connected:
            logger.warning("Database not connected")
            return None
            
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), params or {})
                return result.fetchall()
        except SQLAlchemyError as e:
            logger.error(f"Query execution failed: {e}")
            return None
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get database health status"""
        return {
            "connected": self.connected,
            "engine_url": str(self.engine.url) if self.engine else None,
            "status": "healthy" if self.connected else "disconnected"
        }

# Global database manager instance
db_manager = DatabaseManager()

# Initialize with default settings
db_manager.initialize()