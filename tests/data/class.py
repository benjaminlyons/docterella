"""
Test classes for docstring validation testing.
Contains various docstring inconsistencies and one correct example.
All classes are different from those used in the class_prompt examples.
"""

from typing import List, Dict, Any, Optional, Set, Union, Tuple
from datetime import datetime, timedelta
from pathlib import Path


class MessageQueue:
    """Handle message queuing and processing.

    Args:
        queue_name: str
            Name of the message queue.
        max_size: int
            Maximum number of messages in queue.
    """
    def __init__(self, queue_name: str, max_size: int, retry_attempts: int, persistence: bool = True):
        self.queue_name = queue_name
        self.max_size = max_size
        self.retry_attempts = retry_attempts
        self.persistence = persistence


class ImageResizer:
    """Resize and optimize images for web usage.

    Args:
        input_path: int
            Path to input image file.
        quality: str
            Image compression quality setting.
        preserve_metadata: bool
            Whether to keep EXIF data in output.
    """
    def __init__(self, input_path: str, quality: int = 85):
        self.input_path = input_path
        self.quality = quality


class PasswordValidator:
    def __init__(self, min_length: int = 8, require_uppercase: bool = True, 
                 require_numbers: bool = True, special_chars: Optional[str] = None):
        self.min_length = min_length
        self.require_uppercase = require_uppercase
        self.require_numbers = require_numbers
        self.special_chars = special_chars


class NotificationService:
    """Send notifications via multiple channels.

    Args:
        email_enabled: bool
            Whether email notifications are enabled.
        sms_enabled: bool
            Whether SMS notifications are enabled.
        webhook_url: str
            URL for webhook notifications.
        rate_limit: int
            Maximum notifications per minute.
        templates: Dict[str, str]
            Notification template mappings.
    """
    def __init__(self, email_enabled: bool, sms_enabled: bool = False):
        self.email_enabled = email_enabled
        self.sms_enabled = sms_enabled


class HttpClient:
    """HTTP client for making REST API requests.

    Args:
        base_url: str
            The URL.
        timeout: int
            The timeout.
        retries: int
            The retries.
        user_agent: str
            The user agent.
    """
    def __init__(self, base_url: str, timeout: float = 30.0, retries: int = 3, 
                 user_agent: str = "HttpClient/1.0"):
        self.base_url = base_url
        self.timeout = timeout
        self.retries = retries
        self.user_agent = user_agent


class BackupManager:
    """Manage automated backups of files and databases.

    Args:
        backup_directory: str
            Directory where backups will be stored.
        retention_days: int
            Number of days to keep backups.
        compression_enabled: bool
            Whether to compress backup files.
    """
    def __init__(self, backup_directory: str, retention_days: int = 30, 
                 compression_enabled: bool = True, max_backup_size: int = 1073741824):
        self.backup_directory = backup_directory
        self.retention_days = retention_days
        self.compression_enabled = compression_enabled
        self.max_backup_size = max_backup_size

class VideoProcessor:
    """Process video files with various transformations.

    Args:
        codec: List[str]
            Video codec to use for encoding.
        bitrate: int
            Target bitrate in kbps. Defaults to 2000.
        resolution: Tuple[int, int]
            Output resolution as (width, height). Defaults to (1920, 1080).
        audio_enabled: bool
            Whether to include audio track. Defaults to True.
        metadata: Optional[Dict[str, Any]]
            Custom metadata to embed in output. Defaults to None.
    """
    def __init__(self, codec: str, bitrate: int = 2000, resolution: Tuple[int, int] = (1920, 1080),
                 audio_enabled: bool = True, metadata: Optional[Dict[str, Any]] = None):
        self.codec = codec
        self.bitrate = bitrate
        self.resolution = resolution
        self.audio_enabled = audio_enabled
        self.metadata = metadata


class EventScheduler:
    """Schedule and manage recurring events.

    Args:
        timezone: str
            Timezone for event scheduling (e.g., 'UTC', 'America/New_York').
        max_events: int
            Maximum number of events to track simultaneously. Defaults to 1000.
        persist_to_disk: bool
            Whether to save events to disk for persistence. Defaults to False.
        notification_buffer: timedelta
            How far in advance to trigger notifications. Defaults to 15 minutes.
    """
    def __init__(self, timezone: str, max_events: int = 1000, persist_to_disk: bool = False,
                 notification_buffer: timedelta = timedelta(minutes=15)):
        self.timezone = timezone
        self.max_events = max_events
        self.persist_to_disk = persist_to_disk
        self.notification_buffer = notification_buffer


class SearchEngine:
    """Full-text search engine with indexing and ranking.

    Args:
        index_path: Path
            Directory path where search index will be stored.
        language: str
            Language for text processing and stemming. Defaults to 'english'.
        max_results: int
            Maximum number of search results to return. Defaults to 50.
        fuzzy_matching: bool
            Whether to enable fuzzy string matching. Defaults to True.
        boost_factors: Optional[Dict[str, float]]
            Field boost factors for ranking. Defaults to None.
        stop_words: Optional[Set[str]]
            Custom stop words to filter out. Defaults to None.
    """
    def __init__(self, index_path: Path, language: str = 'english', max_results: int = 50,
                 fuzzy_matching: bool = True, boost_factors: Optional[Dict[str, float]] = None,
                 stop_words: Optional[Set[str]] = None):
        self.index_path = index_path
        self.language = language
        self.max_results = max_results
        self.fuzzy_matching = fuzzy_matching
        self.boost_factors = boost_factors
        self.stop_words = stop_words


class MetricsCollector:
    """Collect and aggregate application performance metrics.

    Args:
        collection_interval: float
            Interval between metric collections in seconds. Defaults to 60.0.
        storage_backend: str
            Backend for metric storage ('memory', 'redis', 'influxdb'). Defaults to 'memory'.
        retention_period: timedelta
            How long to retain metrics data. Defaults to 24 hours.
        enable_histograms: bool
            Whether to collect histogram metrics. Defaults to True.
        tags: Optional[Dict[str, str]]
            Default tags to apply to all metrics. Defaults to None.
        batch_size: int
            Number of metrics to batch before writing. Defaults to 100.
    """
    def __init__(self, collection_interval: float = 60.0, storage_backend: str = 'memory',
                 retention_period: timedelta = timedelta(hours=24), enable_histograms: bool = True,
                 tags: Optional[Dict[str, str]] = None, batch_size: int = 100):
        self.collection_interval = collection_interval
        self.storage_backend = storage_backend
        self.retention_period = retention_period
        self.enable_histograms = enable_histograms
        self.tags = tags
        self.batch_size = batch_size