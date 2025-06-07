import feedparser
import json
import requests
from datetime import datetime, timedelta
import time
import logging

class AINewsCollector:
    def __init__(self, config_path="config/sources.json"):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def collect_rss_feeds(self, days_back=7):
        """Collect articles from RSS feeds from the last N days"""
        all_articles = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for feed_config in self.config['rss_feeds']:
            try:
                self.logger.info(f"Fetching from {feed_config['name']}")
                feed = feedparser.parse(feed_config['url'])
                
                for entry in feed.entries:
                    # Parse publish date
                    try:
                        published = datetime(*entry.published_parsed[:6])
                        if published < cutoff_date:
                            continue
                    except:
                        # If date parsing fails, include the article
                        published = datetime.now()
                    
                    article = {
                        'title': entry.title,
                        'link': entry.link,
                        'published': published.isoformat(),
                        'summary': getattr(entry, 'summary', ''),
                        'source': feed_config['name'],
                        'priority': feed_config['priority']
                    }
                    all_articles.append(article)
                
                # Be respectful - small delay between requests
                time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error fetching {feed_config['name']}: {e}")
        
        self.logger.info(f"Collected {len(all_articles)} articles")
        return all_articles
    
    def filter_relevant_articles(self, articles):
        """Enhanced filtering with priority scoring and categories"""
        keywords = [kw.lower() for kw in self.config['keywords']]
        high_priority_kw = [kw.lower() for kw in self.config.get('advanced_filters', {}).get('high_priority_keywords', [])]
        company_kw = [kw.lower() for kw in self.config.get('advanced_filters', {}).get('company_keywords', [])]
        exclude_kw = [kw.lower() for kw in self.config.get('advanced_filters', {}).get('exclude_keywords', [])]
        
        filtered_articles = []
        
        for article in articles:
            title_lower = article['title'].lower()
            summary_lower = article['summary'].lower()
            combined_text = title_lower + ' ' + summary_lower
            
            # Skip if contains excluded keywords
            if any(excl in combined_text for excl in exclude_kw):
                continue
            
            # Calculate relevance score
            title_score = sum(3 for kw in keywords if kw in title_lower)  # Title matches worth more
            summary_score = sum(1 for kw in keywords if kw in summary_lower)
            
            # Bonus points for high-priority keywords
            priority_bonus = sum(2 for kw in high_priority_kw if kw in combined_text)
            
            # Bonus for major companies
            company_bonus = sum(2 for kw in company_kw if kw in combined_text)
            
            # Source priority bonus
            source_bonus = 0
            if article.get('priority') == 'high':
                source_bonus = 2
            elif article.get('priority') == 'medium':
                source_bonus = 1
            
            total_score = title_score + summary_score + priority_bonus + company_bonus + source_bonus
            
            # Require minimum relevance (at least one keyword match or high priority source)
            if total_score >= 2 or article.get('priority') == 'high':
                article['relevance_score'] = total_score
                article['priority_level'] = self._determine_priority_level(total_score)
                filtered_articles.append(article)
        
        # Sort by relevance score and date
        filtered_articles.sort(
            key=lambda x: (x['relevance_score'], x['published']), 
            reverse=True
        )
        
        self.logger.info(f"Filtered to {len(filtered_articles)} relevant articles")
        return filtered_articles
    
    def _determine_priority_level(self, score):
        """Determine article priority based on relevance score"""
        if score >= 8:
            return "Critical"
        elif score >= 5:
            return "High"
        elif score >= 3:
            return "Medium"
        else:
            return "Low"
    
    def save_articles(self, articles, filename=None):
        """Save articles to JSON file"""
        if filename is None:
            filename = f"data/articles_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(filename, 'w') as f:
            json.dump(articles, f, indent=2, default=str)
        
        self.logger.info(f"Saved articles to {filename}")
        return filename

# Usage example
if __name__ == "__main__":
    collector = AINewsCollector()
    articles = collector.collect_rss_feeds(days_back=7)
    relevant_articles = collector.filter_relevant_articles(articles)
    collector.save_articles(relevant_articles)