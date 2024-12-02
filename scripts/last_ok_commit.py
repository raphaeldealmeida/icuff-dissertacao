import subprocess
import json


def get_latest_successful_commit(repo):
    # Step 1: Get the latest runs from the repository
    result = subprocess.run(
        [
            "gh",
            "run",
            "list",
            "-R",
            repo,
            "--limit",
            "30",
            "--json",
            "headSha,conclusion",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Failed to fetch runs")
        return None

    # Step 2: Parse the JSON response
    runs = json.loads(result.stdout)

    # Step 3: Find the latest run where all jobs have succeeded
    for run in runs:
        if run["conclusion"] == "success":
            commit_sha = run["headSha"]
            commit_url = f"https://github.com/{repo}/commit/{commit_sha}"
            return commit_url

    print("No successful commit found")
    return None


if __name__ == "__main__":
    repo = "sebastianbergmann/phpunit"  # Replace 'owner/repo' with the actual repository name
    latest_commit_url = get_latest_successful_commit(repo)

    if latest_commit_url:
        print(f"Latest successful commit: {latest_commit_url}")
