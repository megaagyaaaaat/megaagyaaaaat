#!/usr/bin/env python3

import base64
import re
from pathlib import Path

SVG = Path("ascii.svg")
FONT = Path("scripts/fonts/jbmono-ramp.woff2")

FONT_FACE = (
    "@font-face{"
    "font-family:'JBMono';"
    "src:url(data:font/woff2;base64,BASE64);"
    "font-display:block;"
    "}"
)

def main():
    if not SVG.exists():
        raise SystemExit("ascii.svg not found")

    if not FONT.exists():
        raise SystemExit(
            "jbmono-ramp.woff2 not found. "
            "Create/download the font subset first."
        )

    data = base64.b64encode(FONT.read_bytes()).decode("ascii")

    svg = SVG.read_text(encoding="utf-8")

    css = FONT_FACE.replace("BASE64", data)

    svg = svg.replace(
        "<style>",
        "<style>" + css,
        1
    )

    svg = svg.replace(
        'font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"',
        'font-family="JBMono"'
    )

    SVG.write_text(svg, encoding="utf-8")

    print("embedded jbmono-ramp.woff2 into ascii.svg")

if __name__ == "__main__":
    main()
