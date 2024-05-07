from sqlalchemy import Column, String, Text, Integer, DateTime, func, UniqueConstraint
from .moretonbay import Base


class Geelongaustralia(Base):
    __tablename__ = 'geelongaustralia'

    id = Column(Integer, primary_key=True, autoincrement=True)

    app_num = Column(String(255), unique=True, nullable=False)
    vic_smart = Column(String(255),nullable=True,server_default=None)
    lodge_date = Column(Integer, nullable=True)

    address = Column(Text,nullable=True,server_default=None)
    description = Column(Text,nullable=True,server_default=None)
    changes_ = Column(String(255),nullable=True,server_default=None)
    type_ = Column(String(255),nullable=True,server_default=None)
    
    notice_date = Column(Integer, nullable=True)
    authority = Column(String(255),nullable=True,server_default=None)

    decision_date = Column(Integer, nullable=True, server_default=None)
    decision = Column(Text,nullable=True, server_default=None)

    vc_refno = Column(Text, nullable=True, server_default=None)
    vc_decision =Column(Text, nullable=True, server_default=None)
    vc_date = Column(Integer, nullable=True)

    _tid = Column(String(255), nullable=False,server_default=None)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
