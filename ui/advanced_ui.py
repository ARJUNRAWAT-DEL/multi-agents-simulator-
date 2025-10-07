"""
Advanced UI/UX System for Enterprise AI Agent Consortium
Handles theming, responsive design, and progressive web app features
"""

import streamlit as st
from typing import Dict, Any

class ThemeManager:
    """Manages light/dark themes and custom styling"""
    
    def __init__(self):
        self.themes = {
            "light": {
                "primary_color": "#3b82f6",
                "secondary_color": "#1e40af",
                "background_color": "#ffffff",
                "secondary_background": "#f8fafc",
                "text_color": "#1f2937",
                "border_color": "#e5e7eb",
                "accent_color": "#0ea5e9"
            },
            "dark": {
                "primary_color": "#60a5fa",
                "secondary_color": "#3b82f6",
                "background_color": "#0f172a",
                "secondary_background": "#1e293b",
                "text_color": "#f1f5f9",
                "border_color": "#374151",
                "accent_color": "#06b6d4"
            }
        }
    
    def get_theme_css(self, theme_name: str = "light") -> str:
        """Generate CSS for the selected theme"""
        theme = self.themes.get(theme_name, self.themes["light"])
        
        return f"""
        <style>
        /* Root variables for theming */
        :root {{
            --primary-color: {theme["primary_color"]};
            --secondary-color: {theme["secondary_color"]};
            --background-color: {theme["background_color"]};
            --secondary-background: {theme["secondary_background"]};
            --text-color: {theme["text_color"]};
            --border-color: {theme["border_color"]};
            --accent-color: {theme["accent_color"]};
        }}
        
        /* Main container styling */
        .main-header {{
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }}
        
        .main-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='10' cy='10' r='2'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
            opacity: 0.3;
        }}
        
        .main-header h1 {{
            color: white;
            text-align: center;
            margin: 0;
            font-weight: 700;
            font-size: 2.5rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.2);
            position: relative;
            z-index: 2;
        }}
        
        .main-header p {{
            color: rgba(255,255,255,0.9);
            text-align: center;
            margin-top: 0.5rem;
            font-size: 1.2rem;
            font-weight: 300;
            position: relative;
            z-index: 2;
        }}
        
        /* Professional card styling */
        .professional-card {{
            background: var(--secondary-background);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
            position: relative;
        }}
        
        .professional-card:hover {{
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }}
        
        .agent-card {{
            background: linear-gradient(135deg, var(--secondary-background) 0%, var(--background-color) 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid var(--primary-color);
            margin: 0.75rem 0;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            transition: all 0.3s ease;
        }}
        
        .agent-card:hover {{
            border-left-width: 6px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.12);
        }}
        
        .metric-card {{
            background: linear-gradient(135deg, var(--accent-color), var(--primary-color));
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: scale(1.05);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }}
        
        /* Enhanced button styling */
        .stButton > button {{
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 2rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        }}
        
        .stButton > button:active {{
            transform: translateY(0);
        }}
        
        /* Sidebar styling */
        .css-1d391kg {{
            background: var(--secondary-background);
            border-right: 1px solid var(--border-color);
        }}
        
        /* Progress bar styling */
        .stProgress > div > div > div > div {{
            background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
            border-radius: 10px;
        }}
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            background: var(--secondary-background);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.5rem 1rem;
            color: var(--text-color);
            font-weight: 500;
        }}
        
        .stTabs [aria-selected="true"] {{
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }}
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {{
            .main-header h1 {{
                font-size: 1.8rem;
            }}
            
            .main-header p {{
                font-size: 1rem;
            }}
            
            .professional-card {{
                padding: 1rem;
                margin: 0.5rem 0;
            }}
            
            .agent-card {{
                padding: 1rem;
                margin: 0.5rem 0;
            }}
        }}
        
        /* Dark theme specific adjustments */
        [data-theme="dark"] {{
            color-scheme: dark;
        }}
        
        [data-theme="dark"] .stApp {{
            background-color: var(--background-color);
            color: var(--text-color);
        }}
        
        /* Animation classes */
        .fade-in {{
            animation: fadeIn 0.5s ease-in;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .slide-in {{
            animation: slideIn 0.6s ease-out;
        }}
        
        @keyframes slideIn {{
            from {{ transform: translateX(-100px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        
        /* Loading animations */
        .loading-spinner {{
            border: 3px solid var(--border-color);
            border-top: 3px solid var(--primary-color);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }}
        
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
        
        /* Professional status indicators */
        .status-online {{
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #10b981;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }}
        
        .status-processing {{
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #f59e0b;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }}
            70% {{ box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
        }}
        
        /* Enhanced form styling */
        .stTextInput > div > div > input {{
            border-radius: 8px;
            border: 2px solid var(--border-color);
            transition: border-color 0.3s ease;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}
        
        .stSelectbox > div > div > div {{
            border-radius: 8px;
            border: 2px solid var(--border-color);
        }}
        
        /* Professional toast notifications */
        .success-toast {{
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        }}
        
        .error-toast {{
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
        }}
        
        .warning-toast {{
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: white;
            padding: 1rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        }}
        </style>
        """

class ResponsiveLayout:
    """Handles responsive design and mobile optimization"""
    
    @staticmethod
    def get_device_type():
        """Determine device type based on viewport"""
        # This would be enhanced with JavaScript in a real implementation
        return "desktop"  # Placeholder
    
    @staticmethod
    def get_responsive_columns(desktop_cols: list, mobile_cols: list = None):
        """Return responsive column configuration"""
        device = ResponsiveLayout.get_device_type()
        if device == "mobile" and mobile_cols:
            return mobile_cols
        return desktop_cols

class PWAManager:
    """Progressive Web App features"""
    
    @staticmethod
    def generate_manifest():
        """Generate PWA manifest"""
        return {
            "name": "Enterprise AI Agent Consortium",
            "short_name": "AI Agents",
            "description": "Advanced Multi-Agent Collaboration Platform",
            "start_url": "/",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#3b82f6",
            "icons": [
                {
                    "src": "/static/icon-192.png",
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": "/static/icon-512.png",
                    "sizes": "512x512",
                    "type": "image/png"
                }
            ]
        }
    
    @staticmethod
    def get_pwa_meta_tags():
        """Generate PWA meta tags"""
        return """
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <meta name="theme-color" content="#3b82f6">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="default">
        <meta name="apple-mobile-web-app-title" content="AI Agents">
        <meta name="description" content="Advanced Multi-Agent Collaboration Platform for Strategic Product Development">
        <meta name="keywords" content="AI, agents, collaboration, product development, enterprise">
        
        <!-- PWA Icons -->
        <link rel="apple-touch-icon" href="/static/icon-192.png">
        <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
        <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">
        <link rel="manifest" href="/static/manifest.json">
        """

class UIComponents:
    """Reusable UI components with professional styling"""
    
    @staticmethod
    def render_professional_header(title: str, subtitle: str, theme: str = "light"):
        """Render professional header with theme support"""
        theme_manager = ThemeManager()
        css = theme_manager.get_theme_css(theme)
        
        st.markdown(css, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="main-header fade-in">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_metric_card(title: str, value: str, delta: str = None, icon: str = "📊"):
        """Render professional metric card"""
        delta_html = f"<div style='font-size: 0.9rem; margin-top: 0.5rem;'>Δ {delta}</div>" if delta else ""
        
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
            <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.25rem;">{title}</div>
            <div style="font-size: 2rem; font-weight: 700;">{value}</div>
            {delta_html}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_agent_status_card(agent_name: str, status: str, description: str):
        """Render agent status card"""
        status_icon = "🟢" if status == "active" else "🟡" if status == "processing" else "⚪"
        status_class = "status-online" if status == "active" else "status-processing"
        
        st.markdown(f"""
        <div class="agent-card slide-in">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <span class="{status_class}"></span>
                <strong style="font-size: 1.1rem;">{agent_name}</strong>
                <span style="margin-left: auto; font-size: 1.2rem;">{status_icon}</span>
            </div>
            <div style="color: #6b7280; font-size: 0.9rem;">{description}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_loading_animation(message: str = "Processing..."):
        """Render professional loading animation"""
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem;">
            <div class="loading-spinner"></div>
            <div style="margin-top: 1rem; color: #6b7280; font-weight: 500;">{message}</div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_toast_notification(message: str, type: str = "success"):
        """Render toast notification"""
        toast_class = f"{type}-toast"
        icon = "✅" if type == "success" else "❌" if type == "error" else "⚠️"
        
        st.markdown(f"""
        <div class="{toast_class} fade-in">
            <span style="margin-right: 0.5rem; font-size: 1.2rem;">{icon}</span>
            {message}
        </div>
        """, unsafe_allow_html=True)

# Global instances
theme_manager = ThemeManager()
responsive_layout = ResponsiveLayout()
pwa_manager = PWAManager()
ui_components = UIComponents()