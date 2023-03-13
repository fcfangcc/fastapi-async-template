import datetime

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String, text

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), unique=True, nullable=False)
    nick_name = Column(String(length=64), nullable=False, comment="NickName")
    hashed_password = Column(String(length=128), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    channel = Column(String(length=20), default="InviteCode")

    state = Column(BigInteger, default=0, nullable=False, comment="delete use timstamp")
    create_time = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment="创建时间")
    modified_time = Column(
        DateTime,
        nullable=False,
        onupdate=datetime.datetime.now,
        default=datetime.datetime.now,
        # server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    def __repr__(self) -> str:
        return "<User {0}>".format(self.email)
