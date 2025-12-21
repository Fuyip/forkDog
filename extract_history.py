import subprocess
import os
from datetime import datetime

OUTPUT_DIR = "monkey_evolution"
FILE_PATH = "monkey_data/monkey.svg"

def extract_history():
    # Get all commits that touched the file
    cmd = ["git", "log", "--pretty=format:%H %at", "--", FILE_PATH]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error getting git log: {result.stderr}")
        return

    commits = result.stdout.strip().split('\n')
    
    print(f"Found {len(commits)} historical versions.")

    for line in commits:
        if not line: continue
        parts = line.split()
        commit_hash = parts[0]
        timestamp = int(parts[1])
        
        dt = datetime.fromtimestamp(timestamp)
        date_str = dt.strftime("%Y-%m-%d_%H-%M")
        
        # Determine unique filename
        filename = f"{date_str}_monkey.svg"
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        # Handle duplicates (multiple commits same minute)
        counter = 1
        while os.path.exists(output_path):
            filename = f"{date_str}_monkey_{counter}.svg"
            output_path = os.path.join(OUTPUT_DIR, filename)
            counter += 1

        # Get file content from that commit
        cmd_show = ["git", "show", f"{commit_hash}:{FILE_PATH}"]
        result_show = subprocess.run(cmd_show, capture_output=True, text=True)
        
        if result_show.returncode == 0:
            with open(output_path, "w") as f:
                f.write(result_show.stdout)
            print(f"Saved: {filename}")
        else:
            print(f"Failed to extract from {commit_hash}")

if __name__ == "__main__":
    extract_history()
