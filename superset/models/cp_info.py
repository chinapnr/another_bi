from datetime import datetime
from superset.models.baseModel import BaseModel
from flask_appbuilder import Model
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String
)
from superset.models.helpers import ExtraJSONMixin


class CpInfo(Model, BaseModel):
    __tablename__ = "cp_info"
    id = Column(Integer, primary_key=True)
    cp_name = Column(String(100), nullable=False)
    short_name = Column(String(100), nullable=False)
    app_token = Column(String(200), nullable=False)
    app_key = Column(String(100), nullable=False)
    role_name = Column(String(100), nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": "id",
            "cp_name": self.cp_name,
            "short_name": self.short_name,
            "app_token": self.app_token,
            "app_key": self.app_key,
            "role_name": self.role_name,
            "create_time": self.create_time
        }


