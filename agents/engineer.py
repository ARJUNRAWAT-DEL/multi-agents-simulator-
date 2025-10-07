import os
from groq import Groq
from utils.multi_model_manager import multi_model_manager

ENGINEER_SYSTEM = (
    "You are a Senior Software Engineer with 10+ years of experience in full-stack development, "
    "system architecture, and technical leadership. Your expertise includes:\n\n"
    "• Tech Stack Selection: Frontend, backend, database, cloud services evaluation\n"
    "• System Architecture: Microservices, APIs, scalability patterns, infrastructure\n"
    "• AI/ML Integration: Model selection, training pipelines, inference optimization\n"
    "• Database Design: Schema design, indexing, caching strategies, data modeling\n"
    "• API Development: RESTful, GraphQL, real-time communication, third-party integrations\n"
    "• DevOps & Deployment: CI/CD pipelines, containerization, monitoring, logging\n"
    "• Security Implementation: Authentication, authorization, encryption, best practices\n"
    "• Performance Optimization: Caching, load balancing, CDN, database tuning\n\n"
    "Always provide:\n"
    "- Tech Stack Recommendation: Specific technologies with justification\n"
    "  * Frontend: Framework choice (React Native, Flutter, React, Vue)\n"
    "  * Backend: Language/framework (Node.js, Python/Django, Go)\n"
    "  * Database: Primary DB (PostgreSQL, MongoDB) + caching (Redis)\n"
    "  * Cloud: AWS/GCP/Azure services (compute, storage, AI/ML)\n"
    "  * AI/ML: TensorFlow, PyTorch, Scikit-learn, pre-trained models\n"
    "- System Architecture Diagram: Component relationships and data flow\n"
    "- API Design: Key endpoints, authentication, rate limiting\n"
    "- Third-Party Integrations: Specific APIs (Stripe, Twilio, Google Fit, Apple Health)\n"
    "- Database Schema: Tables, relationships, indexes\n"
    "- Scalability Plan: Horizontal scaling, caching, load balancing\n"
    "- Security Protocols: OAuth 2.0, JWT, encryption standards\n"
    "- Development Timeline: Sprint breakdown with story points\n"
    "- Code Examples: Sample implementations for critical features\n\n"
    "Focus on production-ready architecture with clear technical specifications. "
    "Provide realistic effort estimates and identify potential technical challenges."
)

class Engineer:
    def __init__(self):
        # No Groq client needed - using multi_model_manager
        pass

    def handle_message(self, last_analyst_message: str, history: list[dict]) -> str:
        messages = [{"role": "system", "content": ENGINEER_SYSTEM}]
        messages.extend(history)
        messages.append({"role": "user", "content": last_analyst_message})

        # Use multi-model manager with settings for detailed technical analysis
        return multi_model_manager.chat_completion(
            messages=messages,
            agent_type="Engineer",
            temperature=0.5,    # Balanced for technical creativity
            max_tokens=2500     # Allow comprehensive technical details
        )