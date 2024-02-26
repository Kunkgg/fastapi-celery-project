from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from project.database import Base


class WhiteboxReport(Base):
    __tablename__ = "whitebox_reports"

    id = Column(Integer, primary_key=True, autoincrement=True)
    search_version = Column(String(128), unique=False, nullable=False)
    group_name = Column(String(128), unique=False, nullable=False)
    b_version = Column(String(128), unique=False, nullable=False)
    user = Column(String(128), unique=False, nullable=False)
    status = Column(String(128), unique=False, nullable=False)
    check_options = Column(String(128), unique=False, nullable=False)
    created_time = Column(DateTime, nullable=False, default=datetime.utcnow)

    email = Column(String(128), unique=True, nullable=False)

    def __init__(self, username, email, *args, **kwargs):
        self.username = username
        self.email = email