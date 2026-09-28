import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

bank_id = os.getenv("HINDSIGHT_BANK_ID")


# ==============================
# Simulated deployment
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
    ],

    "result": "SUCCESS",

    "root_cause": "No failure occurred",

    "resolution": "Database migration was executed separately after staging validation",

    "lesson": "Separating database migrations from application deployment reduced deployment risk"
}


# ==============================
# Create deployment experience
# ==============================

experience = f"""
Deployment Experience

Deployment ID:
{deployment['deployment_id']}

Service:
{deployment['service']}

Version:
{deployment['version']}

Environment:
{deployment['environment']}

Changes:
{', '.join(deployment['changes'])}

Result:
{deployment['result']}

Root Cause:
{deployment['root_cause']}

Resolution:
{deployment['resolution']}

Lesson Learned:
{deployment['lesson']}
"""


print("\n========================================")
print("       DEPLOYMENT RESULT")
print("========================================")

print(f"\nDeployment: {deployment['deployment_id']}")
print(f"Result: {deployment['result']}")

print("\nResolution:")
print(deployment["resolution"])

print("\nLesson:")
print(deployment["lesson"])


# ==============================
# Store result in Hindsight
# ==============================

print("\n🧠 Storing deployment experience in Hindsight...")

result = client.retain(
    bank_id=bank_id,
    content=experience
)

print("\n========================================")
print("       MEMORY UPDATED")
print("========================================")

print("Deployment experience stored successfully!")
print(f"Memory items added: {result.items_count}")

client.close()