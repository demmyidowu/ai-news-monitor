import json
from datetime import datetime
import logging
import re

class NotebookLMScriptGenerator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def create_notebooklm_script(self, articles, output_path=None):
        """Create a comprehensive script optimized for NotebookLM podcast generation"""
        
        if output_path is None:
            date_str = datetime.now().strftime('%Y%m%d')
            output_path = f"outputs/NotebookLM_Script_{date_str}.md"
        
        # Categorize articles
        categories = self._categorize_articles(articles)
        
        # Build comprehensive script
        script = self._build_comprehensive_script(categories, articles)
        
        # Save script
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(script)
        
        self.logger.info(f"✅ NotebookLM script saved to: {output_path}")
        
        # Also create a summary document for context
        summary_path = output_path.replace('Script', 'Summary').replace('.md', '.txt')
        self._create_summary_document(articles, summary_path)
        
        return output_path, summary_path
    
    def _categorize_articles(self, articles):
        """Enhanced categorization for better podcast flow"""
        categories = {
            'breaking': [],      # Major announcements & breaking news
            'research': [],      # Academic papers and studies  
            'industry': [],      # Company news and products
            'policy': [],        # Regulation and governance
            'trends': [],        # Market trends and analysis
            'tools': [],         # New tools and applications
            'funding': [],       # Investment and funding news
            'people': []         # Leadership changes, interviews
        }
        
        for article in articles:
            text = (article['title'] + ' ' + article.get('summary', '')).lower()
            priority = article.get('priority_level', 'Medium')
            
            # Categorize based on content and priority
            if priority == 'Critical' or any(kw in text for kw in ['breaking', 'announces', 'launches', 'releases', 'unveils']):
                categories['breaking'].append(article)
            elif any(kw in text for kw in ['arxiv', 'research', 'paper', 'study', 'academic', 'university']):
                categories['research'].append(article)
            elif any(kw in text for kw in ['funding', 'investment', 'raises', 'series', 'valuation', 'ipo']):
                categories['funding'].append(article)
            elif any(kw in text for kw in ['regulation', 'policy', 'law', 'ethics', 'governance', 'government']):
                categories['policy'].append(article)
            elif any(kw in text for kw in ['trend', 'market', 'analysis', 'forecast', 'prediction', 'outlook']):
                categories['trends'].append(article)
            elif any(kw in text for kw in ['tool', 'app', 'platform', 'api', 'framework', 'library']):
                categories['tools'].append(article)
            elif any(kw in text for kw in ['ceo', 'cto', 'founder', 'hire', 'joins', 'interview', 'appoint']):
                categories['people'].append(article)
            else:
                categories['industry'].append(article)
        
        return categories
    
    def _build_comprehensive_script(self, categories, all_articles):
        """Build a rich, conversational script for NotebookLM"""
        
        date_str = datetime.now().strftime('%B %d, %Y')
        total_articles = len(all_articles)
        
        script = f"""# AI Industry Weekly Podcast Script
**Date:** {date_str}
**Total Stories Covered:** {total_articles}

## Podcast Overview
This week's AI industry update covers major developments across artificial intelligence, machine learning, and emerging technologies. We'll explore breakthrough research, significant company announcements, policy developments, and market trends that are shaping the future of AI.

---

## Executive Summary

### Key Themes This Week:
"""
        
        # Add thematic overview
        for category, articles in categories.items():
            if articles:
                count = len(articles)
                script += f"- **{category.title()}**: {count} major development{'s' if count > 1 else ''}\n"
        
        script += f"\n### Market Context\n"
        script += f"The AI industry continues its rapid evolution with {total_articles} significant developments this week. "
        
        # Add high-level insights
        critical_count = len(categories.get('breaking', []))
        research_count = len(categories.get('research', []))
        
        if critical_count > 0:
            script += f"Notably, we saw {critical_count} major announcement{'s' if critical_count != 1 else ''} that could reshape the industry. "
        
        if research_count > 0:
            script += f"From the research front, {research_count} significant breakthrough{'s' if research_count != 1 else ''} emerged from leading institutions. "
        
        script += "Let's dive into the details.\n\n---\n\n"
        
        # Add detailed sections
        section_order = ['breaking', 'research', 'industry', 'funding', 'tools', 'policy', 'trends', 'people']
        section_titles = {
            'breaking': '🚨 Breaking News & Major Announcements',
            'research': '🔬 Research Breakthroughs & Academic Developments', 
            'industry': '🏢 Industry News & Company Updates',
            'funding': '💰 Investment & Funding News',
            'tools': '🛠️ New Tools & Platforms',
            'policy': '📋 Policy, Ethics & Regulation',
            'trends': '📈 Market Trends & Analysis',
            'people': '👥 Leadership & People News'
        }
        
        for category in section_order:
            articles = categories.get(category, [])
            if not articles:
                continue
                
            script += f"## {section_titles[category]}\n\n"
            
            # Add section context
            script += self._get_section_context(category, len(articles))
            script += "\n\n"
            
            # Add articles with rich context
            for i, article in enumerate(articles[:8], 1):  # Limit to top 8 per section
                script += self._format_article_for_script(article, i, category)
                script += "\n"
            
            script += "---\n\n"
        
        # Add conclusion and analysis
        script += self._build_conclusion_section(categories, all_articles)
        
        return script
    
    def _get_section_context(self, category, count):
        """Get contextual introduction for each section"""
        contexts = {
            'breaking': f"This week brought {count} major announcement{'s' if count != 1 else ''} that are already making waves across the AI industry. These developments represent significant shifts in capabilities, market positioning, and technological advancement.",
            
            'research': f"The academic and research community published {count} notable development{'s' if count != 1 else ''} this week. These findings provide crucial insights into the future direction of AI technology and its underlying scientific foundations.",
            
            'industry': f"Corporate developments dominated headlines with {count} significant update{'s' if count != 1 else ''} from major tech companies. These moves signal important strategic shifts and competitive positioning in the AI landscape.",
            
            'funding': f"The investment landscape saw {count} noteworthy development{'s' if count != 1 else ''} this week, reflecting continued confidence in AI innovation and market potential.",
            
            'tools': f"Developers and practitioners gained access to {count} new tool{'s' if count != 1 else ''} and platform{'s' if count != 1 else ''} this week, expanding the practical applications of AI technology.",
            
            'policy': f"Regulatory and ethical considerations took center stage with {count} important development{'s' if count != 1 else ''} in AI governance and policy formation.",
            
            'trends': f"Market analysis revealed {count} significant trend{'s' if count != 1 else ''} shaping the broader AI ecosystem and its future trajectory.",
            
            'people': f"Leadership changes and key personnel moves made news with {count} important announcement{'s' if count != 1 else ''} across the industry."
        }
        
        return contexts.get(category, f"This section covers {count} important development{'s' if count != 1 else ''} in {category}.")
    
    def _format_article_for_script(self, article, index, category):
        """Format individual articles with rich context for engaging discussion"""
        
        title = article.get('title', 'Untitled Article')
        source = article.get('source', 'Unknown Source')
        summary = article.get('summary', '')
        priority = article.get('priority_level', 'Medium')
        
        # Clean title and summary
        clean_title = re.sub(r'^\d+\.\s*', '', title)  # Remove numbering
        clean_title = re.sub(r'[🔥⭐]', '', clean_title)  # Remove emojis
        
        script_section = f"### {index}. {clean_title}\n\n"
        
        # Add priority indicator and context
        priority_context = {
            'Critical': '**🚨 CRITICAL DEVELOPMENT**',
            'High': '**⭐ HIGH IMPACT**',
            'Medium': '**📢 NOTABLE**',
            'Low': '**📋 UPDATE**'
        }
        
        if priority in priority_context:
            script_section += f"{priority_context[priority]}\n\n"
        
        # Add source context
        script_section += f"**Source:** {source}\n\n"
        
        # Add rich summary and discussion points
        if summary:
            # Clean summary
            clean_summary = summary.replace('Summary:', '').strip()
            if clean_summary:
                script_section += f"**Key Details:** {clean_summary}\n\n"
        
        # Add discussion prompts based on category
        discussion_prompts = self._get_discussion_prompts(category, clean_title, summary)
        if discussion_prompts:
            script_section += f"**Discussion Points:**\n{discussion_prompts}\n\n"
        
        # Add industry implications
        implications = self._get_implications(category, clean_title, priority)
        if implications:
            script_section += f"**Industry Implications:** {implications}\n\n"
        
        return script_section
    
    def _get_discussion_prompts(self, category, title, summary):
        """Generate relevant discussion prompts for NotebookLM hosts"""
        
        title_lower = title.lower()
        summary_lower = (summary or '').lower()
        
        prompts = {
            'breaking': [
                "- What makes this announcement particularly significant for the AI industry?",
                "- How might this impact existing market players and competitive dynamics?",
                "- What are the potential implications for developers and end users?"
            ],
            'research': [
                "- What new possibilities does this research unlock?",
                "- How might this advance translate into practical applications?",
                "- What are the broader scientific implications of these findings?"
            ],
            'industry': [
                "- What strategic motivations might be driving this move?",
                "- How does this fit into the company's broader AI strategy?",
                "- What signal does this send to the market and competitors?"
            ],
            'funding': [
                "- What does this investment say about market confidence in AI?",
                "- How might this funding accelerate development in this space?",
                "- What trends does this reflect in AI investment patterns?"
            ]
        }
        
        base_prompts = prompts.get(category, [
            "- What are the key implications of this development?",
            "- How might this impact the broader AI ecosystem?",
            "- What should industry watchers pay attention to next?"
        ])
        
        return '\n'.join(base_prompts)
    
    def _get_implications(self, category, title, priority):
        """Generate industry implications for discussion"""
        
        implications = {
            'Critical': "This development has the potential to significantly reshape competitive dynamics and market positioning across the AI industry.",
            'High': "This represents an important shift that industry participants should monitor closely for strategic implications.",
            'Medium': "This development contributes to ongoing trends and may influence future industry direction.",
            'Low': "While incremental, this update reflects broader patterns in AI industry evolution."
        }
        
        return implications.get(priority, "This development adds to the evolving AI landscape and merits industry attention.")
    
    def _build_conclusion_section(self, categories, all_articles):
        """Build comprehensive conclusion with analysis and forward-looking insights"""
        
        conclusion = "## Weekly Analysis & Looking Ahead\n\n"
        
        conclusion += "### Key Takeaways\n\n"
        
        # Synthesize major themes
        if categories.get('breaking'):
            conclusion += "**Major Announcements:** This week's breakthrough announcements signal accelerating innovation and intensifying competition in the AI space. The pace of development continues to exceed industry expectations.\n\n"
        
        if categories.get('research'):
            conclusion += "**Research Progress:** Academic and research developments this week demonstrate continued advancement in AI capabilities and our understanding of these systems. These findings will likely influence practical applications in the coming months.\n\n"
        
        if categories.get('funding'):
            conclusion += "**Investment Climate:** Funding activity reflects sustained investor confidence in AI innovation, with particular interest in practical applications and enterprise solutions.\n\n"
        
        if categories.get('policy'):
            conclusion += "**Regulatory Environment:** Policy developments indicate growing attention to AI governance and ethical considerations, which will increasingly shape industry practices.\n\n"
        
        conclusion += "### Industry Implications\n\n"
        conclusion += "The developments covered this week reflect several important trends:\n\n"
        conclusion += "- **Acceleration:** The pace of AI innovation continues to accelerate across research, development, and deployment\n"
        conclusion += "- **Democratization:** New tools and platforms are making AI capabilities more accessible to broader audiences\n"
        conclusion += "- **Maturation:** The industry is showing signs of maturation with increased focus on practical applications and governance\n"
        conclusion += "- **Competition:** Competitive dynamics are intensifying as major players vie for market position\n\n"
        
        conclusion += "### What to Watch Next Week\n\n"
        conclusion += "Based on this week's developments, here are key areas to monitor:\n\n"
        conclusion += "- Follow-up announcements and product releases from major AI companies\n"
        conclusion += "- Market reactions and competitive responses to breakthrough developments\n"
        conclusion += "- Academic publications building on this week's research findings\n"
        conclusion += "- Policy responses to emerging AI capabilities and applications\n"
        conclusion += "- Investment and funding activity in emerging AI sectors\n\n"
        
        conclusion += "### Conclusion\n\n"
        conclusion += f"This week's {len(all_articles)} developments underscore the dynamic nature of the AI industry. "
        conclusion += "From breakthrough research to major corporate announcements, the pace of change continues to accelerate. "
        conclusion += "As AI capabilities expand and mature, we're seeing increased focus on practical applications, "
        conclusion += "ethical considerations, and competitive positioning.\n\n"
        conclusion += "The industry remains in a period of rapid evolution, with each week bringing significant "
        conclusion += "developments that shape the future of artificial intelligence and its impact on society.\n\n"
        
        return conclusion
    
    def _create_summary_document(self, articles, output_path):
        """Create a concise summary document for NotebookLM context"""
        
        date_str = datetime.now().strftime('%B %d, %Y')
        
        summary = f"""AI Industry Weekly Summary - {date_str}

OVERVIEW
========
This document summarizes {len(articles)} key developments in artificial intelligence from the past week.

MAJOR DEVELOPMENTS
==================
"""
        
        # Sort by priority and add top stories
        sorted_articles = sorted(articles, 
                               key=lambda x: (x.get('relevance_score', 0), x.get('published', '')), 
                               reverse=True)
        
        for i, article in enumerate(sorted_articles[:15], 1):  # Top 15 stories
            summary += f"\n{i}. {article.get('title', 'Untitled')}\n"
            summary += f"   Source: {article.get('source', 'Unknown')}\n"
            if article.get('summary'):
                clean_summary = article['summary'].replace('Summary:', '').strip()
                summary += f"   Details: {clean_summary}\n"
            if article.get('priority_level'):
                summary += f"   Priority: {article['priority_level']}\n"
        
        # Add category breakdown
        categories = self._categorize_articles(articles)
        summary += f"\n\nCATEGORY BREAKDOWN\n==================\n"
        
        for category, cat_articles in categories.items():
            if cat_articles:
                summary += f"{category.title()}: {len(cat_articles)} stories\n"
        
        # Save summary
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        self.logger.info(f"✅ NotebookLM summary document saved to: {output_path}")

# Integration function
def create_notebooklm_assets(articles_data):
    """Create both script and summary for NotebookLM"""
    
    generator = NotebookLMScriptGenerator()
    
    print("📝 Creating NotebookLM-optimized assets...")
    
    script_path, summary_path = generator.create_notebooklm_script(articles_data)
    
    print(f"✅ NotebookLM Script: {script_path}")
    print(f"✅ Summary Document: {summary_path}")
    print("\n🎙️ Next steps:")
    print("1. Upload both files to NotebookLM")
    print("2. Click 'Generate Podcast' in NotebookLM")
    print("3. Enjoy your AI-generated conversational podcast!")
    
    return script_path, summary_path

if __name__ == "__main__":
    # Test with existing data
    import json
    from datetime import datetime
    
    date_str = datetime.now().strftime('%Y%m%d')
    data_file = f"data/articles_{date_str}.json"
    
    try:
        with open(data_file, 'r') as f:
            articles = json.load(f)
        create_notebooklm_assets(articles)
    except FileNotFoundError:
        print(f"No articles file found at {data_file}")
        print("Run your AI news collector first: python main.py")