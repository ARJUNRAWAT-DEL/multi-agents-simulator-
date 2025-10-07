import os
from utils.multi_model_manager import multi_model_manager

FINANCIAL_ANALYST_SYSTEM = (
    "You are a Senior Financial Analyst. Be concise and data-driven:\n"
    "• Financial projections (revenue, costs, cash flow)\n"
    "• ROI/IRR and break-even analysis\n"
    "• Capital requirements and funding strategy\n"
    "• Key metrics and benchmarking\n"
    "Keep responses under 150 words for speed."
)

class FinancialAnalyst:
    def __init__(self):
        pass  # No API client needed - using multi_model_manager

    def handle_message(self, context_message: str, history: list[dict]) -> str:
        messages = [{"role": "system", "content": FINANCIAL_ANALYST_SYSTEM}]
        messages.extend(history)
        messages.append({"role": "user", "content": context_message})

        # Use multi-model manager with ultra-optimized settings for speed
        return multi_model_manager.chat_completion(
            messages=messages,
            agent_type="FinancialAnalyst",
            temperature=0.1,
            max_tokens=50
        )