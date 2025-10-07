import os
from utils.multi_model_manager import multi_model_manager

LEGAL_COMPLIANCE_SYSTEM = (
    "You are a Legal Compliance Officer. Be concise and risk-focused:\n"
    "• Regulatory requirements (GDPR, SOX, PCI, industry-specific)\n"
    "• Legal risks and mitigation\n"
    "• Compliance timeline and costs\n"
    "• Critical documentation needed\n"
    "Keep responses under 150 words for speed."
)

class LegalComplianceAgent:
    def __init__(self):
        pass  # No API client needed - using multi_model_manager

    def handle_message(self, context_message: str, history: list[dict]) -> str:
        messages = [{"role": "system", "content": LEGAL_COMPLIANCE_SYSTEM}]
        messages.extend(history)
        messages.append({"role": "user", "content": context_message})

        # Use multi-model manager with ultra-optimized settings for speed
        return multi_model_manager.chat_completion(
            messages=messages,
            agent_type="LegalCompliance",
            temperature=0.1,
            max_tokens=50
        )
