# WaniKani scraper for AnkiDeck

This tool scrapes data from WaniKani and formats it for easy import into Anki, a popular flashcard app.

## Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/Alpyg/wani_scraper.git
   ```
1. Copy out.txt to kanji.txt:
   ```bash
   cp out.txt kanji.txt
   ```
1. Run the scraper:
   ```bash
   python src/main.py [kanji|vocabulary] >> kanji.txt
   ```
1. Import the generated file into Anki.
