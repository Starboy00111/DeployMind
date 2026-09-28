import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

load_dotenv()

client = Hindsight(
    base_url=os.getenv("HINDSIGHT_BASE_URL"),
    api_key=os.getenv("HINDSIGHT_API_KEY")
)

bank_id = os.getenv("HINDSIGHT_BANK_ID")

query = """
Find previous deployment experiences involving:
- database migrations
- payment services
- deployment failures
- migration timeouts
- lessons learned
"""

result = client.recall(
    bank_id=bank_id,
    query=query
)

print("\n===== HINDSIGHT MEMORY RECALL =====\n")

print(result)

client.close()