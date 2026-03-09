import os
from datetime import datetime
from typing import List
from sqlalchemy import select
from src.storage.connection import DatabaseConnection
from src.storage.models import ClusterDB, ArticleDB
from src.utils.logger import project_logger as logger

class MarkdownReportGenerator:
    """Generates human-readable Markdown reports from the database findings."""
    
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection
        self.reports_dir = "reports"
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_daily_report(self):
        """Fetches latest clusters and generates a Markdown file."""
        logger.info("Generating Daily Markdown Report...")
        
        with self.db_connection.get_session() as session:
            # Fetch clusters from today (simple date filter)
            today = datetime.utcnow().date()
            stmt = select(ClusterDB).order_by(ClusterDB.overall_bias.desc())
            clusters = session.scalars(stmt).all()
            
            if not clusters:
                logger.warning("No clusters found in database to generate report.")
                return

            report_content = self._build_markdown(clusters)
            
            timestamp = datetime.now().strftime("%Y-%m-%d")
            filename = f"DAILY_REPORT_{timestamp}.md"
            filepath = os.path.join(self.reports_dir, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report_content)
            
            # Also create a latest link
            latest_path = os.path.join(self.reports_dir, "LATEST_REPORT.md")
            with open(latest_path, "w", encoding="utf-8") as f:
                f.write(report_content)
                
            logger.success(f"Report generated successfully: {filepath}")

    def _build_markdown(self, clusters: List[ClusterDB]) -> str:
        """Constructs the Markdown string."""
        date_str = datetime.now().strftime("%B %d, %Y")
        
        md = f"# Unbiased India News - Daily Report\n"
        md += f"**Date:** {date_str}\n\n"
        md += "---\n\n"
        
        # Summary Table
        md += "## Executive Summary\n"
        md += "| Story | Bias Score | Sources | Status |\n"
        md += "| :--- | :---: | :---: | :--- |\n"
        
        for c in clusters:
            bias_emoji = "🟦" if c.overall_bias < -0.5 else "🟧" if c.overall_bias > 0.5 else "⬜"
            status = "🚩 BLINDSPOT" if c.is_blindspot else "✅ Balanced"
            md += f"| {c.main_event} | {bias_emoji} {c.overall_bias:.2f} | {len(c.articles)} | {status} |\n"
        
        md += "\n---\n\n"
        
        # Detailed Cluster Analysis
        md += "## Detailed Story Analysis\n\n"
        
        for c in clusters:
            md += f"### {c.main_event}\n"
            md += f"**Overall Bias Score:** {c.overall_bias:.2f} (-2 to +2)\n\n"
            
            md += "#### 📝 Summary\n"
            for bullet in c.summary_3_bullets:
                md += f"- {bullet}\n"
            
            if c.is_blindspot:
                md += f"\n> ⚠️ **Blindspot Detected:** This story shows significant ideological skew in its coverage spectrum.\n"
            
            md += "\n#### 🏢 Ownership & Framing Context\n"
            md += f"{c.reasoning_trace or 'No detailed reasoning trace available.'}\n\n"
            
            md += "#### 🔗 Sources in this Cluster\n"
            for art in c.articles:
                md += f"- [{art.source}]({art.link}) - {art.title}\n"
            
            md += "\n---\n\n"
            
        md += "\n*Generated automatically by Unbiased India News Pipeline.*"
        return md
