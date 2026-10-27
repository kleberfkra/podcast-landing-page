"""Busca os episódios mais recentes do podcast (RSS do Spotify for Creators) e grava episodes.json.

Para cada episódio: título, data, capa do episódio e link direto em open.spotify.com.
"""
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED = "https://anchor.fm/s/10b6ee9dc/podcast/rss"
SHOW_URL = "https://open.spotify.com/show/23H1CGhWocjTDJTiOK0Vzv"
LIMIT = 6
OUT = Path(__file__).resolve().parent.parent / "episodes.json"
ITUNES = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"
UA = {"User-Agent": "Mozilla/5.0"}
# Na página de episódio do Spotify for Creators há a lista de todos os episódios: {"title":"...","spotifyUrl":"..."}
PAIR = re.compile(r'"title":("(?:[^"\\]|\\.)*"),"spotifyUrl":("(?:[^"\\]|\\.)*")')


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read()


def spotify_urls(creators_link):
    """Retorna {título: link open.spotify.com/episode/...}."""
    try:
        html = get(creators_link).decode("utf-8", "ignore")
        return {json.loads(t).strip(): json.loads(u) for t, u in PAIR.findall(html)}
    except Exception:
        return {}


def main():
    root = ET.fromstring(get(FEED))
    channel_img = root.find(f"channel/{ITUNES}image")
    default_img = channel_img.get("href") if channel_img is not None else ""

    episodes = []
    for item in root.iter("item"):
        img = item.find(f"{ITUNES}image")
        episodes.append({
            "title": item.findtext("title", "").strip(),
            "published": parsedate_to_datetime(item.findtext("pubDate")).isoformat(),
            "image": img.get("href") if img is not None else default_img,
            "link": item.findtext("link", ""),
        })

    episodes.sort(key=lambda e: e["published"], reverse=True)
    episodes = episodes[:LIMIT]
    urls = spotify_urls(episodes[0]["link"]) if episodes else {}
    for e in episodes:
        e.pop("link")
        e["url"] = urls.get(e["title"], SHOW_URL)

    OUT.write_text(json.dumps(episodes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(episodes)} episódios gravados em {OUT.name}")


if __name__ == "__main__":
    main()
