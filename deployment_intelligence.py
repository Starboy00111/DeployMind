import os

from dotenv import load_dotenv
from groq import Groq
from hindsight_client import Hindsight

from github_monitor import (
    get_failed_run,
    get_failed_jobs,
    get_job_logs,
)

from github_automation import (
    trigger_remediation,
    wait_for_remediation,
    get_latest_workflow_run,
)


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
HINDSIGHT_BASE_URL = os.getenv("HINDSIGHT_BASE_URL")
HINDSIGHT_BANK_ID = os.getenv("HINDSIGHT_BANK_ID")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# ============================================================
# INITIALIZE CLIENTS
# ============================================================

hindsight = Hindsight(
    HINDSIGHT_BASE_URL,
    api_key=HINDSIGHT_API_KEY,
)

groq = Groq(
    api_key=GROQ_API_KEY
)


# ============================================================
# GET REAL GITHUB DEPLOYMENT FAILURE
# ============================================================

def get_real_deployment_failure():

    run = get_failed_run()

    if not run:

        print("No failed GitHub Actions run found.")

        return None

    jobs_data = get_failed_jobs(
        run["id"]
    )

    failed_job = None

    for job in jobs_data["jobs"]:

        if job["conclusion"] == "failure":

            failed_job = job

            break

    if not failed_job:

        print("Failed job not found.")

        return None

    logs = get_job_logs(
        failed_job["id"]
    )

    return {
        "workflow": run["name"],
        "run_id": run["id"],
        "run_number": run["run_number"],
        "status": run["status"],
        "conclusion": run["conclusion"],
        "job": failed_job["name"],
        "job_id": failed_job["id"],
        "logs": logs,
    }


# ============================================================
# EXTRACT ERROR
# ============================================================

def extract_error(logs):

    if "Database migration timeout" in logs:

        return "Database migration timeout"

    if "timeout" in logs.lower():

        return "Deployment timeout"

    if "migration" in logs.lower():

        return "Database migration error"

    if "ERROR" in logs:

        return "Deployment error"

    return "Unknown deployment error"


# ============================================================
# EXTRACT ROOT CAUSE
# ============================================================

def extract_root_cause(logs):

    for line in logs.splitlines():

        if "ROOT CAUSE:" in line:

            return (
                line
                .split("ROOT CAUSE:", 1)[1]
                .strip()
                .strip('"')
            )

    return (
        "Root cause not automatically identified."
    )


# ============================================================
# EXTRACT PIPELINE RECOMMENDATION
# ============================================================

def extract_recommended_action(logs):

    for line in logs.splitlines():

        if "RECOMMENDED ACTION:" in line:

            return (
                line
                .split("RECOMMENDED ACTION:", 1)[1]
                .strip()
                .strip('"')
            )

    return (
        "No pipeline recommendation found."
    )


# ============================================================
# RECALL HISTORICAL DEPLOYMENT EXPERIENCE
# ============================================================

def get_historical_memory():

    print()
    print("Searching Hindsight memory...")
    print()

    recall = hindsight.recall(
        HINDSIGHT_BANK_ID,
        """
        Find previous deployment failures related to:

        database migrations,
        migration timeouts,
        production deployment failures,
        root causes,
        resolutions,
        successful follow-up deployments,
        and lessons learned.

        Focus on previous deployment experiences
        that can help solve the current deployment issue.
        """
    )

    memory_parts = []

    for result in recall.results[:5]:

        text = getattr(
            result,
            "text",
            str(result)
        )

        memory_parts.append(text)

    historical_memory = "\n\n".join(
        memory_parts
    )

    print()
    print("Historical memory found:")
    print("----------------------------------------")

    if historical_memory:

        print(historical_memory)

    else:

        print(
            "No historical deployment memory found."
        )

    return historical_memory


# ============================================================
# GROQ DEPLOYMENT ANALYSIS
# ============================================================

def analyze_with_groq(
    deployment_error,
    historical_memory
):

    prompt = f"""
You are DeployMind, a DevOps deployment intelligence agent.

A real GitHub Actions deployment has failed.

CURRENT DEPLOYMENT:

{deployment_error}

HISTORICAL DEPLOYMENT MEMORY:

{historical_memory}

Analyze the current deployment using historical
deployment experience.

Return exactly these sections:

1. ERROR
Identify the current deployment error.

2. HISTORICAL MATCH
Explain whether Hindsight found a similar
previous deployment failure.

3. ROOT CAUSE
Explain the likely root cause using current
evidence and historical evidence.

4. RECOMMENDED FIX
Give a safe and practical remediation procedure.

5. VALIDATION BEFORE RETRY
Explain what should be checked before retrying.

6. LESSON TO REMEMBER
Give the deployment lesson that should be stored
in persistent memory.

IMPORTANT:

- Do not claim the system predicts failure.
- Do not invent information.
- Use current deployment evidence.
- Use Hindsight historical evidence.
- Prefer safe and reversible DevOps actions.
- Do not recommend arbitrary destructive commands.
"""

    print()
    print("Groq analyzing deployment...")

    response = groq.chat.completions.create(

        model="openai/gpt-oss-120b",

        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful DevOps reliability "
                    "and deployment analysis agent."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],

        temperature=0.2,

        max_tokens=1200,
    )

    return response.choices[0].message.content


# ============================================================
# AUTOMATIC REMEDIATION
# ============================================================

def run_automatic_remediation(
    error_type
):

    print()
    print("========================================")
    print("DeployMind Remediation Decision")
    print("========================================")

    # --------------------------------------------------------
    # SAFE REMEDIATION CATALOG
    # --------------------------------------------------------

    if error_type != "Database migration timeout":

        print(
            "No approved automatic remediation "
            "exists for this error."
        )

        print(
            "Manual investigation is required."
        )

        return False

    print(
        "Approved remediation detected."
    )

    print()

    print("Remediation:")
    print(
        "Run database migration separately "
        "before application deployment."
    )

    # --------------------------------------------------------
    # GET CURRENT RUN
    # --------------------------------------------------------

    previous_run = get_latest_workflow_run()

    previous_run_id = None

    if previous_run:

        previous_run_id = previous_run["id"]

        print()

        print(
            f"Current latest GitHub run: "
            f"#{previous_run['run_number']}"
        )

    # --------------------------------------------------------
    # TRIGGER REMEDIATION
    # --------------------------------------------------------

    print()
    print(
        "Triggering GitHub remediation workflow..."
    )

    triggered = trigger_remediation()

    if not triggered:

        print(
            "Failed to trigger remediation."
        )

        return False

    print()

    print(
        "GitHub remediation workflow "
        "triggered successfully."
    )

    # --------------------------------------------------------
    # MONITOR REMEDIATION
    # --------------------------------------------------------

    result = wait_for_remediation(
        previous_run_id=previous_run_id
    )

    # --------------------------------------------------------
    # CHECK RESULT
    # --------------------------------------------------------

    if result["success"]:

        print()
        print("========================================")
        print("AUTOMATIC REMEDIATION SUCCESS")
        print("========================================")

        print(
            "GitHub remediation completed successfully."
        )

        return True

    print()
    print("========================================")
    print("AUTOMATIC REMEDIATION FAILED")
    print("========================================")

    print(
        "GitHub remediation did not "
        "complete successfully."
    )

    return False


# ============================================================
# STORE DEPLOYMENT LEARNING IN HINDSIGHT
# ============================================================

def remember_deployment_outcome(
    failure,
    error_type,
    remediation_success
):

    print()
    print("========================================")
    print("Learning From Deployment Outcome")
    print("========================================")

    # --------------------------------------------------------
    # SUCCESSFUL REMEDIATION
    # --------------------------------------------------------

    if remediation_success:

        outcome = f"""
Deployment learning event:

Application:
OrderApp

Workflow:
{failure["workflow"]}

Original Failed Run:
#{failure["run_number"]}

Failure:
{error_type}

Remediation:
Database migration was handled separately
before application deployment.

Outcome:
SUCCESS

Lesson:
Separating database migration from application
deployment resolved the deployment issue.

Future deployments with similar database
migration timeout patterns should validate
and execute migrations separately before
application deployment.
"""

    # --------------------------------------------------------
    # FAILED REMEDIATION
    # --------------------------------------------------------

    else:

        outcome = f"""
Deployment learning event:

Application:
OrderApp

Workflow:
{failure["workflow"]}

Original Failed Run:
#{failure["run_number"]}

Failure:
{error_type}

Remediation:
Database migration remediation was attempted.

Outcome:
FAILURE

Lesson:
The approved database migration remediation
did not successfully complete the deployment.

Future analysis should investigate the new
failure before attempting another retry.
"""

    print(
        "Storing deployment outcome in Hindsight..."
    )

    # IMPORTANT:
    # hindsight-client 0.10.1 uses retain(),
    # not remember().

    hindsight.retain(
        HINDSIGHT_BANK_ID,
        outcome,
    )

    print()

    print(
        "Deployment outcome stored in Hindsight."
    )


# ============================================================
# MAIN DEPLOYMIND EXECUTION
# ============================================================

print("========================================")
print("DeployMind Intelligence Agent")
print("========================================")


try:

    # --------------------------------------------------------
    # STEP 1 — DETECT REAL FAILURE
    # --------------------------------------------------------

    failure = get_real_deployment_failure()

    if not failure:

        raise SystemExit


    # --------------------------------------------------------
    # STEP 2 — EXTRACT FAILURE INFORMATION
    # --------------------------------------------------------

    error_type = extract_error(
        failure["logs"]
    )

    root_cause = extract_root_cause(
        failure["logs"]
    )

    pipeline_recommendation = (
        extract_recommended_action(
            failure["logs"]
        )
    )


    print()
    print("REAL DEPLOYMENT FAILURE DETECTED")
    print("----------------------------------------")

    print(
        f"Workflow : "
        f"{failure['workflow']}"
    )

    print(
        f"Run      : "
        f"#{failure['run_number']}"
    )

    print(
        f"Job      : "
        f"{failure['job']}"
    )

    print(
        f"Error    : "
        f"{error_type}"
    )

    print(
        f"Root Cause: "
        f"{root_cause}"
    )

    print(
        f"Pipeline Action: "
        f"{pipeline_recommendation}"
    )


    # --------------------------------------------------------
    # STEP 3 — PREPARE DEPLOYMENT CONTEXT
    # --------------------------------------------------------

    deployment_error = f"""
Deployment: OrderApp

Workflow:
{failure["workflow"]}

Run:
#{failure["run_number"]}

Status:
{failure["conclusion"].upper()}

Failed Job:
{failure["job"]}

Detected Error:
{error_type}

Root Cause From Pipeline:
{root_cause}

Pipeline Recommended Action:
{pipeline_recommendation}
"""


    # --------------------------------------------------------
    # STEP 4 — RECALL HINDSIGHT MEMORY
    # --------------------------------------------------------

    historical_memory = (
        get_historical_memory()
    )


    # --------------------------------------------------------
    # STEP 5 — GROQ ANALYSIS
    # --------------------------------------------------------

    analysis = analyze_with_groq(
        deployment_error,
        historical_memory
    )


    print()
    print("========================================")
    print("DEPLOYMIND ANALYSIS")
    print("========================================")

    print(analysis)


    # --------------------------------------------------------
    # STEP 6 — AUTOMATIC REMEDIATION
    # --------------------------------------------------------

    remediation_success = (
        run_automatic_remediation(
            error_type
        )
    )


    # --------------------------------------------------------
    # STEP 7 — LEARN FROM RESULT
    # --------------------------------------------------------

    remember_deployment_outcome(
        failure,
        error_type,
        remediation_success
    )


    # --------------------------------------------------------
    # STEP 8 — FINAL SUMMARY
    # --------------------------------------------------------

    print()
    print("========================================")
    print("DEPLOYMIND EXECUTION SUMMARY")
    print("========================================")

    print(
        "Failure detected       : YES"
    )

    print(
        "Hindsight memory       : YES"
    )

    print(
        "Groq analysis          : YES"
    )

    print(
        "Remediation triggered  : YES"
    )

    print(
        "Remediation successful : "
        + (
            "YES"
            if remediation_success
            else "NO"
        )
    )

    print(
        "Outcome stored         : YES"
    )

    print()

    print(
        "DeployMind execution completed."
    )

    print(
        "========================================"
    )


finally:

    # --------------------------------------------------------
    # CLOSE HINDSIGHT CLIENT
    # --------------------------------------------------------

    try:

        hindsight.close()

    except Exception:

        pass