import pytz
from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.orm import declarative_mixin

utc_timezone = pytz.utc

@declarative_mixin
class Timestamp:
    created_at = Column(DateTime, default=datetime.now(utc_timezone), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(utc_timezone), nullable=False)