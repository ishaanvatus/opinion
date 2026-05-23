"""
Web scraping pipeline for collecting public opinion data from social media
and discussion forums. Used to calibrate the Cell Particle Swarm Model
against real-world sentiment trajectories.

Target event: Liu Wenzheng death hoax (February 2023)
States: {-1: skeptic, 0: neutral, 1: supporter}
"""

import json
import time
import re
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

from config import SEED

# ---------------------------------------------------------------------------
# Sentiment lexicon for mapping text to {-1, 0, 1}
# ---------------------------------------------------------------------------

SUPPORT_WORDS = {
    "mourning", "rip", "condolences", "sad", "tragedy", "heartbroken",
    "devastating", "grief", "pray", "prayers", "shocked", "unbelievable",
    "terrible", "horrible", "loss", "rest in peace", "gone",
    "哀悼", "安息", "节哀", "痛心", "悲剧", "祈祷", "震惊",
}

SKEPTIC_WORDS = {
    "fake", "hoax", "false", "rumour", "rumor", "lie", "debunked",
    "fabricated", "misinformation", "not true", "didn't die", "alive",
    "still living", "scam", "clickbait", "misleading", "exposed",
    "假消息", "谣言", "辟谣", "假的", "没死", "还活着", "炒作",
}

NEUTRAL_WORDS = {
    "report", "news", "update", "statement", "clarification", "checking",
    "verify", "verification", "official", "source",
    "消息", "新闻", "官方", "核实",
}


def classify_sentiment(text: str) -> int:
    """Return -1 (skeptic), 0 (neutral), or 1 (supporter) based on lexicon."""
    text_lower = text.lower()
    s_count = sum(1 for w in SUPPORT_WORDS if w in text_lower)
    k_count = sum(1 for w in SKEPTIC_WORDS if w in text_lower)
    if s_count > k_count:
        return 1
    elif k_count > s_count:
        return -1
    return 0


# ---------------------------------------------------------------------------
# Scraper 1: requests + BeautifulSoup (static pages)
# ---------------------------------------------------------------------------

class StaticScraper:
    """Scrape public discussion threads using requests + BeautifulSoup."""

    def __init__(self, user_agent: str | None = None):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": user_agent or (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        })
        self.session.max_redirects = 5

    def scrape_url(self, url: str, timeout: int = 20) -> list[dict]:
        """Fetch a single URL and extract comment-like text blocks."""
        results = []
        try:
            resp = self.session.get(url, timeout=timeout)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            # Remove script/style tags that contain non-content text
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            for tag in soup.find_all(["p", "div", "span", "li", "td"]):
                text = tag.get_text(strip=True, separator=" ")
                if len(text) > 30:
                    sentiment = classify_sentiment(text)
                    results.append({
                        "text": text[:500],
                        "sentiment": sentiment,
                        "source": url,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
        except requests.RequestException as e:
            print(f"[StaticScraper] Error fetching {url}: {e}")

        return results


# ---------------------------------------------------------------------------
# Scraper 2: Playwright (dynamic / JS-rendered pages)
# ---------------------------------------------------------------------------

class DynamicScraper:
    """Scrape JavaScript-rendered pages using Playwright."""

    def __init__(self):
        if not HAS_PLAYWRIGHT:
            raise ImportError(
                "Playwright not installed. Run: pip install playwright && playwright install"
            )

    def scrape_url(self, url: str, wait_selector: str = "body",
                   wait_ms: int = 3000) -> list[dict]:
        """Launch a headless browser, wait for content, extract text."""
        results = []
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_selector(wait_selector, timeout=10000)
                page.wait_for_timeout(wait_ms)

                texts = page.eval_on_selector_all(
                    "p, div, span, li, td",
                    "elements => elements.map(e => e.innerText).filter(t => t.length > 30)"
                )
                for text in texts:
                    sentiment = classify_sentiment(text)
                    results.append({
                        "text": text[:500],
                        "sentiment": sentiment,
                        "source": url,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })
            except Exception as e:
                print(f"[DynamicScraper] Error on {url}: {e}")
            finally:
                browser.close()

        return results


# ---------------------------------------------------------------------------
# Local test: scrape a local HTML file instead of hitting live URLs
# ---------------------------------------------------------------------------

def scrape_local_html(html_path: str) -> list[dict]:
    """Scrape a local HTML file for testing the pipeline without network."""
    results = []
    with open(html_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    for tag in soup.find_all(["p", "div", "span", "li", "td"]):
        text = tag.get_text(strip=True, separator=" ")
        if len(text) > 30:
            sentiment = classify_sentiment(text)
            results.append({
                "text": text[:500],
                "sentiment": sentiment,
                "source": html_path,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            })
    return results


# ---------------------------------------------------------------------------
# Data pipeline
# ---------------------------------------------------------------------------

def build_sentiment_timeline(data: list[dict],
                             time_key: str = "timestamp",
                             state_key: str = "sentiment") -> dict:
    """Aggregate sentiment counts into a timeline comparable to model output."""
    timeline = {}
    for entry in data:
        ts = entry.get(time_key, "")[:10]
        state = entry.get(state_key, 0)
        if ts not in timeline:
            timeline[ts] = {"support": 0, "neutral": 0, "skeptic": 0}
        if state == 1:
            timeline[ts]["support"] += 1
        elif state == 0:
            timeline[ts]["neutral"] += 1
        else:
            timeline[ts]["skeptic"] += 1
    return timeline


def save_results(data: list[dict], path: str = "scraped_data.json"):
    """Write scraped data to JSON for later analysis."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(data)} entries to {path}")


def load_results(path: str = "scraped_data.json") -> list[dict]:
    """Load previously scraped data."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Local test mode
# ---------------------------------------------------------------------------

DEMO_HTML = """<!DOCTYPE html>
<html><body>
<h1>Liu Wenzheng Discussion Thread</h1>
<p>So sad to hear the news. RIP Liu Wenzheng. Condolences to the family.</p>
<p>This is fake news, he's still alive. Complete hoax.</p>
<p>The official statement hasn't been released yet. Waiting for verification.</p>
<p>I can't believe this tragedy. Heartbroken.</p>
<p>This rumor has been debunked multiple times already.</p>
</body></html>"""


def run_local_demo():
    """Run the pipeline on a built-in HTML snippet — no network needed."""
    print("[Local demo] Parsing inline HTML...")
    html_path = Path("/tmp/demo_thread.html")
    html_path.write_text(DEMO_HTML, encoding="utf-8")

    all_data = scrape_local_html(str(html_path))
    timeline = build_sentiment_timeline(all_data)
    save_results(all_data, "scraped_data.json")

    total = len(all_data)
    s = sum(1 for d in all_data if d["sentiment"] == 1)
    n = sum(1 for d in all_data if d["sentiment"] == 0)
    k = sum(1 for d in all_data if d["sentiment"] == -1)

    print(f"\nSummary: {total} entries")
    print(f"  Supporters: {s} ({s/total*100:.1f}%)")
    print(f"  Neutrals:   {n} ({n/total*100:.1f}%)")
    print(f"  Skeptics:   {k} ({k/total*100:.1f}%)")
    print(f"\nTimeline: {json.dumps(timeline, indent=2)}")
    return all_data, timeline


# ---------------------------------------------------------------------------
# Example usage (live)
# ---------------------------------------------------------------------------

def run_demo():
    """Demonstrate the scraping pipeline with sample URLs."""
    urls = [
        "https://weibo.com/hot/search",
        "https://twitter.com/search?q=liu%20wenzheng",
        "https://www.reddit.com/search/?q=liu+wenzheng",
    ]

    all_data = []

    print("[1/3] Running static scraper...")
    scraper = StaticScraper()
    for url in urls:
        entries = scraper.scrape_url(url)
        all_data.extend(entries)
        time.sleep(1)

    if HAS_PLAYWRIGHT:
        print("[2/3] Running dynamic scraper...")
        dyn = DynamicScraper()
        for url in urls:
            entries = dyn.scrape_url(url)
            all_data.extend(entries)
            time.sleep(2)
    else:
        print("[2/3] Playwright not available, skipping dynamic scraper")

    print("[3/3] Building sentiment timeline...")
    timeline = build_sentiment_timeline(all_data)
    save_results(all_data)

    total = len(all_data)
    if total > 0:
        s = sum(1 for d in all_data if d["sentiment"] == 1)
        n = sum(1 for d in all_data if d["sentiment"] == 0)
        k = sum(1 for d in all_data if d["sentiment"] == -1)
        print(f"\nSummary: {total} entries")
        print(f"  Supporters: {s} ({s/total*100:.1f}%)")
        print(f"  Neutrals:   {n} ({n/total*100:.1f}%)")
        print(f"  Skeptics:   {k} ({k/total*100:.1f}%)")
    else:
        print("No data collected. Add working URLs to the urls list.")

    return all_data, timeline


if __name__ == "__main__":
    import sys
    if "--local" in sys.argv:
        run_local_demo()
    else:
        run_demo()
