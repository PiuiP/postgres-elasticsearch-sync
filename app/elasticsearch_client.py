from elasticsearch import Elasticsearch
from app.config import ELASTICSEARCH_URL
import logging
from functools import wraps

logger = logging.getLogger(__name__)


ARTICLES_MAPPING = {
    "properties": {
        "id": {"type": "integer"},
        "title": {
            "type": "text",
            "analyzer": "russian",
            "fields": {
                "keyword": {"type": "keyword"}  # для сортировки и агрегаций
            }
        },
        "text": {
            "type": "text",
            "analyzer": "russian"
        },
        "source": {"type": "keyword"},  # для фильтрации по источникам
        "pub_date": {"type": "date"},   # для сортировки по дате
        #для синхронизации
        "created_at": {"type": "date"},
        "updated_at": {"type": "date"}
    }
}

def ensure_connected(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            if not self.es or not self.es.ping():
                logger.warning("Elasticsearch connection lost, attempting to reconnect...")
                self.es = Elasticsearch(ELASTICSEARCH_URL)
                if not self.es.ping():
                    logger.error("Failed to reconnect to Elasticsearch")
                    return False
                logger.info("Successfully reconnected to Elasticsearch")
        except Exception as e:
            logger.error(f"Connection error in {func.__name__}: {e}")
            return False
        
        return func(self, *args, **kwargs)
    return wrapper


class ElasticSearchClient:
    def __init__(self):
        try:
            self.es = Elasticsearch(ELASTICSEARCH_URL)
            if not self.es.ping():
                logger.error("Elasticsearch is not available")
        except Exception as e:
            logger.error(f"Elasticsearch connection error: {e}")
            self.es = None

    @ensure_connected
    def index_exists(self, index_name: str) -> bool:
        return self.es.indices.exists(index=index_name)
    
    @ensure_connected
    def document_exists(self, index_name: str, doc_id: int) -> bool:
        try:
            return self.es.exists(index=index_name, id=doc_id)
        except Exception as e:
            logger.error(f"Failed to check if document {doc_id} exists: {e}")
            return False

    @ensure_connected
    def create(self, index_name: str, mapping: dict = None):
        try:
            if not self.index_exists(index_name):
                self.es.indices.create(index=index_name, mappings=mapping)
                logger.info(f"Index {index_name} created successfully")
                return True
            else:
                logger.info(f"Index {index_name} already exists")
                return True
        except Exception as e:
            logger.error(f"Failed to create index {index_name}: {e}")
            return False

    @ensure_connected
    def index_doc(self, index_name: str, doc: dict, doc_id: int = None):
        """
        doc_id передан и документ существует - обновится
        doc_id передан и документа нет - создастся с этим id
        """
        try:
            response = self.es.index(index=index_name, document=doc, id=doc_id)
            if response.get('result') in ['created', 'updated']:
                logger.debug(f"Document {doc_id} indexed successfully")
                return True
            else:
                logger.error(f"Unexpected response: {response}")
                return False
        except Exception as e:
            logger.error(f"Failed to index document {doc_id}: {e}")
            return False

    @ensure_connected
    def delete_doc(self, index_name: str, doc_id: int):
        try:
            if self.document_exists(index_name, doc_id):
                response = self.es.delete(index=index_name, id=doc_id)
                if response.get('result') == 'deleted':
                    logger.info(f"Document {doc_id} deleted successfully")
                    return True
            else:
                logger.info(f"Document {doc_id} does not exist, nothing to delete")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete document {doc_id}: {e}")
            return False

