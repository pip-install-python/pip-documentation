# Changelog

All notable changes to Pip Install Python Documentation will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] - 2025-11-16

### Initial Production Release

Production-ready documentation platform for Pip Install Python's custom Dash components and Python packages, now live at **https://pip-install-python.com**

---

## 🎯 Core Features

### 📚 Documentation System
- **Markdown-Driven Content**
  - Write documentation in Markdown with Python integration
  - Frontmatter metadata for page configuration
  - Custom directive system for interactive examples
  - Automatic page generation and routing
  - Table of contents generation

- **Custom Markdown Directives**
  - `.. toc::` - Automatic table of contents from headings
  - `.. exec::module.path` - Render executable Python components
  - `.. source::file/path.py` - Display source code with syntax highlighting
  - `.. sourcetabs::module.path` - Tabbed source code display
  - `.. kwargs::ComponentName` - Component props documentation tables
  - `.. llms_copy::` - Copy llms.txt URL for AI assistant sharing

- **18 Custom Component Libraries Documented**
  - Currently maintained: dash-summernote, dash-insta-stories, dash-image-gallery, dash-fullcalendar, dash-gauge, dash-emoji-mart, dash-dock, dash-pannellum, dash-planet, dash-model-viewer, dash-excalidraw
  - Archived: dash-credit-cards, dash-charty, dash-nivo, dash-discord, dash-dynamic-grid-layout, dash-swiper, dash-fullcalendar
  - Each with comprehensive guides, live examples, and download statistics

### 🎨 Modern UI/UX
- **Responsive Design**
  - Mobile, tablet, and desktop optimized layouts
  - Adaptive navigation with hamburger menu on mobile
  - Responsive AppShell with collapsible sidebar
  - Custom breakpoints for optimal viewing

- **Theme System**
  - Light and dark mode with automatic persistence
  - Browser preference detection on first visit
  - Smooth theme transitions without page flash
  - Theme-aware Plotly charts with DMC figure templates
  - Professional typography with Inter font family
  - Systematic 4px-based spacing scale
  - 5-level shadow system for depth
  - Code block theming with proper syntax highlighting

- **Navigation & Search**
  - Custom page ordering and organization
  - Searchable component navigation
  - Icon-based visual hierarchy
  - "Other Apps" menu for quick access to related projects
  - Breadcrumb-style organization

### 📊 Analytics & Tracking

- **Visitor Analytics System**
  - Session-based tracking using MD5 hash of IP + user agent
  - Device type detection (desktop, mobile, tablet, bot)
  - Bot type classification (training, search, traditional)
  - Geolocation tracking with ip-api.com integration
  - Unique visitor counting (sessions, not page views)
  - First-visit-only location data to avoid duplicates
  - Privacy-conscious tracking with session IDs
  - Race condition handling for concurrent file access
  - JSON data persistence with error recovery

- **Analytics Dashboard** (`/analytics/traffic`)
  - Real-time visitor statistics (unique visitors by device type)
  - Interactive geolocation bubble map with Plotly
  - Device breakdown visualization (desktop/mobile/tablet/bot)
  - Traffic by page with bar charts
  - Hourly traffic patterns with line charts
  - Browser detection and analytics
  - Comprehensive visitor metrics and insights

- **PyPI Download Statistics**
  - Automatic aggregation across all 18 packages
  - Real-time download counters from pypistats.org API
  - Visual presentation on home page
  - Smart error handling and caching
  - Historical data tracking

### 🤖 AI Integration & Chat

- **Page-Level AI Chat**
  - Context-aware AI assistant on every documentation page
  - Streaming SSE responses for real-time interaction
  - Page context injection (markdown content, code examples, metadata)
  - Session-based conversation tracking
  - Multiple response formats (markdown, code)
  - Chat history and analytics tracking
  - Cost and token usage monitoring
  - Error handling and graceful degradation

- **AI Analytics Dashboard** (`/analytics`)
  - Cost breakdown by model (Claude Opus, Sonnet, Haiku)
  - Total API costs and token usage tracking
  - Questions per page visualization
  - Recent user questions with interactive modal details
  - Chat log viewing with formatted Q&A display
  - Time-based filtering and analysis
  - Cost efficiency metrics

- **AI Chat Modal System**
  - Row selection in dash-ag-grid tables
  - Modal display of complete chat interactions
  - Formatted question and response sections
  - Metadata badges (timestamp, page, model, cost, tokens)
  - Markdown rendering for responses
  - Clean, professional UI with DMC Paper components

### 🔍 SEO & LLM Integration

- **dash-improve-my-llms Integration (v0.3.0)**
  - Automatic llms.txt generation for AI understanding
  - page.json with technical architecture details
  - architecture.txt with ASCII art overview
  - robots.txt with intelligent bot management
  - sitemap.xml with smart priority inference
  - Schema.org structured data for search engines
  - Custom page-specific llms.txt routes
  - Source directive processing for complete context

- **Bot Management**
  - Blocks AI training bots (GPTBot, CCBot, anthropic-ai)
  - Allows AI search bots (ChatGPT-User, ClaudeBot, PerplexityBot)
  - Allows traditional search engines (Googlebot, Bingbot)
  - Configurable crawl delays and disallowed paths
  - Privacy controls with mark_hidden() for sensitive pages

- **SEO Optimization**
  - Google Analytics integration (G-6WYY9JHMP2)
  - Minimal, optimized HTML template
  - Fast page load times
  - Mobile-friendly design
  - Proper meta tag configuration
  - Structured data for rich search results

### 🐋 Production Infrastructure

- **Technology Stack**
  - **Dash 3.2.0** - Modern Plotly Dash framework
  - **Dash Mantine Components 2.4.0** - Beautiful React UI
  - **Mantine 8.3.6** - Latest Mantine design system
  - **React 18.2.0** - Modern React features
  - **Python 3.11+** - Latest Python capabilities
  - **Flask 3.1.2** - Production web server
  - **Plotly 6.4.0** - Interactive visualizations

- **Deployment Ready**
  - Docker and docker-compose support
  - Gunicorn production server configuration
  - Environment-based configuration
  - Error handling and logging
  - Graceful degradation for missing data
  - Production URL configuration (pip-install-python.com)

- **Performance Optimizations**
  - Fast file pattern matching with Glob
  - Efficient JSON data persistence
  - LRU caching for geolocation lookups
  - Optimized font loading (Inter, JetBrains Mono)
  - CSS optimization and minification
  - Chart template caching
  - Smart skip paths for analytics tracking

### 🎯 Developer Experience

- **Code Quality**
  - PEP 8 compliant Python code
  - Comprehensive inline comments
  - Type hints where appropriate
  - Modular, reusable components
  - Clean separation of concerns
  - Error handling throughout

- **Documentation Quality**
  - 5 comprehensive guides with 15+ examples
  - Live interactive code demonstrations
  - Best practices and patterns
  - Troubleshooting guides
  - Migration documentation
  - API references

- **Development Tools**
  - Hot reload during development
  - Debug mode support
  - Comprehensive error messages
  - Development server on port 8502
  - Environment variable support

---

## 📁 Project Structure

```
pip-docs/
├── assets/                          # Static assets
│   ├── main.css                    # Custom styles (theme-aware)
│   ├── m2d.css                     # Markdown styling
│   ├── chat.js                     # AI chat client
│   ├── llms_copy.js                # LLM copy button handler
│   ├── model_viewer_*.js           # 3D model viewer scripts
│   └── [images, icons, etc.]
│
├── callbacks/                       # Dash callbacks
│   └── chat_callbacks.py           # AI chat functionality
│
├── components/                      # UI components
│   ├── appshell.py                 # Main layout with MantineProvider
│   ├── header.py                   # Header with search and theme toggle
│   └── navbar.py                   # Navigation sidebar (custom ordering)
│
├── docs/                            # Documentation content
│   ├── dash_*/                     # Component-specific docs (18 packages)
│   └── [markdown files + Python examples]
│
├── lib/                             # Utility libraries
│   ├── analytics_tracker.py        # Visitor analytics system
│   ├── constants.py                # App-wide constants
│   ├── directives/                 # Custom markdown directives
│   └── page_chat/                  # AI chat context gathering
│
├── pages/                           # Dash pages
│   ├── home.py                     # Home page with download stats
│   ├── markdown.py                 # Dynamic markdown loader
│   ├── analytics.py                # Visitor analytics dashboard
│   ├── api_analytics.py            # AI chat analytics dashboard
│   └── not_found_404.py            # Custom 404 page
│
├── templates/
│   └── index.html                  # Production HTML template
│
├── CHANGELOG.md                    # This file
├── README.md                       # Project documentation
├── CLAUDE.md                       # AI development notes
├── requirements.txt                # Python dependencies
├── package.json                    # Node.js dependencies
├── run.py                          # Application entry point
└── visitor_analytics.json          # Analytics data store
```

---

## 🔧 Configuration

### Environment Variables
- `DASH_DEBUG` - Enable debug mode (default: False)
- `DASH_HOST` - Server host (default: 0.0.0.0)
- `DASH_PORT` - Server port (default: 8502)
- `ANTHROPIC_API_KEY` - API key for AI chat (required for chat features)

### Key Configuration Points
- `run.py:44` - Base URL for SEO (set to https://pip-install-python.com)
- `run.py:47-53` - Bot management policies
- `lib/constants.py` - App-wide constants and theming
- `templates/index.html` - Google Analytics and meta tags
- `components/appshell.py` - Theme configuration and MantineProvider settings

---

## 📊 Analytics Features Breakdown

### Session-Based Tracking
- Unique session ID generated from IP address + user agent (MD5 hash)
- Prevents duplicate counting of same visitor across pages
- First-visit-only geolocation to reduce API calls
- Consistent localhost location assignment for development testing

### Visitor Analytics
- **Device Detection**: Desktop, mobile, tablet, bot classification
- **Bot Classification**: Training bots, search bots, traditional crawlers
- **Geolocation**: City, region, country with coordinates
- **Privacy**: No PII stored, only hashed session IDs
- **Performance**: Skip tracking for assets (.css, .js, images, Dash internals)

### AI Chat Analytics
- **Cost Tracking**: Per-model cost breakdown (Opus $15/$75, Sonnet $3/$15, Haiku $0.25/$1.25)
- **Token Usage**: Input and output token counting
- **Question Analysis**: Track questions per page
- **Response Logging**: Complete chat history with timestamps
- **Modal Details**: Interactive row selection for full chat logs

---

## 🚀 Getting Started

### Installation
```bash
# Clone repository
git clone https://github.com/pip-install-python/pip-docs.git
cd pip-docs

# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
npm install

# Run development server
python run.py
```

### Access Points
- **Main Application**: http://localhost:8502
- **Visitor Analytics**: http://localhost:8502/analytics/traffic
- **AI Chat Analytics**: http://localhost:8502/analytics
- **404 Page**: http://localhost:8502/404

### Production Deployment
```bash
# Build Docker image
docker build -t pip-docs .

# Run with Docker Compose
docker-compose up -d

# Access at port 8550
```

---

## 🎯 Future Enhancements

### Planned Features
- Extended analytics dashboard with more visualizations
- User authentication and personalized experiences
- Advanced search with full-text indexing
- Version switcher for documentation
- Code playground/sandbox for testing components
- Automated screenshot generation for examples
- More chart types (heatmaps, 3D plots, geographic maps)
- Export analytics to CSV/JSON
- Real-time visitor tracking with WebSocket
- A/B testing framework for documentation

### Under Consideration
- Multi-language support (i18n)
- Community contributions and voting system
- Interactive tutorials and walkthroughs
- Video tutorials integration
- RSS feed for updates
- Newsletter integration
- Component comparison tools
- Performance benchmarking suite

---

## 🙏 Acknowledgments

### Built With
- [Plotly Dash](https://dash.plotly.com/) - Web framework
- [Dash Mantine Components](https://dash-mantine-components.com/) - UI components
- [Mantine](https://mantine.dev/) - React component library
- [dash-improve-my-llms](https://pypi.org/project/dash-improve-my-llms/) - AI/SEO integration
- [dash-ag-grid](https://dash.plotly.com/dash-ag-grid) - Advanced data grids
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Anthropic Claude](https://anthropic.com/) - AI chat capabilities

### Special Thanks
- Plotly Dash team for the amazing framework
- Snehil Vijay for Dash Mantine Components
- The open-source community for continuous support
- All contributors to the custom Dash components

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Support & Community

### Get Help
- **GitHub Issues**: [Report bugs or request features](https://github.com/pip-install-python/pip-docs/issues)
- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/pip-install-python/pip-docs/discussions)
- **Dash Community**: [Plotly Community Forum](https://community.plotly.com/)
- **Discord**: [Join the Dash Discord](https://discord.gg/uwQ2f3KCad)

### Stay Connected
- **Website**: https://pip-install-python.com
- **GitHub**: [@pip-install-python](https://github.com/pip-install-python)
- **YouTube**: [Pip Install Python](https://youtube.com/@PipInstallPython)
- **Plotly.pro**: https://plotly.pro
- **ai-agent.buzz**: https://ai-agent.buzz
- **GeoMapIndex**: https://dash.geomapindex.com

---

**Made with ❤️ by Pip Install Python LLC**

**Star this repo if you find it useful!** ⭐

---

[1.0.0]: https://github.com/pip-install-python/pip-docs/releases/tag/v1.0.0