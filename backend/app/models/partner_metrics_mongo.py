"""
Partner Network Metrics - MongoDB Document Models
Stores historical data from Kelkoo, Admedia, MaxBounty APIs
"""

from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Dict, Any
from beanie import Document, Indexed
from pydantic import Field


class PartnerNetworkMetricDoc(Document):
    """Daily metrics from partner networks (Kelkoo, Admedia, MaxBounty)."""
    
    network: Indexed(str)  # "kelkoo", "admedia", "maxbounty"
    date: Indexed(date)
    
    # Core metrics
    leads: int = 0
    revenue: float = 0.0
    currency: str = "USD"  # "EUR" for Kelkoo, "USD" for others
    
    # Additional metrics (network-specific)
    clicks: Optional[int] = None
    impressions: Optional[int] = None
    
    # Store full API response for future reference
    raw_data: Dict[str, Any] = Field(default_factory=dict)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "partner_network_metrics"
        
    class Config:
        json_encoders = {
            date: lambda v: v.isoformat(),
            datetime: lambda v: v.isoformat(),
        }


class AlertHistoryDoc(Document):
    """Stores history of sent alerts for dashboard display."""
    
    network: Indexed(str)
    metric_name: str
    previous_value: float
    current_value: float
    change_percent: float
    direction: str  # "up" or "down"
    
    telegram_sent: bool = True
    telegram_message_id: Optional[int] = None
    
    detected_at: Indexed(datetime)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "alert_history"


class SystemConfigDoc(Document):
    """System configuration stored in database."""
    
    key: Indexed(str, unique=True)
    value: Any
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "system_config"
