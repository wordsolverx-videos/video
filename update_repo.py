import os
import sys
import json
import subprocess
from datetime import datetime

# Configuration
REPO_URL = "https://github.com/wordsolverx-videos/video.git"
REPO_DIR = "wordsolver-video-repo" # Subfolder for the actual git repo
TARGET_DIR = "quordle"

def run_command(command, cwd=None):
    try:
        result = subprocess.run(
            command, cwd=cwd, shell=True, check=True, text=True, capture_output=True
        )
        print(f"Success: {command}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running {command}: {e.stderr}")
        return None

def update_video_repo(video_id):
    # Use the directory where THIS script is located as the base
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_path = os.path.join(script_dir, REPO_DIR)
    
    # Check for PAT in environment (for GitHub Actions)
    pat = os.environ.get("VIDEO_REPO_PAT")
    auth_url = REPO_URL
    if pat:
        # Inject PAT into URL: https://TOKEN@github.com/...
        auth_url = REPO_URL.replace("https://", f"https://{pat}@")

    # 1. Setup Repo (Clone or Pull)
    if not os.path.exists(repo_path):
        print(f"Cloning repo to {repo_path}...")
        run_command(f"git clone {auth_url} {REPO_DIR}", cwd=script_dir)
    else:
        print(f"Pulling latest changes in {repo_path}...")
        run_command("git pull", cwd=repo_path)
    
    # 2. Create Target Directory
    target_path = os.path.join(repo_path, TARGET_DIR)
    if not os.path.exists(target_path):
        os.makedirs(target_path)
        
    # 3. Create JSON File
    today = datetime.now().strftime("%Y-%m-%d")
    json_filename = f"{today}.json"
    json_path = os.path.join(target_path, json_filename)
    
    data = {
        "id": video_id,
        "date": today,
        "platform": "youtube",
        "type": "daily-solve"
    }
    
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
        
    print(f"Created {json_filename} with video ID: {video_id}")
    
    # 4. Commit and Push
    print("Pushing changes...")
    run_command("git add .", cwd=repo_path)
    run_command(f'git commit -m "Add Quordle video for {today}"', cwd=repo_path)
    run_command("git push", cwd=repo_path)
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_repo.py <video_id>")
        sys.exit(1)
    
    video_id = sys.argv[1]
    update_video_repo(video_id)
