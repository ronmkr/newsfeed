from datetime import datetime
from typing import List
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class ClusterDB(Base):
    __tablename__ = "clusters"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    cluster_id: Mapped[str] = mapped_column(String, unique=True)
    main_event: Mapped[str] = mapped_column(String)
    summary_3_bullets: Mapped[List[str]] = mapped_column(JSON, default=[])
    overall_bias: Mapped[float] = mapped_column(Float, default=0.0)
    is_blindspot: Mapped[bool] = mapped_column(Boolean, default=False)
    blindspot_note: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationship to articles
    articles: Mapped[List["ArticleDB"]] = relationship("ArticleDB", back_populates="cluster")

class ArticleDB(Base):
    __tablename__ = "articles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    cluster_id: Mapped[int] = mapped_column(ForeignKey("clusters.id"))
    title: Mapped[str] = mapped_column(String)
    link: Mapped[str] = mapped_column(String)
    source: Mapped[str] = mapped_column(String)
    summary: Mapped[str] = mapped_column(String)
    published_at: Mapped[str] = mapped_column(String)
    bias_score: Mapped[float] = mapped_column(Float, nullable=True)
    ingested_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Back relationship
    cluster: Mapped["ClusterDB"] = relationship("ClusterDB", back_populates="articles")
