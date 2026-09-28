import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

bank_id = os.getenv("HINDSIGHT_BANK_ID")


def analyze_deployment(deployment):
    query = f"""
    Find previous deployment experiences similar to this deployment.

    Current deployment:
    Service: {deployment['service']}
    Version: {deployment['version']}
    Environment: {deployment['environment']}

    Changes:
    {', '.join(deployment['changes'])}

    Look for:
    - similar services
    - similar changes
    - previous failures
    - previous successes
    - root causes
    - resolutions
    - lessons learned
    """

    result = client.recall(
        bank_id=bank_id,
        query=query
    )

    return result


new_deployment = {
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
print("        DEPLOYMENT ANALYSIS")
print("========================================")

print(f"\nDeployment ID: {new_deployment['deployment_id']}")
print(f"Service: {new_deployment['service']}")
print(f"Version: {new_deployment['version']}")
print(f"Environment: {new_deployment['environment']}")

print("\nChanges:")
for change in new_deployment["changes"]:
    print(f"  - {change}")


print("\n🧠 Searching Hindsight memory...")

memory = analyze_deployment(new_deployment)

print("\n========================================")
print("        HINDSIGHT RESULTS")
print("========================================")

for result in memory.results:
    print(f"\nType: {result.type}")
    print(f"Memory: {result.text}")

client.close()