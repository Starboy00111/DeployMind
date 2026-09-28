import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

bank_id = os.getenv("HINDSIGHT_BANK_ID")

deployment = """
Deployment ID: DEP-001

Service: Payment Service
Version: v2.3.0
Environment: Production

Changes:
- Database migration
- Payment API changes
- Docker image update

Result: FAILED

Root Cause:
Database migration timed out during deployment.

Resolution:
The database migration was executed separately before
deploying the application.

Lesson Learned:
Large database migrations should be tested in staging
before production deployment.

Tags:
database migration, payment service, deployment failure
"""

result = client.retain(
    bank_id=bank_id,
    content=deployment
)

print("Deployment memory stored successfully!")
print("Memory:", result)

client.close()