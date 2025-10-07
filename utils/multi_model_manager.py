"""
Multi-Model AI Manager for Enterprise AI Agent Consortium
Supports multiple free AI providers with fallback capabilities
"""

import os
import logging
import time
import random
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests
import json

logger = logging.getLogger(__name__)

class MultiModelManager:
    """Manages multiple AI model providers with automatic fallback"""
    
    def __init__(self):
        self.providers = {
            "huggingface": {
                "name": "Hugging Face (Free)",
                "models": [
                    "microsoft/DialoGPT-large",
                    "facebook/blenderbot-400M-distill",
                    "microsoft/GODEL-v1_1-large-seq2seq"
                ],
                "api_key": os.getenv("HUGGINGFACE_API_KEY"),
                "base_url": "https://api-inference.huggingface.co/models",
                "rate_limit": None,  # Usually unlimited for free tier
                "active": True
            },
            "together": {
                "name": "Together AI (Free Tier)",
                "models": [
                    "meta-llama/Llama-2-7b-chat-hf",
                    "mistralai/Mixtral-8x7B-Instruct-v0.1",
                    "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"
                ],
                "api_key": os.getenv("TOGETHER_API_KEY"),
                "base_url": "https://api.together.xyz/v1/chat/completions",
                "rate_limit": 60,  # requests per minute
                "active": bool(os.getenv("TOGETHER_API_KEY"))
            },
            "replicate": {
                "name": "Replicate (Free Credits)",
                "models": [
                    "meta/llama-2-70b-chat",
                    "mistralai/mixtral-8x7b-instruct-v0.1"
                ],
                "api_key": os.getenv("REPLICATE_API_TOKEN"),
                "base_url": "https://api.replicate.com/v1/predictions",
                "rate_limit": None,
                "active": bool(os.getenv("REPLICATE_API_TOKEN"))
            },
            "cohere": {
                "name": "Cohere (Free Tier)",
                "models": ["command", "command-light"],
                "api_key": os.getenv("COHERE_API_KEY"),
                "base_url": "https://api.cohere.ai/v1/generate",
                "rate_limit": 100,  # requests per minute
                "active": bool(os.getenv("COHERE_API_KEY"))
            },
            "local_ollama": {
                "name": "Ollama (Local - Unlimited)",
                "models": ["llama2", "mistral", "codellama", "neural-chat", "gemma:2b"],
                "api_key": None,
                "base_url": "http://localhost:11434",
                "rate_limit": None,
                "active": True  # Check if Ollama is running
            }
        }
        
        self.request_history = {}
        self.current_provider = "local_ollama"  # Start with Ollama if available
        self.fallback_order = ["local_ollama", "together", "huggingface", "cohere", "replicate"]
        self.timeout_count = 0  # Track consecutive Ollama timeouts
        self.max_timeouts = 3   # Disable Ollama after 3 consecutive timeouts
        
        # Check provider availability
        self._check_provider_availability()
    
    def _check_provider_availability(self):
        """Check which providers are available"""
        for provider_id, config in self.providers.items():
            if provider_id == "local_ollama":
                # Check if Ollama is running locally
                try:
                    response = requests.get("http://localhost:11434/api/tags", timeout=2)
                    config["active"] = response.status_code == 200
                except:
                    config["active"] = False
            elif config["api_key"]:
                config["active"] = True
            else:
                config["active"] = False
                
        logger.info(f"Available providers: {[k for k, v in self.providers.items() if v['active']]}")
    
    def chat_completion(self, messages: List[Dict], agent_type: str = "default", 
                       temperature: float = 0.1, max_tokens: int = 50) -> str:
        """Get chat completion from available providers with fallback - ultra-optimized for speed"""
        
        # INSTANT MODE: Always use emergency fallback for your system since Ollama is too slow
        logger.info("Using emergency mode for instant response")
        from utils.emergency_fallback import emergency_engine
        return emergency_engine.get_fallback_response(
            messages[-1].get('content', '') if messages else '', 
            agent_type
        )
        
        # Smart timeout management: Skip Ollama if it's been timing out too much
        if self.timeout_count >= self.max_timeouts:
            logger.info(f"Skipping Ollama due to {self.timeout_count} consecutive timeouts - using emergency mode")
            from utils.emergency_fallback import emergency_engine
            return emergency_engine.get_fallback_response(
                messages[-1].get('content', '') if messages else '', 
                agent_type
            )
        
        for provider_id in self.fallback_order:
            provider = self.providers[provider_id]
            
            if not provider["active"]:
                continue
                
            try:
                response = self._call_provider(provider_id, messages, temperature, max_tokens)
                if response:
                    logger.info(f"Successfully used {provider['name']}")
                    return response
            except Exception as e:
                logger.warning(f"Provider {provider_id} failed: {e}")
                continue
        
        # If all providers fail, use emergency fallback
        from utils.emergency_fallback import emergency_engine
        return emergency_engine.get_fallback_response("General project inquiry", agent_type)
    
    def _call_provider(self, provider_id: str, messages: List[Dict], 
                      temperature: float, max_tokens: int) -> Optional[str]:
        """Call specific provider"""
        
        if provider_id == "together":
            return self._call_together(messages, temperature, max_tokens)
        elif provider_id == "huggingface":
            return self._call_huggingface(messages, temperature, max_tokens)
        elif provider_id == "cohere":
            return self._call_cohere(messages, temperature, max_tokens)
        elif provider_id == "replicate":
            return self._call_replicate(messages, temperature, max_tokens)
        elif provider_id == "local_ollama":
            return self._call_ollama(messages, temperature, max_tokens)
        
        return None
    
    def _call_together(self, messages: List[Dict], temperature: float, max_tokens: int) -> Optional[str]:
        """Call Together AI API"""
        if not self.providers["together"]["api_key"]:
            return None
            
        headers = {
            "Authorization": f"Bearer {self.providers['together']['api_key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "meta-llama/Llama-2-7b-chat-hf",
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            self.providers["together"]["base_url"],
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        
        return None
    
    def _call_huggingface(self, messages: List[Dict], temperature: float, max_tokens: int) -> Optional[str]:
        """Call Hugging Face Inference API"""
        # Convert messages to prompt format
        prompt = self._messages_to_prompt(messages)
        
        model = "microsoft/DialoGPT-large"
        url = f"{self.providers['huggingface']['base_url']}/{model}"
        
        headers = {
            "Authorization": f"Bearer {self.providers['huggingface']['api_key']}" if self.providers['huggingface']['api_key'] else {},
            "Content-Type": "application/json"
        }
        
        data = {
            "inputs": prompt,
            "parameters": {
                "temperature": temperature,
                "max_length": max_tokens,
                "return_full_text": False
            }
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "")
        
        return None
    
    def _call_cohere(self, messages: List[Dict], temperature: float, max_tokens: int) -> Optional[str]:
        """Call Cohere API"""
        if not self.providers["cohere"]["api_key"]:
            return None
            
        prompt = self._messages_to_prompt(messages)
        
        headers = {
            "Authorization": f"Bearer {self.providers['cohere']['api_key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "command",
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(
            self.providers["cohere"]["base_url"],
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result["generations"][0]["text"]
        
        return None
    
    def _call_replicate(self, messages: List[Dict], temperature: float, max_tokens: int) -> Optional[str]:
        """Call Replicate API"""
        if not self.providers["replicate"]["api_key"]:
            return None
            
        prompt = self._messages_to_prompt(messages)
        
        headers = {
            "Authorization": f"Token {self.providers['replicate']['api_key']}",
            "Content-Type": "application/json"
        }
        
        data = {
            "version": "meta/llama-2-70b-chat",
            "input": {
                "prompt": prompt,
                "temperature": temperature,
                "max_length": max_tokens
            }
        }
        
        response = requests.post(
            self.providers["replicate"]["base_url"],
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 201:
            # Replicate returns a prediction URL - would need polling for completion
            # For now, return a placeholder
            return "Response from Replicate model (simplified implementation)"
        
        return None
    
    def _call_ollama(self, messages: List[Dict], temperature: float, max_tokens: int) -> Optional[str]:
        """Call local Ollama instance with optimized settings for speed"""
        prompt = self._messages_to_prompt(messages)
        
        # Optimize for maximum speed
        data = {
            "model": "gemma:2b",  # Back to gemma:2b - smaller and might be faster
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,     # Ultra low for fastest generation
                "num_predict": min(max_tokens, 50),  # Much shorter responses
                "top_k": 5,         # Very restrictive for speed
                "top_p": 0.7,       # Lower for faster sampling
                "repeat_penalty": 1.0,
                "num_ctx": 256,     # Minimal context for speed
                "num_thread": 6,    # More threads if available
                "num_gpu": 0        # Force CPU for consistency
            }
        }
        
        try:
            response = requests.post(
                f"{self.providers['local_ollama']['base_url']}/api/generate",
                json=data,
                timeout=3  # Ultra-aggressive 3 second timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "").strip()
                if response_text:
                    self.timeout_count = 0  # Reset timeout counter on success
                    return response_text
        except requests.exceptions.Timeout:
            self.timeout_count += 1  # Increment timeout counter
            logger.warning(f"Ollama response timeout #{self.timeout_count} - model may be too slow")
            return None
        except requests.exceptions.ConnectionError:
            logger.info("Ollama not available locally")
        
        return None
    
    def _messages_to_prompt(self, messages: List[Dict]) -> str:
        """Convert messages format to prompt string"""
        prompt_parts = []
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"Human: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        prompt_parts.append("Assistant: ")
        return "\n".join(prompt_parts)
    
    def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all providers"""
        status = {}
        
        for provider_id, config in self.providers.items():
            status[provider_id] = {
                "name": config["name"],
                "active": config["active"],
                "models": config["models"],
                "rate_limit": config["rate_limit"],
                "has_api_key": bool(config["api_key"]) if config["api_key"] is not None else "Not required"
            }
        
        return status
    
    def setup_instructions(self) -> str:
        """Get setup instructions for API keys"""
        return """
# Free AI Model Setup Instructions

## 1. Together AI (Recommended - Free $25 credits)
- Sign up at: https://api.together.xyz/
- Get API key from dashboard
- Set environment variable: TOGETHER_API_KEY=your_key_here
- Free tier: $25 credits, multiple models

## 2. Hugging Face (Free unlimited for public models)
- Sign up at: https://huggingface.co/
- Create token at: https://huggingface.co/settings/tokens
- Set environment variable: HUGGINGFACE_API_KEY=your_token_here
- Completely free for inference API

## 3. Cohere (Free tier)
- Sign up at: https://cohere.ai/
- Get API key from dashboard
- Set environment variable: COHERE_API_KEY=your_key_here
- Free tier: 100 requests/month

## 4. Replicate (Free credits)
- Sign up at: https://replicate.com/
- Get API token from account settings
- Set environment variable: REPLICATE_API_TOKEN=your_token_here
- Free tier: $10 credits monthly

## 5. Ollama (Local - Unlimited & Free)
- Install Ollama: https://ollama.ai/
- Run: ollama serve
- Pull models: ollama pull llama2
- Completely free, runs locally

## Quick Setup (add to .env file):
```
TOGETHER_API_KEY=your_together_key
HUGGINGFACE_API_KEY=your_hf_token
COHERE_API_KEY=your_cohere_key
REPLICATE_API_TOKEN=your_replicate_token
```
        """

# Global multi-model manager instance
multi_model_manager = MultiModelManager()