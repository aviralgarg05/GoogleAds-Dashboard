"""
Partner Network Metrics Model
Stores historical data from Kelkoo, Admedia, MaxBounty APIs
"""

import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, DateTime, Date, Integer, Numeric, JSON, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PartnerNetworkMetric(Base):
    """Daily metrics from partner networks (Kelkoo, Admedia, MaxBounty)."""
    
    __tablename__ = "partner_network_metrics"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    network: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )  # "kelkoo", "admedia", "maxbounty"
    
    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True
    )
    
    # Core metrics
    leads: Mapped[int] = mapped_column(
        Integer,
        default=0
    )
    revenue: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        default=0
    )
    currency: Mapped[str] = mapped_column(
        String(3),
        default="USD"
    )  # "EUR" for Kelkoo, "USD" for others
    
    # Additional metrics (network-specific)
    clicks: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )
    impressions: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )
    
    # Store full API response for future reference
    raw_data: Mapped[dict] = mapped_column(
        JSON,
        default=dict
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    
    # Composite index for common queries
    __table_args__ = (
        Index("ix_partner_metrics_network_date", "network", "date"),
    )
    
    def __repr__(self) -> str:
        return f"<PartnerNetworkMetric {self.network} {self.date}: {self.leads} leads, {self.revenue} {self.currency}>"


class AlertHistory(Base):
    """Stores history of sent alerts for dashboard display."""
    
    __tablename__ = "alert_history"
    
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    network: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )
    metric_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    previous_value: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False
    )
    current_value: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False
    )
    change_percent: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )
    direction: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )  # "up" or "down"
    
    telegram_sent: Mapped[bool] = mapped_column(
        default=True
    )
    telegram_message_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )
    
    detected_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )
    
    def __repr__(self) -> str:
        return f"<AlertHistory {self.network} {self.metric_name}: {self.change_percent}%>"
