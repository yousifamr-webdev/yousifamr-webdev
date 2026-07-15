import os
import requests
from datetime import datetime

# --- YOUR DETAILS ---
USERNAME = "yousifamr-webdev"
BIRTHDATE = datetime(2003, 1, 1) # Edit to your exact birth date!
# --------------------

def fetch_github_stats():
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    response = requests.get(f"https://api.github.com/users/{USERNAME}", headers=headers)
    user_data = response.json()
    repos = user_data.get("public_repos", 0)
    followers = user_data.get("followers", 0)
    
    repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    repos_response = requests.get(repos_url, headers=headers)
    repos_data = repos_response.json() if repos_response.status_code == 200 else []
    stars = sum(repo.get("stargazers_count", 0) for repo in repos_data if isinstance(repo, dict))
    
    return repos, stars, followers

def calculate_age():
    now = datetime.now()
    age = (now - BIRTHDATE).days / 365.2425
    return f"{age:.4f}"

def main():
    repos, stars, followers = fetch_github_stats()
    age = calculate_age()
    
    # ---------------------------------------------------------
    # PASTE YOUR CUSTOM ASCII ART HERE
    # Generate yours at an image-to-ASCII website (width ~45 chars)
    # ---------------------------------------------------------
    ascii_art = [
        "               .,;:cc::;,.               ",
        "             .ll:'      ':ll.            ",
        "            .o;            ;o.           ",
        "            l;              ;l           ",
        "            l;              ;l           ",
        "            .o;            ;o.           ",
        "             .ll:'      ':ll.            ",
        "               .,;:cc::;,.               ",
        "                                         ",
        "        __   __               _  __      ",
        "        \\ \\ / /__  _   _ ___ (_)/ _|     ",
        "         \\ V / _ \\| | | / __| | |_       ",
        "          | | (_) | |_| \\__ \\ |  _|      ",
        "          |_|\\___/ \\__,_|___/_|_|        ",
        "                                         "
    ]

    # This draws the actual image and sets up Light/Dark mode colors!
    svg_template = f"""<svg width="850" height="420" viewBox="0 0 850 420" fill="none" xmlns="http://www.w3.org/2000/svg">
    <style>
        .bg {{ fill: #ffffff; }}
        .text {{ font-family: "Courier New", Courier, monospace; font-size: 14px; fill: #24292f; white-space: pre; }}
        .title {{ fill: #0969da; font-weight: bold; }}
        .separator {{ fill: #57606a; }}
        
        @media (prefers-color-scheme: dark) {{
            .bg {{ fill: #0d1117; }}
            .text {{ fill: #c9d1d9; }}
            .title {{ fill: #58a6ff; }}
            .separator {{ fill: #8b949e; }}
        }}
    </style>
    <rect width="850" height="420" rx="10" class="bg"/>
    <g class="text">
    """

    # Renders the ASCII art
    y_offset = 40
    for line in ascii_art:
        line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg_template += f'<text x="20" y="{y_offset}">{line}</text>\n'
        y_offset += 16
        
    # Renders the stats
    stats_x = 380
    svg_template += f'''
        <text x="{stats_x}" y="40"><tspan class="title">{USERNAME}@github</tspan></text>
        <text x="{stats_x}" y="56" class="separator">------------------------------------------------</text>
        
        <text x="{stats_x}" y="80"><tspan class="title">OS:</tspan>             Windows 11, Linux</text>
        <text x="{stats_x}" y="96"><tspan class="title">Host:</tspan>           Web Developer</text>
        <text x="{stats_x}" y="112"><tspan class="title">IDE:</tspan>            VSCode</text>
        <text x="{stats_x}" y="128"><tspan class="title">Age:</tspan>            {age}</text>
        
        <text x="{stats_x}" y="160"><tspan class="title">Languages:</tspan>      JavaScript, Python, HTML, CSS</text>
        <text x="{stats_x}" y="176"><tspan class="title">Tools:</tspan>          React, Node.js, Git</text>
        
        <text x="{stats_x}" y="208" class="separator">- Contact --------------------------------------</text>
        <text x="{stats_x}" y="224"><tspan class="title">Email.Work:</tspan>     your.email@example.com</text>
        <text x="{stats_x}" y="240"><tspan class="title">LinkedIn:</tspan>       linkedin.com/in/yousifamr</text>
        
        <text x="{stats_x}" y="272" class="separator">- GitHub Stats ---------------------------------</text>
        <text x="{stats_x}" y="288"><tspan class="title">Repos:</tspan>          {repos}</text>
        <text x="{stats_x}" y="304"><tspan class="title">Stars:</tspan>          {stars}</text>
        <text x="{stats_x}" y="320"><tspan class="title">Followers:</tspan>      {followers}</text>
    </g>
    </svg>'''

    # Saves the image file
    with open("neofetch.svg", "w", encoding="utf-8") as f:
        f.write(svg_template)

if __name__ == "__main__":
    main()
