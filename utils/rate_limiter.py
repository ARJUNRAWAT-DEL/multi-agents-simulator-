"""
Rate Limiting and API Management Utility
Handles API rate limiting, token tracking, and fallback responses
"""

import time
import logging
from typing import Dict, Optional, Any, List
from datetime import datetime, timedelta
import json
import os

# Make Groq import optional since we're using emergency fallback
try:
    from groq import Groq
    from groq.types.chat import ChatCompletion
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    Groq = None
    ChatCompletion = None

logger = logging.getLogger(__name__)

class RateLimitManager:
    """Manages API rate limiting and token usage tracking"""
    
    def __init__(self):
        self.daily_token_limit = 100000  # Groq free tier daily limit
        self.tokens_used_today = 0
        self.last_reset_date = datetime.now().date()
        self.request_timestamps = []
        self.max_requests_per_minute = 30  # Conservative limit
        self.min_request_interval = 2.0  # Minimum seconds between requests
        self.last_request_time = 0
        
        # Load token usage from file if exists
        self._load_token_usage()
    
    def _load_token_usage(self):
        """Load token usage from persistent storage"""
        try:
            if os.path.exists('token_usage.json'):
                with open('token_usage.json', 'r') as f:
                    data = json.load(f)
                    saved_date = datetime.fromisoformat(data.get('date', str(datetime.now().date())))
                    
                    # Reset if it's a new day
                    if saved_date.date() == datetime.now().date():
                        self.tokens_used_today = data.get('tokens_used', 0)
                    else:
                        self.tokens_used_today = 0
        except Exception as e:
            logger.warning(f"Could not load token usage: {e}")
            self.tokens_used_today = 0
    
    def _save_token_usage(self):
        """Save token usage to persistent storage"""
        try:
            data = {
                'date': str(datetime.now().date()),
                'tokens_used': self.tokens_used_today
            }
            with open('token_usage.json', 'w') as f:
                json.dump(data, f)
        except Exception as e:
            logger.warning(f"Could not save token usage: {e}")
    
    def can_make_request(self, estimated_tokens: int = 1000) -> tuple[bool, str]:
        """Check if we can make a request without hitting limits"""
        current_time = time.time()
        
        # Be very conservative - if we're above 95% usage, block all requests
        if self.tokens_used_today + estimated_tokens > (self.daily_token_limit * 0.95):
            remaining_tokens = self.daily_token_limit - self.tokens_used_today
            return False, f"Conservative rate limit reached. Remaining: {remaining_tokens} tokens (95% limit)"
        
        # Check daily token limit
        if self.tokens_used_today + estimated_tokens > self.daily_token_limit:
            remaining_tokens = self.daily_token_limit - self.tokens_used_today
            return False, f"Daily token limit would be exceeded. Remaining: {remaining_tokens} tokens"
        
        # Check rate limiting (requests per minute)
        now = datetime.now()
        # Remove timestamps older than 1 minute
        self.request_timestamps = [
            ts for ts in self.request_timestamps 
            if now - ts < timedelta(minutes=1)
        ]
        
        if len(self.request_timestamps) >= self.max_requests_per_minute:
            return False, "Rate limit: Too many requests per minute"
        
        # Check minimum interval between requests
        if current_time - self.last_request_time < self.min_request_interval:
            wait_time = self.min_request_interval - (current_time - self.last_request_time)
            return False, f"Rate limit: Wait {wait_time:.1f} seconds before next request"
        
        return True, "OK"
    
    def record_request(self, tokens_used: int = 0):
        """Record that a request was made"""
        self.request_timestamps.append(datetime.now())
        self.last_request_time = time.time()
        self.tokens_used_today += tokens_used
        self._save_token_usage()
        
        logger.info(f"API request made. Tokens used today: {self.tokens_used_today}/{self.daily_token_limit}")
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get current usage statistics"""
        return {
            "tokens_used_today": self.tokens_used_today,
            "daily_limit": self.daily_token_limit,
            "remaining_tokens": self.daily_token_limit - self.tokens_used_today,
            "usage_percentage": (self.tokens_used_today / self.daily_token_limit) * 100,
            "requests_last_minute": len(self.request_timestamps),
            "can_make_request": self.can_make_request()[0]
        }

class GroqClientManager:
    """Enhanced Groq client with rate limiting and fallback handling"""
    
    def __init__(self):
        # Only initialize Groq client if available and API key exists
        if GROQ_AVAILABLE and os.getenv("GROQ_API_KEY"):
            try:
                self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            except Exception as e:
                logger.warning(f"Failed to initialize Groq client: {e}")
                self.client = None
        else:
            self.client = None
            logger.info("Groq client not available - using fallback mode only")
            
        self.rate_limiter = RateLimitManager()
        
        # Fallback responses for different agent types
        self.fallback_responses = {
            "ProductManager": "I'm currently at capacity, but based on the project context, I recommend focusing on user requirements, market analysis, and creating a clear product roadmap. Please try again in a few minutes for detailed analysis.",
            
            "Analyst": "Due to high demand, I'm providing a brief analysis: Focus on data-driven insights, identify key metrics, and consider stakeholder needs. For comprehensive analysis, please retry in a few minutes.",
            
            "Engineer": "System temporarily at capacity. Quick recommendation: Ensure clean architecture, consider scalability, implement proper error handling, and maintain code quality. Detailed technical analysis available shortly.",
            
            "LegalComplianceAgent": "Legal review capacity reached. Key considerations: Ensure GDPR compliance, review terms of service, check IP requirements, and maintain audit trails. Full legal analysis available soon.",
            
            "FinancialAnalyst": "Financial analysis temporarily limited. Focus on: ROI calculations, budget planning, cost-benefit analysis, and risk assessment. Detailed financial modeling available after rate limit reset.",
            
            "SecurityExpert": "Security review at capacity. Priority items: Implement authentication, encrypt sensitive data, ensure secure communications, and maintain access controls. Comprehensive security audit available shortly.",
            
            "default": "I'm currently experiencing high demand. Please try again in a few minutes for a detailed response. In the meantime, consider the key aspects of your request and any immediate actions you can take."
        }
    
    def safe_chat_completion(self, messages: List[Dict], agent_type: str = "default", 
                           temperature: float = 0.4, max_tokens: int = 1000) -> str:
        """Make a chat completion with rate limiting and fallback"""
        
        # If Groq client is not available, use fallback immediately
        if not self.client:
            logger.info("Groq client not available - using fallback response")
            return self._get_fallback_response(agent_type, "Groq client not initialized")
        
        # Estimate tokens (rough approximation)
        estimated_tokens = sum(len(str(msg)) for msg in messages) // 4 + max_tokens
        
        # Check if we can make the request
        can_request, reason = self.rate_limiter.can_make_request(estimated_tokens)
        
        if not can_request:
            logger.warning(f"Rate limit hit: {reason}")
            return self._get_fallback_response(agent_type, reason)
        
        try:
            # Add rate limiting delay
            time.sleep(1)  # Small delay to be respectful to API
            
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            # Record successful request
            actual_tokens = getattr(response.usage, 'total_tokens', estimated_tokens)
            self.rate_limiter.record_request(actual_tokens)
            
            return response.choices[0].message.content
            
        except Exception as e:
            error_str = str(e)
            logger.error(f"API request failed: {error_str}")
            
            # Handle specific rate limit errors
            if "rate_limit_exceeded" in error_str or "429" in error_str:
                # Update our local tracking to match the actual usage from the error
                if "Used" in error_str and "Limit" in error_str:
                    try:
                        # Parse actual usage from error message
                        import re
                        usage_match = re.search(r"Used (\d+)", error_str)
                        limit_match = re.search(r"Limit (\d+)", error_str)
                        if usage_match and limit_match:
                            actual_used = int(usage_match.group(1))
                            actual_limit = int(limit_match.group(1))
                            
                            # Update our tracking to match reality
                            self.rate_limiter.daily_token_limit = actual_limit
                            self.rate_limiter.tokens_used_today = actual_used
                            self.rate_limiter._save_token_usage()
                            
                            logger.warning(f"Updated rate limiter: {actual_used}/{actual_limit} tokens")
                    except Exception as parse_error:
                        logger.error(f"Could not parse rate limit error: {parse_error}")
                
                return self._get_fallback_response(agent_type, "Rate limit exceeded - Daily quota reached")
            
            # Handle other API errors
            return self._get_fallback_response(agent_type, f"API error: {error_str}")
    
    def _get_fallback_response(self, agent_type: str, reason: str) -> str:
        """Get appropriate fallback response"""
        
        # Check if we're completely out of quota (>95%)
        usage_stats = self.rate_limiter.get_usage_stats()
        
        if usage_stats['usage_percentage'] > 95:
            # Use emergency fallback system for intelligent responses
            try:
                from utils.emergency_fallback import emergency_engine
                return emergency_engine.get_fallback_response("General project inquiry", agent_type)
            except ImportError:
                pass
        
        # Use basic fallback
        base_response = self.fallback_responses.get(agent_type, self.fallback_responses["default"])
        
        return f"""
{base_response}

📊 **Current API Usage Status:**
- Tokens used today: {usage_stats['tokens_used_today']:,}/{usage_stats['daily_limit']:,}
- Usage: {usage_stats['usage_percentage']:.1f}%
- Remaining tokens: {usage_stats['remaining_tokens']:,}

💡 **Reason:** {reason}

🔄 **Next Steps:**
1. Wait for daily quota reset (resets at midnight PT)
2. Consider upgrading to Groq Dev Tier for higher limits
3. Continue using emergency fallback mode for basic guidance

⏰ **Service resumes in**: {24 - datetime.now().hour} hours (approximate)
        """.strip()
    
    def get_usage_dashboard(self) -> Dict[str, Any]:
        """Get usage dashboard data"""
        return self.rate_limiter.get_usage_stats()

# Global instance
groq_manager = GroqClientManager()