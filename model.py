from sqlalchemy import Column, Integer, String
from database import Base, engine

class Task(Base):
    __tablename__ = "tasks"
#
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    assignee_name = Column(String(255), nullable=False)
    priority = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)

Base.metadata.create_all(bind=engine)
