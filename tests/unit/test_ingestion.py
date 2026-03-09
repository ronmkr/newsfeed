import pytest
from src.ingestion.collector import IngestionCoordinator
from src.ingestion.models import RawArticle

def test_deduplicate_logic():
    coordinator = IngestionCoordinator()
    articles = [
        RawArticle(title="Same Title", link="http://site1.com/a", source="s1", summary="", published_at=""),
        RawArticle(title="Same Title", link="http://site2.com/b", source="s2", summary="", published_at=""), # Duplicate title
        RawArticle(title="Diff Title", link="http://site1.com/a", source="s1", summary="", published_at=""), # Duplicate URL
        RawArticle(title="Unique", link="http://site3.com/c", source="s3", summary="", published_at="")
    ]
    
    unique = coordinator.deduplicate(articles)
    assert len(unique) == 2
    assert unique[0].title == "Same Title"
    assert unique[1].title == "Unique"
