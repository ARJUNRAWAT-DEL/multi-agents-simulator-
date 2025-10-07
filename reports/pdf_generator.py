"""
Enterprise AI Agent Consortium - PDF Report Generator
Professional PDF report generation with templates, charts, and branding
"""

import io
from datetime import datetime
from typing import Dict, List, Optional
import base64

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.platypus import Image as RLImage
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.colors import HexColor, black, white, blue, grey
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics.charts.piecharts import Pie
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class PDFReportGenerator:
    """Generate professional PDF reports for agent conversations"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet() if REPORTLAB_AVAILABLE else None
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        if not REPORTLAB_AVAILABLE:
            return
            
        # Custom styles for professional documents
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=HexColor('#1e3a8a'),
            alignment=1  # Center
        )
        
        self.heading_style = ParagraphStyle(
            'CustomHeading',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            textColor=HexColor('#3b82f6'),
            leftIndent=0
        )
        
        self.subheading_style = ParagraphStyle(
            'CustomSubHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            textColor=HexColor('#1d4ed8'),
            leftIndent=10
        )
        
        self.body_style = ParagraphStyle(
            'CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            leftIndent=0,
            alignment=0  # Left
        )
        
        self.highlight_style = ParagraphStyle(
            'Highlight',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=6,
            backColor=HexColor('#f0f9ff'),
            borderColor=HexColor('#3b82f6'),
            borderWidth=1,
            leftIndent=10,
            rightIndent=10,
            topPadding=8,
            bottomPadding=8
        )
    
    def generate_executive_report(self, session_data: Dict, conversation: List[Dict], 
                                report: str, analytics: Optional[Dict] = None) -> bytes:
        """Generate comprehensive executive report PDF"""
        if not REPORTLAB_AVAILABLE:
            raise ImportError("ReportLab is required for PDF generation. Install with: pip install reportlab")
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch)
        
        story = []
        
        # Title page
        story.extend(self._create_title_page(session_data))
        story.append(PageBreak())
        
        # Executive summary
        story.extend(self._create_executive_summary(session_data, report, analytics))
        story.append(PageBreak())
        
        # Project overview
        story.extend(self._create_project_overview(session_data))
        
        # Analytics and insights
        if analytics:
            story.extend(self._create_analytics_section(analytics))
            story.append(PageBreak())
        
        # Detailed conversation analysis
        story.extend(self._create_conversation_analysis(conversation))
        story.append(PageBreak())
        
        # Recommendations and next steps
        story.extend(self._create_recommendations_section(analytics, report))
        
        # Appendices
        story.extend(self._create_appendix(session_data, conversation))
        
        doc.build(story)
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
    
    def _create_title_page(self, session_data: Dict) -> List:
        """Create professional title page"""
        elements = []
        
        # Main title
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph("ENTERPRISE AI AGENT CONSORTIUM", self.title_style))
        elements.append(Spacer(1, 0.5*inch))
        
        # Subtitle
        subtitle_style = ParagraphStyle(
            'Subtitle',
            fontSize=18,
            textColor=HexColor('#64748b'),
            alignment=1
        )
        elements.append(Paragraph("Strategic Product Development Analysis", subtitle_style))
        elements.append(Spacer(1, 1*inch))
        
        # Project information
        project_info = [
            ["Project:", session_data.get('project_title', 'Untitled Project')],
            ["Industry:", session_data.get('industry', 'Technology')],
            ["Category:", session_data.get('project_type', 'Software Development')],
            ["Analysis Date:", datetime.now().strftime("%B %d, %Y")],
            ["Report Type:", session_data.get('output_format', 'Executive Summary')]
        ]
        
        table = Table(project_info, colWidths=[2*inch, 4*inch])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TEXTCOLOR', (0, 0), (0, -1), HexColor('#374151')),
            ('TEXTCOLOR', (1, 0), (1, -1), HexColor('#111827')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        elements.append(table)
        
        elements.append(Spacer(1, 2*inch))
        
        # Footer
        footer_style = ParagraphStyle(
            'Footer',
            fontSize=10,
            textColor=HexColor('#6b7280'),
            alignment=1
        )
        elements.append(Paragraph("Generated by Enterprise AI Agent Consortium", footer_style))
        elements.append(Paragraph("Confidential Business Analysis", footer_style))
        
        return elements
    
    def _create_executive_summary(self, session_data: Dict, report: str, analytics: Optional[Dict]) -> List:
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.heading_style))
        elements.append(Spacer(1, 12))
        
        # Key metrics table if analytics available
        if analytics:
            metrics_data = [
                ["Metric", "Score", "Interpretation"],
                ["Success Probability", f"{analytics.get('success_probability', 0)*100:.1f}%", 
                 self._interpret_score(analytics.get('success_probability', 0))],
                ["Technical Complexity", f"{analytics.get('technical_complexity', 0)*100:.1f}%",
                 self._interpret_complexity(analytics.get('technical_complexity', 0))],
                ["Business Value", f"{analytics.get('business_value', 0)*100:.1f}%",
                 self._interpret_business_value(analytics.get('business_value', 0))],
                ["Quality Score", f"{analytics.get('quality_score', 0)*100:.1f}%",
                 self._interpret_quality(analytics.get('quality_score', 0))]
            ]
            
            metrics_table = Table(metrics_data, colWidths=[2*inch, 1*inch, 2.5*inch])
            metrics_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f3f4f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#111827')),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#d1d5db')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(metrics_table)
            elements.append(Spacer(1, 20))
        
        # Main report content
        if report:
            # Split report into paragraphs and format
            paragraphs = report.split('\n\n')
            for para in paragraphs[:3]:  # First 3 paragraphs for summary
                if para.strip():
                    elements.append(Paragraph(para.strip(), self.body_style))
                    elements.append(Spacer(1, 6))
        
        return elements
    
    def _create_project_overview(self, session_data: Dict) -> List:
        """Create project overview section"""
        elements = []
        
        elements.append(Paragraph("PROJECT OVERVIEW", self.heading_style))
        elements.append(Spacer(1, 12))
        
        # Project details
        elements.append(Paragraph("Project Description", self.subheading_style))
        elements.append(Paragraph(session_data.get('project_description', 'No description available'), 
                                self.body_style))
        elements.append(Spacer(1, 12))
        
        # Configuration details
        elements.append(Paragraph("Analysis Configuration", self.subheading_style))
        
        config_data = [
            ["Parameter", "Value"],
            ["Selected Agents", ", ".join([k for k, v in session_data.get('selected_agents', {}).items() if v])],
            ["Analysis Rounds", str(session_data.get('rounds', 2))],
            ["AI Model", session_data.get('model_used', 'llama-3.3-70b-versatile')],
            ["Duration", f"{session_data.get('duration_seconds', 0)} seconds"],
            ["Total Messages", str(session_data.get('total_messages', 0))]
        ]
        
        config_table = Table(config_data, colWidths=[2*inch, 3*inch])
        config_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f3f4f6')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(config_table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_analytics_section(self, analytics: Dict) -> List:
        """Create analytics and insights section"""
        elements = []
        
        elements.append(Paragraph("ANALYTICS & INSIGHTS", self.heading_style))
        elements.append(Spacer(1, 12))
        
        # Key topics
        if analytics.get('key_topics'):
            elements.append(Paragraph("Key Topics Identified", self.subheading_style))
            topics_text = "• " + "\n• ".join(analytics['key_topics'][:8])
            elements.append(Paragraph(topics_text, self.body_style))
            elements.append(Spacer(1, 12))
        
        # Risk factors
        if analytics.get('risk_factors'):
            elements.append(Paragraph("Risk Factors", self.subheading_style))
            risks_text = "• " + "\n• ".join(analytics['risk_factors'])
            elements.append(Paragraph(risks_text, self.highlight_style))
            elements.append(Spacer(1, 12))
        
        # Recommendations
        if analytics.get('recommendations'):
            elements.append(Paragraph("Key Recommendations", self.subheading_style))
            recs_text = "• " + "\n• ".join(analytics['recommendations'])
            elements.append(Paragraph(recs_text, self.body_style))
            elements.append(Spacer(1, 12))
        
        return elements
    
    def _create_conversation_analysis(self, conversation: List[Dict]) -> List:
        """Create detailed conversation analysis"""
        elements = []
        
        elements.append(Paragraph("AGENT COLLABORATION ANALYSIS", self.heading_style))
        elements.append(Spacer(1, 12))
        
        # Agent participation summary
        agent_counts = {}
        for msg in conversation:
            agent = msg.get('agent_type', 'Unknown')
            agent_counts[agent] = agent_counts.get(agent, 0) + 1
        
        if agent_counts:
            elements.append(Paragraph("Agent Participation", self.subheading_style))
            
            participation_data = [["Agent", "Messages", "Contribution %"]]
            total_messages = sum(agent_counts.values())
            
            for agent, count in sorted(agent_counts.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total_messages) * 100 if total_messages > 0 else 0
                participation_data.append([agent, str(count), f"{percentage:.1f}%"])
            
            participation_table = Table(participation_data, colWidths=[2*inch, 1*inch, 1*inch])
            participation_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f3f4f6')),
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, HexColor('#d1d5db')),
            ]))
            elements.append(participation_table)
            elements.append(Spacer(1, 20))
        
        return elements
    
    def _create_recommendations_section(self, analytics: Optional[Dict], report: str) -> List:
        """Create recommendations and next steps section"""
        elements = []
        
        elements.append(Paragraph("RECOMMENDATIONS & NEXT STEPS", self.heading_style))
        elements.append(Spacer(1, 12))
        
        if analytics and analytics.get('recommendations'):
            elements.append(Paragraph("Strategic Recommendations", self.subheading_style))
            for i, rec in enumerate(analytics['recommendations'], 1):
                elements.append(Paragraph(f"{i}. {rec}", self.body_style))
                elements.append(Spacer(1, 6))
        
        # Implementation timeline (placeholder)
        elements.append(Spacer(1, 12))
        elements.append(Paragraph("Suggested Implementation Timeline", self.subheading_style))
        
        timeline_data = [
            ["Phase", "Duration", "Key Activities"],
            ["Phase 1: Planning", "2-4 weeks", "Requirements analysis, team formation, architecture design"],
            ["Phase 2: Development", "8-16 weeks", "Core development, testing, integration"],
            ["Phase 3: Launch", "2-4 weeks", "Deployment, monitoring, optimization"],
            ["Phase 4: Scale", "Ongoing", "Feature expansion, performance optimization"]
        ]
        
        timeline_table = Table(timeline_data, colWidths=[1.5*inch, 1*inch, 3*inch])
        timeline_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#f3f4f6')),
            ('GRID', (0, 0), (-1, -1), 1, HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(timeline_table)
        
        return elements
    
    def _create_appendix(self, session_data: Dict, conversation: List[Dict]) -> List:
        """Create appendix with technical details"""
        elements = []
        
        elements.append(PageBreak())
        elements.append(Paragraph("APPENDIX", self.heading_style))
        elements.append(Spacer(1, 12))
        
        # Technical specifications
        elements.append(Paragraph("A. Technical Specifications", self.subheading_style))
        tech_specs = [
            f"Analysis Engine: Enterprise AI Agent Consortium v1.0",
            f"AI Model: {session_data.get('model_used', 'llama-3.3-70b-versatile')}",
            f"Processing Date: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}",
            f"Session ID: {session_data.get('session_id', 'N/A')}",
            f"Total Processing Time: {session_data.get('duration_seconds', 0)} seconds"
        ]
        
        for spec in tech_specs:
            elements.append(Paragraph(spec, self.body_style))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _interpret_score(self, score: float) -> str:
        """Interpret success probability score"""
        if score >= 0.8:
            return "Excellent prospects"
        elif score >= 0.6:
            return "Good potential"
        elif score >= 0.4:
            return "Moderate risk"
        else:
            return "High risk"
    
    def _interpret_complexity(self, score: float) -> str:
        """Interpret technical complexity score"""
        if score >= 0.8:
            return "Highly complex"
        elif score >= 0.6:
            return "Moderately complex"
        elif score >= 0.4:
            return "Some complexity"
        else:
            return "Low complexity"
    
    def _interpret_business_value(self, score: float) -> str:
        """Interpret business value score"""
        if score >= 0.8:
            return "High commercial value"
        elif score >= 0.6:
            return "Good business case"
        elif score >= 0.4:
            return "Moderate value"
        else:
            return "Limited value"
    
    def _interpret_quality(self, score: float) -> str:
        """Interpret analysis quality score"""
        if score >= 0.8:
            return "Comprehensive analysis"
        elif score >= 0.6:
            return "Good coverage"
        elif score >= 0.4:
            return "Basic analysis"
        else:
            return "Needs more depth"

# Global PDF generator instance
pdf_generator = PDFReportGenerator() if REPORTLAB_AVAILABLE else None