import subprocess
import json
import re


def get_test_stats_from_commit(repo, commit_sha):
    # Step 1: Get all run IDs for the commit
    result = subprocess.run(
        [
            "gh",
            "run",
            "list",
            "--commit",
            commit_sha,
            "-R",
            repo,
            "--json",
            "databaseId,displayTitle,workflowName,url",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"Failed to fetch runs for commit: {commit_sha}")
        return None

    runs = json.loads(result.stdout)

    if not runs:
        print(f"No runs found for commit: {commit_sha}")
        return None

    all_stats = []

    # Step 2: Loop through each run and get the logs
    for run in runs:
        run_id = run["databaseId"]
        wf_name = run["workflowName"]
        # Construct the HTML URL manually using the repo and run ID
        run_url = run["url"]
        print(f"Checking Workflow {wf_name} run: {run_url}")

        log_result = subprocess.run(
            ["gh", "run", "view", str(run_id), "--log", "-R", repo],
            capture_output=True,
            text=True,
        )

        if log_result.returncode != 0:
            print(f"Failed to fetch logs for run: {run_id}")
            continue

        logs = log_result.stdout
        # print(logs)

        # Step 3: Parse the logs for test stats (example based on pytest)
        test_stats = re.search(
            # r"(\d+) passed, (\d+) failed, (\d+) warnings? in ([\d\.]+)s", logs
            r"(\d+) passed.*?(\d+) failed.*?(\d+) warnings?.*?in ([\d\.]+)s",
            logs,
        )

        test_commands = re.search(r"(pytest|py\.test)(\s+[^\s]+)*", logs)
        if test_commands:
            print(test_commands.groups())

        if test_stats:
            passed, failed, warnings, time = test_stats.groups()
            stats = {
                "passed": int(passed),
                "failed": int(failed),
                "warnings": int(warnings),
                "time": float(time),
                "run_url": run_url,
            }
            print(stats)
            all_stats.append(stats)

    # Step 4: Return all test statistics
    return all_stats


def print_test_summary(stats, commit_sha):
    if stats:
        total_passed = sum(stat["passed"] for stat in stats)
        total_failed = sum(stat["failed"] for stat in stats)
        total_warnings = sum(stat["warnings"] for stat in stats)
        total_time = sum(stat["time"] for stat in stats)

        print(f"Test statistics for commit {commit_sha}:")
        print(f"Total Passed: {total_passed}")
        print(f"Total Failed: {total_failed}")
        print(f"Total Warnings: {total_warnings}")
        print(f"Total Execution Time: {total_time:.2f} seconds")
        print("\nDetailed Runs:")
        for stat in stats:
            print(f"Run URL: {stat['run_url']}")
            print(
                f"  Passed: {stat['passed']}, Failed: {stat['failed']}, Warnings: {stat['warnings']}, Time: {stat['time']} seconds"
            )
            print()
    else:
        print(f"No test statistics found for commit {commit_sha}.")


if __name__ == "__main__":
    repo = "dask/dask"  # Replace with the actual repository name
    commit_sha = "26cd64ee3cb4753f9adf16ce4bdb1bdc9fce48b8"  # Replace with the commit SHA you want to analyze

    # Fetch and display test stats for all runs associated with the commit
    stats = get_test_stats_from_commit(repo, commit_sha)
    print_test_summary(stats, commit_sha)
