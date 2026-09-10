import json
import os
import urllib.request
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
    "variables": {"login": USERNAME}
}).encode("utf-8")

request = urllib.request.Request(
    "https://api.github.com/graphql",
    data=payload,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "User-Agent": "github-profile-bunnies"
    }
)

with urllib.request.urlopen(request) as response:
    result = json.loads(response.read().decode("utf-8"))

if "errors" in result:
    raise RuntimeError(result["errors"])

calendar = result["data"]["user"]["contributionsCollection"]["contributionCalendar"]
weeks = calendar["weeks"]
total = calendar["totalContributions"]

# -----------------------------
# Layout
# -----------------------------
CELL = 11
GAP = 3
STEP = CELL + GAP

LEFT = 20
TOP = 35

GRAPH_WIDTH = len(weeks) * STEP
WIDTH = LEFT + GRAPH_WIDTH + 20
HEIGHT = TOP + (7 * STEP) + 25

COLORS = [
    "#161b22",  # 0
    "#0e4429",  # low
    "#006d32",
    "#26a641",
    "#39d353",  # high
]

def level(count):
    if count == 0:
        return 0
    elif count <= 2:
        return 1
    elif count <= 5:
        return 2
    elif count <= 9:
        return 3
    return 4

svg = []

svg.append(f'''<svg width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" xmlns="http://www.w3.org/2000/svg">''')

svg.append("""
<style>
  text {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  }

  .title {
    fill: #8b949e;
    font-size: 12px;
    font-weight: 600;
  }

  @media (prefers-color-scheme: light) {
    .title { fill: #57606a; }
  }
</style>
""")

# -----------------------------
# Title
# -----------------------------
svg.append(
    f'<text x="{LEFT}" y="16" class="title">{USERNAME} — {total} contributions</text>'
)

# -----------------------------
# Contribution graph
# -----------------------------
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

# -----------------------------
# Cute Jumping Bunnies
# -----------------------------
TRAIN_ROW = 3

animal_y = TOP + TRAIN_ROW * STEP
start_x = LEFT - 40
end_x = LEFT + GRAPH_WIDTH + 20

svg.append(f'''
<g>
  <animateTransform
    attributeName="transform"
    type="translate"
    from="{start_x} {animal_y}"
    to="{end_x} {animal_y}"
    dur="12s"
    repeatCount="indefinite"
  />

  <!-- Bunny 1 (White) -->
  <g>
    <animateTransform attributeName="transform" type="translate" values="0,0; 0,-12; 0,0" keyTimes="0; 0.5; 1" dur="0.6s" repeatCount="indefinite" />
    <g fill="#f8f9fa">
      <ellipse cx="6" cy="6" rx="4.5" ry="3.5" />
      <circle cx="10" cy="3.5" r="3" />
      <ellipse cx="9" cy="0.5" rx="1" ry="2.5" transform="rotate(-15 9 0.5)" />
      <ellipse cx="11" cy="0.5" rx="1" ry="2.5" transform="rotate(15 11 0.5)" />
      <circle cx="1.5" cy="6.5" r="1.5" />
      <circle cx="11" cy="3" r="0.6" fill="#0d1117" />
      <ellipse cx="11.5" cy="4.2" rx="0.7" ry="0.4" fill="#ffb6c1" />
    </g>
  </g>

  <!-- Bunny 2 (Gray) -->
  <g transform="translate(-16, 0)">
    <animateTransform attributeName="transform" type="translate" values="0,0; 0,-12; 0,0" keyTimes="0; 0.5; 1" dur="0.6s" begin="0.2s" repeatCount="indefinite" />
    <g fill="#d0d7de">
      <ellipse cx="6" cy="6" rx="4.5" ry="3.5" />
      <circle cx="10" cy="3.5" r="3" />
      <ellipse cx="9" cy="0.5" rx="1" ry="2.5" transform="rotate(-15 9 0.5)" />
      <ellipse cx="11" cy="0.5" rx="1" ry="2.5" transform="rotate(15 11 0.5)" />
      <circle cx="1.5" cy="6.5" r="1.5" fill="#f8f9fa" />
      <circle cx="11" cy="3" r="0.6" fill="#0d1117" />
      <ellipse cx="11.5" cy="4.2" rx="0.7" ry="0.4" fill="#ffb6c1" />
    </g>
  </g>

  <!-- Bunny 3 (Lavender) -->
  <g transform="translate(-32, 0)">
    <animateTransform attributeName="transform" type="translate" values="0,0; 0,-12; 0,0" keyTimes="0; 0.5; 1" dur="0.6s" begin="0.4s" repeatCount="indefinite" />
    <g fill="#d2a8ff">
      <ellipse cx="6" cy="6" rx="4.5" ry="3.5" />
      <circle cx="10" cy="3.5" r="3" />
      <ellipse cx="9" cy="0.5" rx="1" ry="2.5" transform="rotate(-15 9 0.5)" />
      <ellipse cx="11" cy="0.5" rx="1" ry="2.5" transform="rotate(15 11 0.5)" />
      <circle cx="1.5" cy="6.5" r="1.5" fill="#f8f9fa" />
      <circle cx="11" cy="3" r="0.6" fill="#0d1117" />
      <ellipse cx="11.5" cy="4.2" rx="0.7" ry="0.4" fill="#ffb6c1" />
    </g>
  </g>
</g>
''')

svg.append("</svg>")

output = Path("assets/github-animals.svg")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text("".join(svg), encoding="utf-8")