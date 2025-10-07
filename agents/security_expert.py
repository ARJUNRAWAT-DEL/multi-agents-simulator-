import os
from utils.multi_model_manager import multi_model_manager

SECURITY_EXPERT_SYSTEM = (
    "You are a Cybersecurity Expert. Be concise and security-focused:\n"
    "• Security threats and vulnerabilities\n"
    "• Authentication and authorization\n"
    "• Data encryption and protection\n"
    "• Compliance (SOC 2, ISO 27001, HIPAA)\n"
    "Keep responses under 150 words for speed."
)

class SecurityExpert:
    def __init__(self):
        pass  # No API client needed - using multi_model_manager

    def handle_message(self, context_message: str, history: list[dict]) -> str:
        messages = [{"role": "system", "content": SECURITY_EXPERT_SYSTEM}]
        messages.extend(history)
        messages.append({"role": "user", "content": context_message})

        # Use multi-model manager with ultra-optimized settings for speed
        return multi_model_manager.chat_completion(
            messages=messages,
            agent_type="SecurityExpert",
            temperature=0.1,
            max_tokens=50
        )
