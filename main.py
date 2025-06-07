"""
AI News Monitor - Main Workflow
Run this script weekly to generate AI news summaries
"""

import os
import sys
from datetime import datetime
import logging

# Add src directory to path
sys.path.append('src')

from collector import AINewsCollector
from summarizer import AINewsSummarizer

def setup_directories():
    """Create necessary directories if they don't exist"""
    directories = ['data', 'outputs', 'logs']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)

def setup_logging():
    """Setup logging configuration"""
    try:
        log_filename = f"logs/ai_news_{datetime.now().strftime('%Y%m%d')}.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    except Exception as e:
        # Fallback to console-only logging if file creation fails
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
        logger = logging.getLogger(__name__)
        logger.warning(f"Could not create log file, using console only: {e}")
        return logger

def main():
    """Main workflow"""
    setup_directories()  # Create directories BEFORE logging
    logger = setup_logging()
    
    try:
        logger.info("Starting AI News collection and summarization...")
        
        # Step 1: Collect articles
        collector = AINewsCollector()
        articles = collector.collect_rss_feeds(days_back=7)
        
        if not articles:
            logger.warning("No articles collected. Exiting.")
            return
        
        # Step 2: Filter relevant articles
        relevant_articles = collector.filter_relevant_articles(articles)
        
        if not relevant_articles:
            logger.warning("No relevant articles found. Exiting.")
            return
        
        # Step 3: Save raw data
        data_file = collector.save_articles(relevant_articles)
        
        # Step 4: Generate summary with custom names
        summarizer = AINewsSummarizer()
        
        # Create text summary
        text_summary = summarizer.create_text_summary(relevant_articles)
        text_output = f"outputs/AI_Industry_Weekly_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(text_output, 'w') as f:
            f.write(text_summary)
        logger.info(f"Text summary saved to {text_output}")
        
        # Create Word document with custom name
        doc_output = summarizer.create_word_document(
            relevant_articles, 
            custom_name="AI_Industry_Weekly"
        )
        
        logger.info("AI News summary generation completed successfully!")
        logger.info(f"Text summary: {text_output}")
        logger.info(f"Word document: {doc_output}")
        logger.info(f"Total articles processed: {len(relevant_articles)}")
        
    except Exception as e:
        logger.error(f"Error in main workflow: {e}")
        raise

if __name__ == "__main__":
    main()