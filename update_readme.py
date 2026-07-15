import os
import requests
import time
from datetime import datetime

# --- YOUR DETAILS ---
USERNAME = "yousifamr-webdev"
BIRTHDATE = datetime(2003, 1, 1) # Edit to your exact birth date!
# --------------------

def fetch_github_stats():
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    # 1. Fetch public repositories (excluding forks)
    repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100&type=owner"
    repos_response = requests.get(repos_url, headers=headers)
    
    if repos_response.status_code != 200:
        print("Failed to fetch repositories.")
        return 0, 0, 0
        
    repos_data = repos_response.json()
    original_repos = [repo for repo in repos_data if not repo.get("fork", False)]
    total_repos = len(original_repos)
    
    total_commits = 0
    total_loc = 0
    
    # 2. Iterate through each repo to calculate commits and lines of code
    for repo in original_repos:
        repo_name = repo["name"]
        
        stats_url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/stats/contributors"
        stats_response = requests.get(stats_url, headers=headers)
        
        # GitHub's stats API returns 202 if it needs a moment to calculate stats.
        if stats_response.status_code == 202:
            time.sleep(2)
            stats_response = requests.get(stats_url, headers=headers)
            
        if stats_response.status_code == 200:
            contributors = stats_response.json()
            for contributor in contributors:
                # Match your exact username
                if contributor["author"]["login"].lower() == USERNAME.lower():
                    total_commits += contributor["total"]
                    for week in contributor["weeks"]:
                        total_loc += week["a"]  # 'a' stands for lines added
                        
    return total_repos, total_commits, total_loc

def calculate_age():
    now = datetime.now()
    age = (now - BIRTHDATE).days / 365.2425
    return f"{age:.4f}"

def main():
    repos, commits, loc = fetch_github_stats()
    age = calculate_age()
    
    # Format large numbers with commas (e.g., 1,000)
    formatted_commits = f"{commits:,}"
    formatted_loc = f"{loc:,}"
    
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

        <text x="60" y="184">        __...__..............._.._      </text>
        <text x="60" y="200">        \\ \\ / /__.._..._.___(_)/ _|     </text>
        <text x="60" y="216">         .\\ V / _ \\| | | / __| | |_.      </text>
        <text x="60" y="232">          ..| | (_) | |_| \\__ \\ |  _|.      </text>
        <text x="60" y="248">          ..|_|\\___/ \\__,_|___/_|_|..      </text>
        <text x="60" y="264">                                         </text>

        <text x="380" y="40"><tspan class="title">yousifamr-webdev@github</tspan></text>
        <text x="380" y="56" class="separator">------------------------------------------------</text>
        
        <text x="380" y="80"><tspan class="title">OS:</tspan>                     Caffeine</text>
        <text x="380" y="96"><tspan class="title">Uptime:</tspan>                 {age}</text>
        <text x="380" y="112"><tspan class="title">Role:</tspan>                   Web Developer</text>
        <text x="380" y="128"><tspan class="title">IDE:</tspan>                    VSCode</text>
        
        <text x="380" y="160"><tspan class="title">Languages.Programming:</tspan>   JavaScript, Python</text>
        <text x="380" y="176"><tspan class="title">Languages.Computer:</tspan>      HTML, CSS</text>
        <text x="380" y="192"><tspan class="title">Languages.Real:</tspan>          Arabic, English</text>
        
        <text x="380" y="224"><tspan class="title">Tools.Framework:</tspan>         React, NextJS, Express, NestJS</text>
        <text x="380" y="240"><tspan class="title">Tools.Workspace:</tspan>         Git, GitHub, Docker, Postman, Figma</text>
        
        <text x="380" y="272" class="separator">- Contact --------------------------------------</text>
        <text x="380" y="288"><tspan class="title">Email.Personal:</tspan>          yousifamr811@gmail.com</text>
        <text x="380" y="304"><tspan class="title">LinkedIn:</tspan>                linkedin.com/in/yousif-amr-b065723bb</text>
        
        <text x="380" y="336" class="separator">- GitHub Stats ---------------------------------</text>
        <text x="380" y="352"><tspan class="title">Repos:</tspan>                   {repos}</text>
        <text x="380" y="368"><tspan class="title">Commits:</tspan>                 {formatted_commits}</text>
        <text x="380" y="384"><tspan class="title">LinesOfCodeWritten:</tspan>      {formatted_loc}</text>
    </g>
    </svg>"""

    with open("neofetch.svg", "w", encoding="utf-8") as f:
        f.write(svg_template)

if __name__ == "__main__":
    main()
