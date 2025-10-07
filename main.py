import os
from agents.pm import ProductManager
from agents.analyst import Analyst
from agents.engineer import Engineer
from dotenv import load_dotenv

# Load .env API key
load_dotenv()

# Turn-based conversation simulation
def simulate_conversation(initial_instruction, turns=3):
    conversation_history = []

    # Initialize agents
    pm = ProductManager()
    analyst = Analyst()
    engineer = Engineer()

    # Step 1: PM starts
    pm_msg = pm.handle_message(initial_instruction, conversation_history)
    conversation_history.append({"role": "assistant", "content": pm_msg})

    for _ in range(turns - 1):
        # Step 2: Analyst responds
        analyst_msg = analyst.handle_message(pm_msg, conversation_history)
        conversation_history.append({"role": "assistant", "content": analyst_msg})

        # Step 3: Engineer responds
        engineer_msg = engineer.handle_message(analyst_msg, conversation_history)
        conversation_history.append({"role": "assistant", "content": engineer_msg})

        # Step 4: PM responds again (optional loop)
        pm_msg = pm.handle_message(engineer_msg, conversation_history)
        conversation_history.append({"role": "assistant", "content": pm_msg})

    return conversation_history


if __name__ == "__main__":
    INSTRUCTION = "We need to design a mobile app for plant fertilizer detection."
    convo = simulate_conversation(INSTRUCTION, turns=2)

    print("\n=== Conversation Transcript ===\n")
    for i, msg in enumerate(convo, 1):
        print(f"{i}. {msg['role'].title()}: {msg['content']}\n")
