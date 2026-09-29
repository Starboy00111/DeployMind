import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")

BASE_URL = "https://api.github.com"


def github_headers():
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_workflow_runs():
    url = (
        f"{BASE_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}/actions/runs"
    )

    response = requests.get(
        url,
        headers=github_headers(),
        params={"per_page": 10},
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def get_failed_run():
    data = get_workflow_runs()

    for run in data["workflow_runs"]:
        if run["conclusion"] == "failure":
            return run

    return None


def get_failed_jobs(run_id):
    url = (
        f"{BASE_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/actions/runs/{run_id}/jobs"
    )

    response = requests.get(
        url,
        headers=github_headers(),
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def get_job_logs(job_id):
    url = (
        f"{BASE_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/actions/jobs/{job_id}/logs"
    )

    response = requests.get(
        url,
        headers=github_headers(),
        timeout=30,
    )

    response.raise_for_status()
    return response.text


if __name__ == "__main__":

    print("========================================")
    print("DeployMind GitHub Deployment Monitor")
    print("========================================")

    run = get_failed_run()

    if not run:
        print("No failed workflow runs found.")
        raise SystemExit

    print()
    print(f"Workflow : {run['name']}")
    print(f"Run      : #{run['run_number']}")
    print(f"Status   : {run['status']}")
    print(f"Result   : {run['conclusion']}")

    print()
    print("Finding failed job...")

    jobs_data = get_failed_jobs(run["id"])

    failed_job = None

    for job in jobs_data["jobs"]:
        if job["conclusion"] == "failure":
            failed_job = job
            break

    if not failed_job:
        print("Failed job could not be found.")
        raise SystemExit

    print(f"Job      : {failed_job['name']}")
    print(f"Job ID   : {failed_job['id']}")

    print()
    print("Downloading job logs...")

    logs = get_job_logs(failed_job["id"])

    print()
    print("========== DEPLOYMENT LOG ==========")
    print(logs)
    print("====================================")