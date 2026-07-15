import os
import requests
import re
from datetime import datetime

# --- YOUR DETAILS ---
USERNAME = "yousifamr-webdev"
BIRTHDATE = datetime(2003, 1, 1) # <--- Replace with your actual birth date!
# --------------------

def fetch_github_stats():
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    
    # Fetch total repositories
    response = requests.get(f"https://api.github.com/users/{USERNAME}", headers=headers)
    user_data = response.json()
    repos = user_data.get("public_repos", 0)
    
    # Fetch total stars across your repos
    repos_url = f"https://api.github.com/users/{USERNAME}/repos?per_page=100"
    repos_response = requests.get(repos_url, headers=headers)
    repos_data = repos_response.json()
    stars = sum(repo.get("stargazers_count", 0) for repo in repos_data if isinstance(repo, dict))
    
    return repos, stars

def calculate_age():
    now = datetime.now()
    days_in_year = 365.2425
    age = (now - BIRTHDATE).days / days_in_year
    return f"{age:.4f}"

def main():
    repos, stars = fetch_github_stats()
    age = calculate_age()
    
    # The Neofetch Layout
    neofetch_content = f"""```text
      .--------.            {USERNAME}@github
     /        /|            -----------------------
    /        / |            Role: Web Developer
   /________/  |            Host: GitHub
   |        |  |            Age: {age}
   |  < />  |  |            Stars: {stars}
   |        | /             Repos: {repos}
   |________|/              
```"""

    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print("README.md not found!")
        return

    # Injects the stats between the HTML comments in your README
    new_content = re.sub(
        r"<!-- NEOFETCH START -->.*<!-- NEOFETCH END -->",
        f"<!-- NEOFETCH START -->\n{neofetch_content}\n<!-- NEOFETCH END -->",
        content,
        flags=re.DOTALL
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    main()
