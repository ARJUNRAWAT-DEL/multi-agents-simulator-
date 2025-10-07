"""
Enterprise AI Agent Consortium - Executive Dashboard
Interactive dashboards with advanced visualizations and analytics
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class ExecutiveDashboard:
    """Create interactive executive dashboards and visualizations"""
    
    def __init__(self):
        self.colors = {
            'primary': '#3b82f6',
            'secondary': '#64748b',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'info': '#06b6d4'
        }
    
    def render_main_dashboard(self, session_data: Dict, analytics: Optional[Dict] = None):
        """Render the main executive dashboard"""
        
        st.markdown("## 📊 Executive Dashboard")
        
        # Key metrics row
        self._render_key_metrics(session_data, analytics)
        
        # Charts row
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_success_probability_gauge(analytics)
            self._render_agent_participation_chart(session_data)
        
        with col2:
            self._render_complexity_analysis(analytics)
            self._render_sentiment_timeline(session_data)
        
        # Additional analytics
        self._render_detailed_analytics(analytics)
    
    def _render_key_metrics(self, session_data: Dict, analytics: Optional[Dict]):
        """Render key performance indicators"""
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            success_prob = analytics.get('success_probability', 0) * 100 if analytics else 0
            st.metric(
                "Success Probability",
                f"{success_prob:.1f}%",
                delta=f"{success_prob - 70:.1f}%" if success_prob > 0 else None
            )
        
        with col2:
            quality = analytics.get('quality_score', 0) * 100 if analytics else 0
            st.metric(
                "Analysis Quality",
                f"{quality:.1f}%",
                delta=f"{quality - 80:.1f}%" if quality > 0 else None
            )
        
        with col3:
            business_value = analytics.get('business_value', 0) * 100 if analytics else 0
            st.metric(
                "Business Value",
                f"{business_value:.1f}%",
                delta=f"{business_value - 60:.1f}%" if business_value > 0 else None
            )
        
        with col4:
            complexity = analytics.get('technical_complexity', 0) * 100 if analytics else 0
            st.metric(
                "Technical Complexity",
                f"{complexity:.1f}%",
                delta=f"{complexity - 50:.1f}%" if complexity > 0 else None,
                delta_color="inverse"
            )
        
        with col5:
            message_count = session_data.get('total_messages', 0)
            st.metric(
                "Total Messages",
                message_count,
                delta=f"{message_count - 8}" if message_count > 0 else None
            )
    
    def _render_success_probability_gauge(self, analytics: Optional[Dict]):
        """Render success probability as a gauge chart"""
        
        st.subheader("🎯 Success Probability")
        
        if not analytics:
            st.info("No analytics data available")
            return
        
        value = analytics.get('success_probability', 0) * 100
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Success %"},
            delta = {'reference': 70},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': self.colors['primary']},
                'steps': [
                    {'range': [0, 40], 'color': self.colors['danger']},
                    {'range': [40, 70], 'color': self.colors['warning']},
                    {'range': [70, 100], 'color': self.colors['success']}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_agent_participation_chart(self, session_data: Dict):
        """Render agent participation pie chart"""
        
        st.subheader("👥 Agent Participation")
        
        agents = session_data.get('selected_agents', {})
        if not any(agents.values()):
            st.info("No agent data available")
            return
        
        # Create participation data
        active_agents = [agent for agent, active in agents.items() if active]
        
        # Simulate participation percentages (in real app, get from conversation history)
        participation_data = {}
        total = 100
        for i, agent in enumerate(active_agents):
            if i == len(active_agents) - 1:
                participation_data[agent] = total
            else:
                pct = np.random.randint(15, 25)
                participation_data[agent] = pct
                total -= pct
        
        fig = px.pie(
            values=list(participation_data.values()),
            names=list(participation_data.keys()),
            title="Message Distribution by Agent",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_complexity_analysis(self, analytics: Optional[Dict]):
        """Render complexity analysis radar chart"""
        
        st.subheader("🔬 Complexity Analysis")
        
        if not analytics:
            st.info("No analytics data available")
            return
        
        # Create radar chart data
        categories = [
            'Technical<br>Complexity',
            'Business<br>Value',
            'Quality<br>Score',
            'Success<br>Probability',
            'Confidence<br>Level'
        ]
        
        values = [
            analytics.get('technical_complexity', 0) * 100,
            analytics.get('business_value', 0) * 100,
            analytics.get('quality_score', 0) * 100,
            analytics.get('success_probability', 0) * 100,
            analytics.get('confidence_score', 0) * 100
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Current Project',
            line_color=self.colors['primary']
        ))
        
        # Add benchmark line
        benchmark = [60, 70, 80, 75, 85]
        fig.add_trace(go.Scatterpolar(
            r=benchmark,
            theta=categories,
            fill='toself',
            name='Industry Benchmark',
            line_color=self.colors['secondary'],
            opacity=0.6
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_sentiment_timeline(self, session_data: Dict):
        """Render sentiment analysis over conversation timeline"""
        
        st.subheader("📈 Sentiment Timeline")
        
        # Simulate sentiment data over conversation rounds
        rounds = session_data.get('rounds', 2)
        timeline_data = []
        
        for round_num in range(1, rounds + 1):
            # Simulate sentiment progression
            base_sentiment = 0.3 + (round_num * 0.2)  # Generally improving
            noise = np.random.normal(0, 0.1)
            sentiment = max(-1, min(1, base_sentiment + noise))
            
            timeline_data.append({
                'Round': f'Round {round_num}',
                'Sentiment': sentiment,
                'Confidence': np.random.uniform(0.7, 0.95)
            })
        
        if not timeline_data:
            st.info("No timeline data available")
            return
        
        df = pd.DataFrame(timeline_data)
        
        fig = go.Figure()
        
        # Add sentiment line
        fig.add_trace(go.Scatter(
            x=df['Round'],
            y=df['Sentiment'],
            mode='lines+markers',
            name='Sentiment',
            line=dict(color=self.colors['primary'], width=3),
            marker=dict(size=8)
        ))
        
        # Add confidence bars
        fig.add_trace(go.Bar(
            x=df['Round'],
            y=df['Confidence'],
            name='Confidence',
            yaxis='y2',
            opacity=0.3,
            marker_color=self.colors['info']
        ))
        
        fig.update_layout(
            title="Sentiment and Confidence by Round",
            xaxis_title="Conversation Round",
            yaxis_title="Sentiment Score",
            yaxis2=dict(
                title="Confidence Level",
                overlaying='y',
                side='right',
                range=[0, 1]
            ),
            height=300,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_detailed_analytics(self, analytics: Optional[Dict]):
        """Render detailed analytics section"""
        
        if not analytics:
            return
        
        st.markdown("---")
        st.subheader("🔍 Detailed Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Key topics word cloud simulation
            st.markdown("**Key Topics**")
            topics = analytics.get('key_topics', [])
            if topics:
                # Create a simple topic frequency chart
                topic_freq = {topic: np.random.randint(5, 20) for topic in topics[:8]}
                
                fig = px.bar(
                    x=list(topic_freq.values()),
                    y=list(topic_freq.keys()),
                    orientation='h',
                    title="Topic Frequency",
                    color=list(topic_freq.values()),
                    color_continuous_scale="Blues"
                )
                fig.update_layout(height=300, showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No topics identified")
        
        with col2:
            # Risk assessment matrix
            st.markdown("**Risk Assessment**")
            risks = analytics.get('risk_factors', [])
            if risks:
                # Create risk impact vs probability matrix
                risk_data = []
                for risk in risks[:5]:
                    risk_data.append({
                        'Risk': risk[:30] + "..." if len(risk) > 30 else risk,
                        'Probability': np.random.uniform(0.2, 0.8),
                        'Impact': np.random.uniform(0.3, 0.9),
                        'Severity': np.random.choice(['Low', 'Medium', 'High'])
                    })
                
                df_risks = pd.DataFrame(risk_data)
                
                fig = px.scatter(
                    df_risks,
                    x='Probability',
                    y='Impact',
                    size=[10] * len(df_risks),
                    color='Severity',
                    hover_data=['Risk'],
                    title="Risk Impact vs Probability",
                    color_discrete_map={
                        'Low': self.colors['success'],
                        'Medium': self.colors['warning'],
                        'High': self.colors['danger']
                    }
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No risks identified")
    
    def render_project_comparison(self, projects: List[Dict]):
        """Render project comparison dashboard"""
        
        st.subheader("📊 Project Portfolio Comparison")
        
        if not projects:
            st.info("No projects available for comparison")
            return
        
        # Create comparison data
        comparison_data = []
        for project in projects:
            comparison_data.append({
                'Project': project.get('name', 'Unnamed'),
                'Success Probability': project.get('success_probability', 0) * 100,
                'Business Value': project.get('business_value', 0) * 100,
                'Technical Complexity': project.get('technical_complexity', 0) * 100,
                'Quality Score': project.get('quality_score', 0) * 100,
                'Industry': project.get('industry', 'Unknown')
            })
        
        df = pd.DataFrame(comparison_data)
        
        # Multi-metric comparison chart
        fig = go.Figure()
        
        metrics = ['Success Probability', 'Business Value', 'Technical Complexity', 'Quality Score']
        
        for i, project in enumerate(df['Project'].unique()):
            project_data = df[df['Project'] == project]
            fig.add_trace(go.Radar(
                r=[project_data[metric].iloc[0] for metric in metrics],
                theta=metrics,
                fill='toself',
                name=project
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Multi-Project Comparison"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Project ranking table
        st.subheader("📋 Project Rankings")
        
        # Calculate overall scores
        df['Overall Score'] = (
            df['Success Probability'] * 0.3 +
            df['Business Value'] * 0.3 +
            df['Quality Score'] * 0.2 +
            (100 - df['Technical Complexity']) * 0.2  # Lower complexity is better
        )
        
        df_sorted = df.sort_values('Overall Score', ascending=False)
        
        # Format for display
        display_df = df_sorted[['Project', 'Industry', 'Overall Score', 'Success Probability', 'Business Value']].copy()
        display_df['Overall Score'] = display_df['Overall Score'].round(1)
        display_df['Success Probability'] = display_df['Success Probability'].round(1).astype(str) + '%'
        display_df['Business Value'] = display_df['Business Value'].round(1).astype(str) + '%'
        
        st.dataframe(display_df, use_container_width=True)

# Global dashboard instance
dashboard = ExecutiveDashboard()