"""
Enterprise AI Agent Consortium - Analytics Engine
Advanced analytics for conversation quality, sentiment analysis, and business insights
"""

import re
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import numpy as np
from collections import Counter

@dataclass
class AnalyticsResult:
    """Container for analytics results"""
    sentiment_score: float
    confidence_score: float
    quality_score: float
    key_topics: List[str]
    technical_complexity: float
    business_value: float
    risk_factors: List[str]
    success_probability: float
    recommendations: List[str]

class ConversationAnalytics:
    """Advanced analytics for conversation analysis"""
    
    def __init__(self):
        # Business and technical keywords
        self.business_keywords = {
            'revenue', 'profit', 'market', 'customer', 'growth', 'roi', 'monetization',
            'strategy', 'competitive', 'value', 'pricing', 'sales', 'marketing', 'brand'
        }
        
        self.technical_keywords = {
            'architecture', 'database', 'api', 'framework', 'scalability', 'security',
            'performance', 'integration', 'deployment', 'cloud', 'microservices', 'infrastructure'
        }
        
        self.risk_keywords = {
            'challenge', 'risk', 'difficult', 'complex', 'uncertain', 'problem',
            'limitation', 'constraint', 'barrier', 'obstacle', 'threat', 'vulnerability'
        }
        
        self.positive_keywords = {
            'excellent', 'great', 'strong', 'effective', 'successful', 'optimal',
            'innovative', 'competitive', 'valuable', 'efficient', 'robust', 'scalable'
        }
        
        self.negative_keywords = {
            'poor', 'weak', 'ineffective', 'problematic', 'risky', 'challenging',
            'limited', 'difficult', 'expensive', 'slow', 'complex', 'uncertain'
        }
    
    def analyze_conversation(self, conversation: List[Dict], report: str) -> AnalyticsResult:
        """Comprehensive conversation analysis"""
        
        # Combine all text for analysis
        all_text = " ".join([msg.get('content', '') for msg in conversation]) + " " + (report or "")
        
        # Perform various analyses
        sentiment = self._analyze_sentiment(all_text)
        confidence = self._calculate_confidence(conversation)
        quality = self._assess_quality(conversation, report)
        topics = self._extract_topics(all_text)
        tech_complexity = self._assess_technical_complexity(all_text)
        business_value = self._assess_business_value(all_text)
        risks = self._identify_risk_factors(all_text)
        success_prob = self._calculate_success_probability(sentiment, confidence, quality, business_value)
        recommendations = self._generate_recommendations(sentiment, quality, tech_complexity, business_value)
        
        return AnalyticsResult(
            sentiment_score=sentiment,
            confidence_score=confidence,
            quality_score=quality,
            key_topics=topics,
            technical_complexity=tech_complexity,
            business_value=business_value,
            risk_factors=risks,
            success_probability=success_prob,
            recommendations=recommendations
        )
    
    def _analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment polarity (-1 to 1)"""
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in self.positive_keywords)
        negative_count = sum(1 for word in words if word in self.negative_keywords)
        
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words == 0:
            return 0.0
        
        sentiment = (positive_count - negative_count) / total_sentiment_words
        return max(-1.0, min(1.0, sentiment))
    
    def _calculate_confidence(self, conversation: List[Dict]) -> float:
        """Calculate confidence based on conversation depth and detail"""
        if not conversation:
            return 0.0
        
        # Factors affecting confidence
        message_count = len(conversation)
        avg_message_length = np.mean([len(msg.get('content', '')) for msg in conversation])
        agent_diversity = len(set(msg.get('agent_type', 'unknown') for msg in conversation))
        
        # Normalize factors
        message_factor = min(1.0, message_count / 10)  # Ideal around 10 messages
        length_factor = min(1.0, avg_message_length / 500)  # Ideal around 500 chars
        diversity_factor = min(1.0, agent_diversity / 3)  # Ideal 3+ different agents
        
        confidence = (message_factor * 0.4 + length_factor * 0.3 + diversity_factor * 0.3)
        return round(confidence, 2)
    
    def _assess_quality(self, conversation: List[Dict], report: str) -> float:
        """Assess overall conversation quality"""
        if not conversation and not report:
            return 0.0
        
        all_text = " ".join([msg.get('content', '') for msg in conversation]) + " " + (report or "")
        
        # Quality indicators
        specificity = self._measure_specificity(all_text)
        completeness = self._measure_completeness(all_text)
        actionability = self._measure_actionability(all_text)
        
        quality = (specificity * 0.3 + completeness * 0.4 + actionability * 0.3)
        return round(quality, 2)
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract key topics from text"""
        # Simple keyword-based topic extraction
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = Counter(words)
        
        # Filter out common words and extract meaningful topics
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
        meaningful_words = [word for word, freq in word_freq.most_common(20) 
                          if len(word) > 3 and word not in stop_words and freq > 1]
        
        return meaningful_words[:8]  # Return top 8 topics
    
    def _assess_technical_complexity(self, text: str) -> float:
        """Assess technical complexity of the project"""
        words = text.lower().split()
        tech_word_count = sum(1 for word in words if word in self.technical_keywords)
        
        # Also look for technical patterns
        patterns = [
            r'\b\w+\s+(architecture|framework|database|api)\b',
            r'\b(micro)?services?\b',
            r'\bcloud\s+\w+\b',
            r'\b\w+\s+integration\b'
        ]
        
        pattern_matches = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in patterns)
        
        # Normalize to 0-1 scale
        total_words = len(words)
        if total_words == 0:
            return 0.0
        
        complexity = min(1.0, (tech_word_count + pattern_matches * 2) / (total_words * 0.1))
        return round(complexity, 2)
    
    def _assess_business_value(self, text: str) -> float:
        """Assess business value and commercial potential"""
        words = text.lower().split()
        business_word_count = sum(1 for word in words if word in self.business_keywords)
        
        # Look for value indicators
        value_patterns = [
            r'\$[\d,]+',  # Dollar amounts
            r'\b\d+%\s+(growth|increase|improvement)\b',
            r'\b(roi|return|profit|revenue)\b',
            r'\b(market\s+size|target\s+market)\b'
        ]
        
        value_matches = sum(len(re.findall(pattern, text, re.IGNORECASE)) for pattern in value_patterns)
        
        total_words = len(words)
        if total_words == 0:
            return 0.0
        
        business_value = min(1.0, (business_word_count + value_matches * 3) / (total_words * 0.1))
        return round(business_value, 2)
    
    def _identify_risk_factors(self, text: str) -> List[str]:
        """Identify potential risk factors"""
        risks = []
        
        # Technical risks
        if any(word in text.lower() for word in ['scalability', 'performance', 'security']):
            risks.append("Technical scalability and performance considerations")
        
        # Market risks
        if any(word in text.lower() for word in ['competitive', 'market', 'competition']):
            risks.append("Competitive market dynamics")
        
        # Resource risks
        if any(word in text.lower() for word in ['budget', 'timeline', 'resource']):
            risks.append("Resource and timeline constraints")
        
        # Regulatory risks
        if any(word in text.lower() for word in ['compliance', 'regulation', 'legal']):
            risks.append("Regulatory and compliance requirements")
        
        return risks[:5]  # Return top 5 risks
    
    def _calculate_success_probability(self, sentiment: float, confidence: float, 
                                     quality: float, business_value: float) -> float:
        """Calculate overall success probability"""
        # Convert sentiment from -1,1 to 0,1 scale
        normalized_sentiment = (sentiment + 1) / 2
        
        # Weighted combination
        success_prob = (
            normalized_sentiment * 0.2 +
            confidence * 0.3 +
            quality * 0.3 +
            business_value * 0.2
        )
        
        return round(success_prob, 2)
    
    def _generate_recommendations(self, sentiment: float, quality: float, 
                                tech_complexity: float, business_value: float) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if quality < 0.6:
            recommendations.append("Conduct deeper analysis with additional agent rounds")
        
        if business_value < 0.5:
            recommendations.append("Strengthen business case with market research and financial projections")
        
        if tech_complexity > 0.7:
            recommendations.append("Consider phased implementation approach to manage technical complexity")
        
        if sentiment < 0:
            recommendations.append("Address identified concerns and risk factors before proceeding")
        
        if tech_complexity > 0.5 and business_value > 0.7:
            recommendations.append("High-value technical project - consider dedicated architecture review")
        
        # Default recommendations
        if not recommendations:
            recommendations.extend([
                "Proceed with detailed project planning and resource allocation",
                "Establish success metrics and monitoring framework",
                "Consider pilot or MVP approach for validation"
            ])
        
        return recommendations[:5]
    
    def _measure_specificity(self, text: str) -> float:
        """Measure how specific and detailed the content is"""
        # Look for specific indicators: numbers, percentages, proper nouns, technical terms
        numbers = len(re.findall(r'\b\d+\b', text))
        percentages = len(re.findall(r'\d+%', text))
        proper_nouns = len(re.findall(r'\b[A-Z][a-z]+\b', text))
        
        total_words = len(text.split())
        if total_words == 0:
            return 0.0
        
        specificity = min(1.0, (numbers + percentages * 2 + proper_nouns) / (total_words * 0.1))
        return specificity
    
    def _measure_completeness(self, text: str) -> float:
        """Measure how complete the analysis is"""
        # Check for key business analysis components
        components = [
            r'\b(market|target|customer|user)\b',
            r'\b(competition|competitor|competitive)\b',
            r'\b(technical|technology|architecture)\b',
            r'\b(timeline|schedule|milestone)\b',
            r'\b(budget|cost|price|financial)\b',
            r'\b(risk|challenge|mitigation)\b'
        ]
        
        covered_components = sum(1 for pattern in components 
                               if re.search(pattern, text, re.IGNORECASE))
        
        completeness = covered_components / len(components)
        return completeness
    
    def _measure_actionability(self, text: str) -> float:
        """Measure how actionable the recommendations are"""
        # Look for action-oriented language
        action_patterns = [
            r'\b(implement|develop|create|build|design)\b',
            r'\b(should|must|need to|recommend)\b',
            r'\b(next steps?|action items?)\b',
            r'\b(phase \d+|step \d+|milestone)\b'
        ]
        
        action_words = sum(len(re.findall(pattern, text, re.IGNORECASE)) 
                          for pattern in action_patterns)
        
        total_words = len(text.split())
        if total_words == 0:
            return 0.0
        
        actionability = min(1.0, action_words / (total_words * 0.05))
        return actionability

# Global analytics engine instance
analytics_engine = ConversationAnalytics()