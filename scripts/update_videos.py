"""Busca os vídeos mais recentes do canal (inclui lives) via RSS do YouTube e grava videos.json."""
import json
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

CHANNEL_ID = "UCx2TGoONR_X-mhG5QKFheOw"
FEED = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
OUT = Path(__file__).resolve().parent.parent / "videos.json"
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}

with urllib.request.urlopen(FEED, timeout=30) as r:
    root = ET.fromstring(r.read())

videos = [
    {
        "id": e.find("yt:videoId", NS).text,
        "title": e.find("a:title", NS).text,
        "published": e.find("a:published", NS).text,
    }
    for e in root.findall("a:entry", NS)
]
videos.sort(key=lambda v: v["published"], reverse=True)
OUT.write_text(json.dumps(videos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"{len(videos)} vídeos gravados em {OUT.name}")
