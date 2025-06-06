"""
Main FastAPI application for IV Spike Notifier
Handles API endpoints and background monitoring scheduler
"""
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

# Import internal modules
from config import SCAN_INTERVAL_SECONDS, LOG_LEVEL, LOG_FORMAT
from app.data_simulator import fetch_option_data, get_simulation_stats
from app.detector import detect_spikes, get_detector_stats, get_recent_spikes
from app.notifier import send_multiple_spike_alerts, test_notifications, get_notification_stats

# Configure logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# Global scheduler
scheduler = AsyncIOScheduler()

async def monitor_iv_spikes():
    """
    Main monitoring function - fetches data, detects spikes, sends notifications
    This runs periodically in the background
    """
    try:
        logger.info("Starting IV spike monitoring cycle...")

        # Fetch option chain data
        options_data = fetch_option_data()
        if not options_data:
            logger.warning("No option data received")
            return

        # Debug: log keys of first option data item
        if options_data:
            logger.info(f"Option data keys sample: {list(options_data[0].keys())}")

        # Detect IV spikes
        spikes = detect_spikes(options_data)

        if spikes:
            logger.info(f"Detected {len(spikes)} IV spikes")
            success = send_multiple_spike_alerts(spikes)
            if success:
                logger.info("Spike notifications sent successfully")
            else:
                logger.error("Failed to send spike notifications")
        else:
            logger.debug("No IV spikes detected in this cycle")

    except Exception as e:
        logger.error(f"Error in monitoring cycle: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown"""
    logger.info("🚀 Starting IV Spike Notifier...")

    # Start scheduler
    scheduler.add_job(
        monitor_iv_spikes,
        trigger=IntervalTrigger(seconds=SCAN_INTERVAL_SECONDS),
        id='iv_monitor',
        name='IV Spike Monitor',
        replace_existing=True
    )
    scheduler.start()
    logger.info(f"📊 Scheduler started - monitoring every {SCAN_INTERVAL_SECONDS} seconds")

    # Optional: test notification on startup
    await asyncio.sleep(1)
    if test_notifications():
        logger.info("✅ Notification system tested successfully")
    else:
        logger.warning("⚠️ Notification system test failed")

    yield

    # Shutdown
    logger.info("🛑 Shutting down IV Spike Notifier...")
    scheduler.shutdown()

# Create FastAPI app
app = FastAPI(
    title="IV Spike Notifier",
    description="Real-time NSE F&O Options IV Spike Detection and Notification System",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "running",
        "service": "IV Spike Notifier",
        "timestamp": datetime.now().isoformat(),
        "monitoring_active": scheduler.running
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "scheduler_running": scheduler.running,
        "jobs_count": len(scheduler.get_jobs()),
        "uptime": "N/A",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/stats")
async def get_stats():
    """Get comprehensive system statistics"""
    try:
        return {
            "timestamp": datetime.now().isoformat(),
            "simulation": get_simulation_stats(),
            "detector": get_detector_stats(),
            "notifications": get_notification_stats(),
            "scheduler": {
                "running": scheduler.running,
                "jobs": len(scheduler.get_jobs()),
                "scan_interval": SCAN_INTERVAL_SECONDS
            }
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recent-spikes")
async def get_recent_spike_alerts(limit: int = 10):
    """Get recent IV spike alerts"""
    try:
        spikes = get_recent_spikes(limit)
        return {
            "count": len(spikes),
            "spikes": [
                {
                    "symbol": spike.symbol,
                    "strike": spike.strike,
                    "expiry": spike.expiry,
                    "option_type": spike.option_type,
                    "old_iv": spike.old_iv,
                    "new_iv": spike.new_iv,
                    "change_percent": spike.change_percent,
                    "timestamp": spike.timestamp
                }
                for spike in spikes
            ]
        }
    except Exception as e:
        logger.error(f"Error getting recent spike alerts: {e}")
        raise HTTPException(status_code=500, detail=str(e))
