import os
from dotenv import load_dotenv
from hindsight_client import Hindsight
from groq import Groq

load_dotenv()

# ==============================
# Connect to Hindsight
# ==============================

hindsight = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

bank_id = os.getenv("HINDSIGHT_BANK_ID")


# ==============================
# Connect to Groq
# ==============================

groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# ==============================
# New Deployment
# ==============================

deployment = {
    "deployment_id": "DEP-002",
    "service": "Payment Service",
    "version": "v2.4.0",
    "environment": "Production",
    "changes": [
        "Database migration",
        "Payment API modification",
        "Docker image update"
    ]
}


print("\n========================================")
print("        DEPLOYMIND AI ANALYSIS")
print("========================================")

print(f"\nDeployment: {deployment['deployment_id']}")
print(f"Service: {deployment['service']}")
print(f"Version: {deployment['version']}")
print(f"Environment: {deployment['environment']}")

print("\nChanges:")

for change in deployment["changes"]:
    print(f"  - {change}")


# ==============================
# Search Hindsight
# ==============================

print("\n🧠 Searching Hindsight memory...")

query = f"""
Find previous deployment experiences similar to this deployment.

Service:
{deployment['service']}

Version:
{deployment['version']}

Environment:
{deployment['environment']}

Changes:
{', '.join(deployment['changes'])}

Look specifically for:
- previous deployment failures
- previous deployment successes
- database migration problems
- root causes
- resolutions
- lessons learned
"""

memory = hindsight.recall(
    bank_id=bank_id,
    query=query
)


# ==============================
# Display memories
# ==============================

print("\n🧠 Historical memories found:")

for item in memory.results:
    print(f"\n[{item.type}]")
    print(item.text)


# ==============================
# Prepare memory for AI
# ==============================

memory_text = "\n".join(
    f"- {item.text}"
    for item in memory.results
)


# ==============================
# Ask Groq AI
# ==============================

print("\n🤖 Asking AI to analyze the deployment...")


prompt = f"""
You are DeployMind, an AI DevOps deployment assistant.

Analyze the current deployment using the historical
experiences retrieved from Hindsight.

CURRENT DEPLOYMENT

Service: {deployment['service']}
Version: {deployment['version']}
Environment: {deployment['environment']}

Changes:
{', '.join(deployment['changes'])}


HISTORICAL HINDSIGHT MEMORIES

{memory_text}


Give your analysis in this format:

RISK LEVEL:
LOW / MEDIUM / HIGH

HISTORICAL EVIDENCE:
Explain which previous deployment is relevant.

MAIN RISK:
Explain the main risk.

RECOMMENDATION:
Give practical actions before production deployment.

VALIDATION REQUIRED:
YES or NO

IMPORTANT:
Do not invent historical events.
Use only the historical evidence provided.
"""


response = groq.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": "You are a careful DevOps deployment analysis agent."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2
)


recommendation = response.choices[0].message.content


# ==============================
# Display AI result
# ==============================

print("\n========================================")
print("        🤖 DEPLOYMIND RECOMMENDATION")
print("========================================")

print(recommendation)


hindsight.close()