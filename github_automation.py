import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_AUTOMATION_TOKEN = os.getenv("GITHUB_AUTOMATION_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")

BASE_URL = "https://api.github.com"


def github_headers():
    return {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_AUTOMATION_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def trigger_remediation():
    """
    Trigger the OrderApp remediation workflow.
    """

    url = (
        f"{BASE_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/actions/workflows/deploy.yml/dispatches"
    )

    payload = {
        "ref": "main",
        "inputs": {
            "deployment_mode": "remediate"
        }
    }

    response = requests.post(
        url,
        headers=github_headers(),
        json=payload,
        timeout=30,
    )

    if response.status_code == 204:
        print(
            "GitHub remediation workflow "
            "triggered successfully."
        )
        return True

    print("Failed to trigger remediation.")
    print("Status code:", response.status_code)
    print("Response:", response.text)

    return False


def get_latest_workflow_run():
    """
    Get the latest OrderApp deployment workflow run.
    """

    url = (
        f"{BASE_URL}/repos/"
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
        f"/actions/runs"
    )

    response = requests.get(
        url,
        headers=github_headers(),
        params={
            "per_page": 10
        },
        timeout=30,
    )

    response.raise_for_status()

    runs = response.json()["workflow_runs"]

    for run in runs:

        if run["name"] == "OrderApp Deployment":
            return run

    return None


def wait_for_remediation(
    previous_run_id=None,
    timeout_seconds=120,
    poll_seconds=5,
):
    """
    Wait for the newly triggered remediation workflow
    and return its final result.
    """

    print()
    print("========================================")
    print("Monitoring Remediation")
    print("========================================")

    print("Waiting for GitHub Actions...")

    elapsed = 0

    while elapsed < timeout_seconds:

        run = get_latest_workflow_run()

        if run:

            run_id = run["id"]

            # Make sure we don't accidentally monitor
            # the old failed workflow.

            if (
                previous_run_id is None
                or run_id != previous_run_id
            ):

                print()
                print(
                    f"Run #{run['run_number']}"
                )

                print(
                    f"Status: {run['status']}"
                )

                print(
                    f"Conclusion: {run['conclusion']}"
                )

                # Workflow has completed.

                if run["status"] == "completed":

                    if run["conclusion"] == "success":

                        print()
                        print(
                            "Remediation workflow "
                            "completed successfully."
                        )

                        return {
                            "success": True,
                            "run": run,
                        }

                    else:

                        print()
                        print(
                            "Remediation workflow failed."
                        )

                        return {
                            "success": False,
                            "run": run,
                        }

                print(
                    "Remediation still running..."
                )

        time.sleep(poll_seconds)

        elapsed += poll_seconds

    print()
    print(
        "Timed out waiting for remediation workflow."
    )

    return {
        "success": False,
        "run": None,
    }


if __name__ == "__main__":

    print("========================================")
    print("DeployMind GitHub Automation")
    print("========================================")

    if not GITHUB_AUTOMATION_TOKEN:

        print(
            "ERROR: "
            "GITHUB_AUTOMATION_TOKEN is missing."
        )

        raise SystemExit(1)

    print()
    print("Repository:")
    print(
        f"{GITHUB_OWNER}/{GITHUB_REPO}"
    )

    # Remember the current latest run.

    previous_run = get_latest_workflow_run()

    previous_run_id = (
        previous_run["id"]
        if previous_run
        else None
    )

    print()
    print("Triggering remediation...")

    triggered = trigger_remediation()

    if not triggered:
        raise SystemExit(1)

    result = wait_for_remediation(
        previous_run_id=previous_run_id
    )

    print()
    print("========================================")
    print("FINAL REMEDIATION RESULT")
    print("========================================")

    if result["success"]:

        print("STATUS: SUCCESS")
        print(
            "DeployMind remediation "
            "completed successfully."
        )

    else:

        print("STATUS: FAILED")
        print(
            "DeployMind remediation "
            "did not complete successfully."
        )