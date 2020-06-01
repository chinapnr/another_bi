from superset.models.baseModel import BaseModel
from flask_appbuilder import Model
from sqlalchemy import (
    Column,
    Integer,
)


class UserDashboardRel(Model, BaseModel):
    __tablename__ = "user_dashboard_rel"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    dashboard_id = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "dashboard_id": self.dashboard_id
        }


