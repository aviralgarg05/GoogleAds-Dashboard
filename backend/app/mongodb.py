"""
TellSpike Backend - MongoDB Configuration

Async MongoDB setup with Motor driver.
"""

import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import Optional

logger = logging.getLogger(__name__)

# MongoDB connection
_client: Optional[AsyncIOMotorClient] = None
_db = None

# Check if MongoDB is configured
MONGODB_URL = os.getenv("MONGODB_URL", "")
MONGODB_CONFIGURED = bool(MONGODB_URL and "mongodb" in MONGODB_URL)


def get_mongodb_url() -> str:
    """Get MongoDB connection URL."""
    return MONGODB_URL


async def init_mongodb():
    """Initialize MongoDB connection and Beanie ODM."""
    global _client, _db
    
    if not MONGODB_CONFIGURED:
        logger.warning("MongoDB not configured - set MONGODB_URL environment variable")
        return False
    
    try:
        # Create motor client
        _client = AsyncIOMotorClient(MONGODB_URL)
        
        # Get database name from URL or use default
        db_name = os.getenv("MONGODB_DB_NAME", "tellspike")
        _db = _client[db_name]
        
        # Initialize Beanie with document models
        from app.models.partner_metrics_mongo import (
            PartnerNetworkMetricDoc,
            AlertHistoryDoc,
            SystemConfigDoc
        )
        
        await init_beanie(
            database=_db,
            document_models=[
                PartnerNetworkMetricDoc,
                AlertHistoryDoc,
                SystemConfigDoc
            ]
        )
        
        logger.info(f"MongoDB connected successfully to database: {db_name}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        _client = None
        _db = None
        return False


async def close_mongodb():
    """Close MongoDB connection."""
    global _client, _db
    
    if _client is not None:
        _client.close()
        _client = None
        _db = None
        logger.info("MongoDB connection closed")


def get_database():
    """Get the MongoDB database instance."""
    if _db is None:
        raise RuntimeError("MongoDB not initialized. Call init_mongodb() first.")
    return _db


def get_client() -> Optional[AsyncIOMotorClient]:
    """Get the MongoDB client instance."""
    return _client
