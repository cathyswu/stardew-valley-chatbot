# 🌱 Stardew Companion

*Your personal AI companion for stress-free farming*

## 🎮 What is this?

Sometimes when life gets overwhelming, I find myself opening Stardew Valley. Just a couple of hours tending to crops, fishing by the dock, or raising animals, and somehow my worries feel a little smaller.

But ironically, even Stardew can get a little stressful — especially when I don’t know what to do next. Should I focus on farming? Mining? I’d end up googling things or bouncing between the wiki and Reddit threads just to figure out what’s optimal.

So I decided to build this.

This project is a personal Retrieval-Augmented Generation (RAG) chatbot designed specifically for Stardew Valley players. Instead of frantically googling "best crops for spring" or "where to find copper ore" across multiple tabs, you now have a one-stop shop for all your Stardew Valley questions, tips, and tricks.

## ✨ Features

- **Comprehensive Knowledge Base**: Sourced from the [Stardew Valley Wiki](https://stardewvalleywiki.com/) and the [r/StardewValley](https://www.reddit.com/r/StardewValley/) community
- **Instant Answers**: No more multiple Google searches - get tips, strategies, and information in one place
- **Stress-Free Gaming**: Focus on relaxing instead of researching
- **Community Wisdom**: Includes both official information and player-discovered strategies

## 🚧 Development Status

This project is currently in active development. Features and functionality may change as the project evolves.

## 🛠️ Local Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/stardew-valley-chatbot.git
   cd stardew-valley-chatbot
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
4. **Set up the knowledge base**
   ```bash
   # Run the scraper to build your knowledge base
   python scraper.py
   
   # Index the data for RAG
   python indexer.py
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

The chatbot should now be running locally!
