import os

POSTGRES_DB_URL = os.getenv("POSTGRES_DB_URL")
ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")

SYNC_INTERVAL_SECONDS = int(os.getenv("SYNC_INTERVAL_SECONDS", 30))

ARTICLES_INDEX: str = "articles"
RISKS_INDEX: str = "risks"
ENTITIES_INDEX: str = "entities"
CLUSTERS_INDEX: str = "clusters"

LAST_SYNC_FILE: str = os.getenv("LAST_SYNC_FILE", "last_sync.txt")
