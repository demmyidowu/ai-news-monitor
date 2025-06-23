# AI News Monitor 🤖

An automated system that collects, filters, and summarizes weekly AI industry news from leading sources. Perfect for staying current with AI developments and creating AI-generated podcasts using Google's NotebookLM.

## 🎯 Features

- **Automated RSS Collection**: Gathers news from 20+ AI-focused sources
- **Smart Filtering**: Uses keywords and relevance scoring to find the most important AI stories
- **Multiple Output Formats**:
  - Text summary for quick reading
  - Word document for professional sharing
  - NotebookLM-optimized script for AI podcast generation
  - Raw JSON data for analysis
- **Weekly Automation**: GitHub Actions runs every Sunday
- **Email Notifications**: Get notified when your summary is ready
- **Categorized Content**: Stories organized by type (research, industry, policy, etc.)

## 📊 News Categories

The system categorizes AI news into:

- 🚨 **Critical Developments** - Breaking news and major announcements
- 🔬 **Research & Development** - Academic papers and breakthroughs
- 🏢 **Industry News** - Company announcements and products
- 📋 **Policy & Ethics** - Regulation and governance
- 📈 **Market Trends** - Analysis and insights
- 🛠️ **Tools & Applications** - New AI tools and platforms
- 💰 **Funding & Investment** - VC activity and funding rounds
- 👥 **People & Leadership** - Key personnel changes

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- GitHub account (for automation)
- (Optional) Gmail account for notifications

### Local Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/ai-news-monitor.git
cd ai-news-monitor
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create directory structure:

```bash
mkdir -p data outputs logs config src
```

4. Copy configuration files:

```bash
cp sources.json config/sources.json
cp collector.py src/collector.py
cp summarizer.py src/summarizer.py
```

5. Run the collector:

```bash
python main.py
```

## 🤖 GitHub Actions Setup

1. Fork this repository
2. Go to Settings → Secrets and variables → Actions
3. Add these secrets (optional, for email notifications):
   - `EMAIL_USERNAME`: Your Gmail address
   - `EMAIL_APP_PASSWORD`: Your Gmail app password
   - `EMAIL_TO`: Primary recipient email address
   - `EMAIL_CC`: CC recipient email address (typically your own)

The workflow runs automatically every Sunday at 9 AM UTC.

### Manual Trigger

1. Go to Actions tab
2. Select "Weekly AI News Collection"
3. Click "Run workflow"
4. (Optional) Adjust days to look back

## 📝 NotebookLM Integration

1. After the workflow runs, download these files from the release:

   - `NotebookLM_Script_YYYYMMDD.md`
   - `NotebookLM_Summary_YYYYMMDD.txt`

2. Go to [NotebookLM](https://notebooklm.google.com/)

3. Create a new notebook and upload both files

4. Click "Generate Podcast" to create an AI-generated conversation about the week's AI news

## 📁 Project Structure

```
ai-news-monitor/
├── main.py                    # Main orchestration script
├── collector.py               # RSS feed collector
├── summarizer.py              # Summary generator
├── notebooklm_generator.py    # NotebookLM script creator
├── sources.json               # RSS feed configuration
├── requirements.txt           # Python dependencies
├── .github/
│   └── workflows/
│       └── ai-news-collection.yml  # GitHub Actions workflow
├── src/                       # Source code directory
├── data/                      # Raw article data
├── outputs/                   # Generated summaries
└── logs/                      # Application logs
```

## 🔧 Configuration

### Adding/Removing News Sources

Edit `sources.json` to customize RSS feeds:

```json
{
  "name": "New AI Blog",
  "url": "https://example.com/ai/rss",
  "priority": "high",
  "category": "research"
}
```

### Customizing Keywords

Modify the `keywords` section in `sources.json` to adjust filtering:

- Core AI terms (GPT, LLM, neural network, etc.)
- Company names (OpenAI, Anthropic, Google, etc.)
- Technology types (computer vision, NLP, robotics, etc.)

## 📊 Output Files

Each run generates:

- **Text Summary** (`AI_Industry_Weekly_YYYYMMDD.txt`) - Readable summary with top stories
- **Word Document** (`AI_Weekly_News_Summary_YYYYMMDD.docx`) - Professional report format
- **NotebookLM Script** (`NotebookLM_Script_YYYYMMDD.md`) - Rich content for AI podcast
- **NotebookLM Summary** (`NotebookLM_Summary_YYYYMMDD.txt`) - Concise context file
- **Raw Data** (`articles_YYYYMMDD.json`) - All collected articles

## 🛠️ Troubleshooting

### No articles found

- Check if RSS feeds are still active
- Verify network connectivity
- Review keywords in `sources.json`

### GitHub Actions failing

- Check Actions tab for error logs
- Verify all files are properly committed
- Ensure directory structure is correct

### Email notifications not working

- Verify Gmail app password is correct
- Check that secrets are properly set
- Enable 2-factor authentication on Gmail

## 📈 Extending the System

### Add New Categories

1. Edit `_categorize_articles()` in `notebooklm_generator.py`
2. Add category logic in `collector.py`
3. Update display titles in `summarizer.py`

### Integrate New Sources

1. Find RSS feed URL
2. Add to `sources.json`
3. Set appropriate priority and category

### Custom Analysis

- Use the JSON output for data analysis
- Track trends over time
- Build visualizations

## 🎯 Key AI Sources Monitored

- **Companies**: OpenAI, Anthropic, Google AI, DeepMind, Microsoft, Meta
- **News**: TechCrunch, MIT Tech Review, VentureBeat, The Verge
- **Academic**: arXiv, Stanford HAI
- **Analysis**: Wired, Ars Technica, AI News

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

For issues or questions:

- Open an issue on GitHub
- Check existing issues for solutions
- Review logs in the `logs/` directory

## 🙏 Acknowledgments

- Built for the AI community
- Powered by Python and GitHub Actions
- Designed for NotebookLM integration

---

**Note**: This tool aggregates publicly available RSS feeds. Always verify important information from original sources.
