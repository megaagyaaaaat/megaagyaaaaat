#!/usr/bin/env python3

import json
from pathlib import Path

INPUT = Path("stats.json")
OUTPUT = Path("stats.svg")

WIDTH = 720
HEIGHT = 190

BG = "#0d1117"
FG = "#c9d1d9"
MUTED = "#8b949e"
ACCENT = "#58a6ff"


def esc(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def main():
    data = json.loads(INPUT.read_text(encoding="utf-8"))

    login = data["login"]
    total = data["total_contributions"]
    commits = data["commits"]
    issues = data["issues"]
    prs = data["pull_requests"]
    reviews = data["reviews"]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">
<style>
text {{
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
}}
.title {{ fill: {FG}; font-size: 20px; font-weight: bold; }}
.label {{ fill: {MUTED}; font-size: 13px; }}
.value {{ fill: {FG}; font-size: 24px; font-weight: bold; }}
</style>

<rect width="100%" height="100%" rx="10" fill="{BG}"/>

<text x="28" y="36" class="title">
  {esc(login)} / GITHUB ACTIVITY
</text>

<text x="28" y="70" class="label">CONTRIBUTIONS</text>
<text x="28" y="101" class="value">{total}</text>

<text x="190" y="70" class="label">COMMITS</text>
<text x="190" y="101" class="value">{commits}</text>

<text x="350" y="70" class="label">ISSUES</text>
<text x="350" y="101" class="value">{issues}</text>

<text x="510" y="70" class="label">PULL REQUESTS</text>
<text x="510" y="101" class="value">{prs}</text>

<text x="28" y="145" class="label">REVIEWS</text>
<text x="28" y="172" class="value">{reviews}</text>

<text x="190" y="145" class="label">STATUS</text>
<text x="190" y="172" class="value">{esc("ACTIVE")}</text>

</svg>
"""

    OUTPUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()

