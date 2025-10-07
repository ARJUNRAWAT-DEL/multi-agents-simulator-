"""
Deliverable Templates for Multi-Agent System
Generates professional documents from agent collaboration
"""

class DeliverableGenerator:
    @staticmethod
    def generate_prd(project_name: str, agent_outputs: dict) -> str:
        """Generate Product Requirements Document"""
        prd = f"""
# Product Requirements Document (PRD)
## {project_name}

---

## 1. Executive Summary

{agent_outputs.get('ProductManager', {}).get('executive_summary', 'TBD')}

**Target Launch Date:** {agent_outputs.get('ProductManager', {}).get('launch_date', 'Q2 2026')}
**Initial Investment Required:** {agent_outputs.get('FinancialAnalyst', {}).get('funding', '$250K-500K')}

---

## 2. Problem Statement

### User Pain Points
{agent_outputs.get('ProductManager', {}).get('problem_statement', 'TBD')}

### Market Opportunity
- **Market Size (TAM):** {agent_outputs.get('Analyst', {}).get('tam', '$X billion')}
- **Growth Rate (CAGR):** {agent_outputs.get('Analyst', {}).get('cagr', 'XX%')}
- **Target Market (SAM):** {agent_outputs.get('Analyst', {}).get('sam', '$X million')}

---

## 3. Target Users

### Primary Personas
{agent_outputs.get('UXDesigner', {}).get('personas', 'TBD')}

### User Segmentation
{agent_outputs.get('Analyst', {}).get('segments', 'TBD')}

---

## 4. Product Vision & Strategy

### Vision Statement
{agent_outputs.get('ProductManager', {}).get('vision', 'TBD')}

### Competitive Positioning
{agent_outputs.get('Analyst', {}).get('positioning', 'TBD')}

### Key Differentiators
{agent_outputs.get('ProductManager', {}).get('differentiators', 'TBD')}

---

## 5. Product Roadmap

### Phase 1: MVP (Months 1-3)
{agent_outputs.get('ProductManager', {}).get('mvp_features', 'TBD')}

### Phase 2: Growth (Months 4-6)
{agent_outputs.get('ProductManager', {}).get('phase2_features', 'TBD')}

### Phase 3: Scale (Months 7-12)
{agent_outputs.get('ProductManager', {}).get('phase3_features', 'TBD')}

---

## 6. Feature Specifications

### Must-Have Features (MVP)
{agent_outputs.get('ProductManager', {}).get('must_have', 'TBD')}

### Should-Have Features (Phase 2)
{agent_outputs.get('ProductManager', {}).get('should_have', 'TBD')}

### Nice-to-Have Features (Future)
{agent_outputs.get('ProductManager', {}).get('nice_to_have', 'TBD')}

---

## 7. User Experience Design

### User Flows
{agent_outputs.get('UXDesigner', {}).get('user_flows', 'TBD')}

### Wireframes & Mockups
{agent_outputs.get('UXDesigner', {}).get('wireframes', 'TBD')}

### Design System
{agent_outputs.get('UXDesigner', {}).get('design_system', 'TBD')}

---

## 8. Technical Architecture

### Tech Stack
{agent_outputs.get('Engineer', {}).get('tech_stack', 'TBD')}

### System Architecture
{agent_outputs.get('TechnicalArchitect', {}).get('architecture', 'TBD')}

### AI/ML Components
{agent_outputs.get('DataScientist', {}).get('ml_models', 'TBD')}

### Third-Party Integrations
{agent_outputs.get('Engineer', {}).get('integrations', 'TBD')}

---

## 9. Success Metrics & KPIs

### Product Metrics
- **DAU/MAU Ratio:** {agent_outputs.get('ProductManager', {}).get('dau_mau', '> 30%')}
- **Retention Rate (30-day):** {agent_outputs.get('ProductManager', {}).get('retention', '> 40%')}
- **Churn Rate:** {agent_outputs.get('ProductManager', {}).get('churn', '< 5%')}
- **NPS Score:** {agent_outputs.get('ProductManager', {}).get('nps', '> 50')}

### Business Metrics
- **Monthly Revenue:** {agent_outputs.get('FinancialAnalyst', {}).get('mrr', 'TBD')}
- **CAC:** {agent_outputs.get('MarketingStrategist', {}).get('cac', 'TBD')}
- **LTV:** {agent_outputs.get('FinancialAnalyst', {}).get('ltv', 'TBD')}
- **LTV:CAC Ratio:** {agent_outputs.get('FinancialAnalyst', {}).get('ltv_cac', '> 3:1')}

---

## 10. Go-to-Market Strategy

### Launch Plan
{agent_outputs.get('MarketingStrategist', {}).get('launch_plan', 'TBD')}

### Marketing Channels
{agent_outputs.get('MarketingStrategist', {}).get('channels', 'TBD')}

### Budget Allocation
{agent_outputs.get('MarketingStrategist', {}).get('marketing_budget', 'TBD')}

---

## 11. Financial Projections

### Revenue Model
{agent_outputs.get('FinancialAnalyst', {}).get('revenue_model', 'TBD')}

### 5-Year Projections
{agent_outputs.get('FinancialAnalyst', {}).get('projections', 'TBD')}

### Break-Even Analysis
{agent_outputs.get('FinancialAnalyst', {}).get('breakeven', 'TBD')}

---

## 12. Legal & Compliance

### Regulatory Requirements
{agent_outputs.get('LegalCompliance', {}).get('regulations', 'TBD')}

### Data Privacy
{agent_outputs.get('LegalCompliance', {}).get('privacy', 'TBD')}

---

## 13. Security

### Security Architecture
{agent_outputs.get('SecurityExpert', {}).get('security_framework', 'TBD')}

### Threat Mitigation
{agent_outputs.get('SecurityExpert', {}).get('threats', 'TBD')}

---

## 14. Operations

### Operational Plan
{agent_outputs.get('OperationsDirector', {}).get('ops_plan', 'TBD')}

### Resource Requirements
{agent_outputs.get('OperationsDirector', {}).get('resources', 'TBD')}

---

## 15. Risks & Mitigation

### Key Risks
{agent_outputs.get('Analyst', {}).get('risks', 'TBD')}

### Mitigation Strategies
{agent_outputs.get('ProductManager', {}).get('risk_mitigation', 'TBD')}

---

## 16. Next Steps

### Immediate Actions (Week 1-2)
1. Finalize product specifications
2. Assemble core team
3. Set up development environment
4. Create detailed project plan

### Short-Term (Month 1-2)
1. Complete MVP development
2. Conduct user testing
3. Iterate based on feedback
4. Prepare for beta launch

### Medium-Term (Month 3-6)
1. Public launch
2. Marketing campaign execution
3. Feature expansion
4. Scale operations

---

**Document Version:** 1.0
**Last Updated:** {agent_outputs.get('timestamp', 'Date TBD')}
**Status:** Draft
"""
        return prd

    @staticmethod
    def generate_executive_summary(project_name: str, agent_outputs: dict) -> str:
        """Generate Executive Summary"""
        summary = f"""
# Executive Summary
## {project_name}

---

## 🎯 Opportunity

{agent_outputs.get('Analyst', {}).get('opportunity', 'TBD')}

**Market Size:** {agent_outputs.get('Analyst', {}).get('market_size', '$X billion')}
**Target Users:** {agent_outputs.get('ProductManager', {}).get('target_users', 'TBD')}

---

## 💡 Solution

{agent_outputs.get('ProductManager', {}).get('solution', 'TBD')}

**Key Features:**
{agent_outputs.get('ProductManager', {}).get('key_features', 'TBD')}

---

## 🎨 User Experience

{agent_outputs.get('UXDesigner', {}).get('ux_summary', 'TBD')}

---

## 💻 Technology

**Tech Stack:** {agent_outputs.get('Engineer', {}).get('stack_summary', 'TBD')}
**AI/ML:** {agent_outputs.get('DataScientist', {}).get('ml_summary', 'TBD')}

---

## 📈 Go-to-Market

{agent_outputs.get('MarketingStrategist', {}).get('gtm_summary', 'TBD')}

**Customer Acquisition Cost (CAC):** {agent_outputs.get('MarketingStrategist', {}).get('cac', '$XX')}
**Expected LTV:CAC Ratio:** {agent_outputs.get('FinancialAnalyst', {}).get('ltv_cac', 'X:1')}

---

## 💰 Financial Outlook

**Initial Investment:** {agent_outputs.get('FinancialAnalyst', {}).get('investment', '$XXX,XXX')}
**Year 1 Revenue:** {agent_outputs.get('FinancialAnalyst', {}).get('year1_revenue', '$XXX,XXX')}
**Break-Even:** {agent_outputs.get('FinancialAnalyst', {}).get('breakeven', 'Month XX')}

---

## ⚠️ Key Risks

1. {agent_outputs.get('Analyst', {}).get('risk1', 'TBD')}
2. {agent_outputs.get('Analyst', {}).get('risk2', 'TBD')}
3. {agent_outputs.get('Analyst', {}).get('risk3', 'TBD')}

---

## 🚀 Recommendation

{agent_outputs.get('ProductManager', {}).get('recommendation', 'Proceed with MVP development')}

"""
        return summary

    @staticmethod
    def generate_tech_proposal(project_name: str, agent_outputs: dict) -> str:
        """Generate Technical Proposal"""
        proposal = f"""
# Technical Proposal
## {project_name}

---

## 1. System Architecture

{agent_outputs.get('TechnicalArchitect', {}).get('architecture_diagram', 'TBD')}

---

## 2. Technology Stack

### Frontend
{agent_outputs.get('Engineer', {}).get('frontend', 'TBD')}

### Backend
{agent_outputs.get('Engineer', {}).get('backend', 'TBD')}

### Database
{agent_outputs.get('Engineer', {}).get('database', 'TBD')}

### Cloud Infrastructure
{agent_outputs.get('Engineer', {}).get('cloud', 'TBD')}

### AI/ML Infrastructure
{agent_outputs.get('DataScientist', {}).get('ml_infrastructure', 'TBD')}

---

## 3. AI/ML Models

{agent_outputs.get('DataScientist', {}).get('model_details', 'TBD')}

---

## 4. API Design

{agent_outputs.get('Engineer', {}).get('api_design', 'TBD')}

---

## 5. Security Implementation

{agent_outputs.get('SecurityExpert', {}).get('security_implementation', 'TBD')}

---

## 6. Scalability Strategy

{agent_outputs.get('TechnicalArchitect', {}).get('scalability', 'TBD')}

---

## 7. Development Timeline

{agent_outputs.get('Engineer', {}).get('timeline', 'TBD')}

---

## 8. Technical Risks

{agent_outputs.get('Engineer', {}).get('tech_risks', 'TBD')}

---

## 9. Infrastructure Costs

{agent_outputs.get('Engineer', {}).get('infrastructure_costs', 'TBD')}

"""
        return proposal

    @staticmethod
    def generate_marketing_plan(project_name: str, agent_outputs: dict) -> str:
        """Generate Marketing Launch Plan"""
        plan = f"""
# Marketing Launch Plan
## {project_name}

---

## 1. Brand Positioning

{agent_outputs.get('MarketingStrategist', {}).get('positioning', 'TBD')}

---

## 2. Target Audience

{agent_outputs.get('MarketingStrategist', {}).get('audience_segments', 'TBD')}

---

## 3. Marketing Channels

{agent_outputs.get('MarketingStrategist', {}).get('channel_strategy', 'TBD')}

---

## 4. Content Strategy

{agent_outputs.get('MarketingStrategist', {}).get('content_plan', 'TBD')}

---

## 5. Launch Campaign

{agent_outputs.get('MarketingStrategist', {}).get('launch_campaign', 'TBD')}

---

## 6. Influencer Strategy

{agent_outputs.get('MarketingStrategist', {}).get('influencer_strategy', 'TBD')}

---

## 7. Paid Advertising

{agent_outputs.get('MarketingStrategist', {}).get('paid_ads', 'TBD')}

---

## 8. Marketing Budget

{agent_outputs.get('MarketingStrategist', {}).get('budget_breakdown', 'TBD')}

---

## 9. Performance Metrics

{agent_outputs.get('MarketingStrategist', {}).get('kpis', 'TBD')}

"""
        return plan
