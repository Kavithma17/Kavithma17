import json
import os
import urllib.request
from datetime import datetime
from pathlib import Path

USERNAME = os.environ.get("GITHUB_USERNAME", "Kavithma17")
TOKEN = os.environ["GITHUB_TOKEN"]

GRAPHQL_QUERY = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks {
          contributionDays {
            contributionCount
            date
            weekday
          }
        }
      }
    }
  }
}
"""

payload = json.dumps({
    "query": GRAPHQL_QUERY,
    "variables": {
        "login": USERNAME
    }
}).encode("utf-8")

request = urllib.request.Request(
    "https://api.github.com/graphql",
    data=payload,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "github-profile-train"
    }
)

with urllib.request.urlopen(request) as response:
    result = json.loads(response.read().decode("utf-8"))

if "errors" in result:
    raise RuntimeError(result["errors"])

calendar = (
    result["data"]["user"]["contributionsCollection"]
    ["contributionCalendar"]
)

weeks = calendar["weeks"]
total = calendar["totalContributions"]

# --------------------------------------------------
# SVG dimensions
# --------------------------------------------------

CELL = 11
GAP = 3
STEP = CELL + GAP

LEFT = 38
TOP = 42

GRAPH_WIDTH = len(weeks) * STEP
WIDTH = max(820, LEFT + GRAPH_WIDTH + 35)
HEIGHT = 220

# GitHub-like contribution shades
COLORS = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]

def level(count):
    if count == 0:
        return 0
    if count <= 2:
        return 1
    if count <= 5:
        return 2
    if count <= 9:
        return 3
    return 4


svg = []

svg.append(
    f'''<svg
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}"
    xmlns="http://www.w3.org/2000/svg">
'''
)

svg.append("""
<style>
    text {
        font-family: -apple-system, BlinkMacSystemFont,
        "Segoe UI", Helvetica, Arial, sans-serif;
    }

    .title {
        fill: #c9d1d9;
        font-size: 15px;
        font-weight: 600;
    }

    .muted {
        fill: #8b949e;
        font-size: 11px;
    }

    .rail {
        stroke: #8b949e;
        stroke-width: 2;
    }

    .sleeper {
        stroke: #484f58;
        stroke-width: 2;
    }

    .wheel {
        fill: #8b949e;
    }

    .train-body {
        fill: #58a6ff;
    }

    .train-window {
        fill: #0d1117;
    }

    .smoke {
        fill: #8b949e;
        opacity: 0;
    }

    @media (prefers-color-scheme: light) {
        .title {
            fill: #24292f;
        }

        .muted {
            fill: #57606a;
        }
    }
</style>
""")

# Background
svg.append(
    f'<rect width="{WIDTH}" height="{HEIGHT}" rx="12" fill="#0d1117"/>'
)

# Title
svg.append(
    f'<text x="{LEFT}" y="22" class="title">'
    f'{USERNAME} — {total} contributions'
    f'</text>'
)

# --------------------------------------------------
# Contribution squares
# --------------------------------------------------

for week_index, week in enumerate(weeks):
    x = LEFT + week_index * STEP

    for day in week["contributionDays"]:
        y = TOP + day["weekday"] * STEP

        count = day["contributionCount"]
        date = day["date"]

        color = COLORS[level(count)]

        svg.append(
            f'''
            <rect
                x="{x}"
                y="{y}"
                width="{CELL}"
                height="{CELL}"
                rx="2"
                fill="{color}">
                <title>{date}: {count} contributions</title>
            </rect>
            '''
        )

# --------------------------------------------------
# Railway
# --------------------------------------------------

rail_y1 = 160
rail_y2 = 170

svg.append(
    f'<line x1="{LEFT}" y1="{rail_y1}" '
    f'x2="{WIDTH - 25}" y2="{rail_y1}" class="rail"/>'
)

svg.append(
    f'<line x1="{LEFT}" y1="{rail_y2}" '
    f'x2="{WIDTH - 25}" y2="{rail_y2}" class="rail"/>'
)

for x in range(LEFT, WIDTH - 25, 18):
    svg.append(
        f'<line x1="{x}" y1="156" '
        f'x2="{x}" y2="174" class="sleeper"/>'
    )

# --------------------------------------------------
# Animated train
# --------------------------------------------------

travel_distance = WIDTH + 180

svg.append(f'''
<g id="train">

    <animateTransform
        attributeName="transform"
        type="translate"
        from="-170 0"
        to="{travel_distance} 0"
        dur="12s"
        repeatCount="indefinite"
    />

    <!-- locomotive -->
    <rect
        x="10"
        y="120"
        width="64"
        height="32"
        rx="4"
        class="train-body"
    />

    <!-- cabin -->
    <rect
        x="43"
        y="102"
        width="28"
        height="24"
        rx="3"
        class="train-body"
    />

    <rect
        x="49"
        y="107"
        width="15"
        height="12"
        rx="2"
        class="train-window"
    />

    <!-- chimney -->
    <rect
        x="19"
        y="103"
        width="11"
        height="19"
        rx="2"
        class="train-body"
    />

    <rect
        x="15"
        y="99"
        width="19"
        height="6"
        rx="2"
        class="train-body"
    />

    <!-- front -->
    <polygon
        points="74,128 86,136 74,144"
        class="train-body"
    />

    <!-- wheels -->
    <circle cx="27" cy="155" r="8" class="wheel"/>
    <circle cx="59" cy="155" r="8" class="wheel"/>

    <!-- first carriage -->
    <rect
        x="-58"
        y="125"
        width="60"
        height="27"
        rx="4"
        class="train-body"
    />

    <rect x="-49" y="131" width="13" height="10"
          rx="2" class="train-window"/>

    <rect x="-28" y="131" width="13" height="10"
          rx="2" class="train-window"/>

    <circle cx="-43" cy="155" r="7" class="wheel"/>
    <circle cx="-14" cy="155" r="7" class="wheel"/>

    <!-- second carriage -->
    <rect
        x="-126"
        y="125"
        width="60"
        height="27"
        rx="4"
        class="train-body"
    />

    <rect x="-117" y="131" width="13" height="10"
          rx="2" class="train-window"/>

    <rect x="-96" y="131" width="13" height="10"
          rx="2" class="train-window"/>

    <circle cx="-111" cy="155" r="7" class="wheel"/>
    <circle cx="-82" cy="155" r="7" class="wheel"/>

    <!-- smoke -->
    <circle cx="24" cy="91" r="5" class="smoke">
        <animate
            attributeName="cy"
            values="91;70;55"
            dur="2s"
            repeatCount="indefinite"
        />
        <animate
            attributeName="opacity"
            values="0;.7;0"
            dur="2s"
            repeatCount="indefinite"
        />
        <animate
            attributeName="r"
            values="3;7;11"
            dur="2s"
            repeatCount="indefinite"
        />
    </circle>

</g>
''')

# Footer
svg.append(
    f'<text x="{LEFT}" y="205" class="muted">'
    '🚂 Building one commit at a time'
    '</text>'
)

svg.append("</svg>")

output = Path("assets/github-train.svg")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text("".join(svg), encoding="utf-8")

print(f"Generated {output}")