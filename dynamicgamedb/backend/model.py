from sqlalchemy import Column, Integer, String, BLOB, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from database import Base

class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)
    title = Column(String(250))
    platform_id = Column(Integer, ForeignKey('platforms.id'))
    platform = relationship("Platform", backref=backref('games'))
    picture = Column(BLOB)
    info = Column(String(500), default="")
    release_date = Column(DateTime)
    developer = Column(String(250), default="")
    publisher = Column(String(250), default="")

    # TODO: change so that it takes a dicitonary instead.
    def __init__(self, title=None, platform=None):
        self.title = title
        self.platform_id = platform.id
        self.platform = platform

    def __repr__(self):
        return '<Game %r>' % (self.title)

class Platform(Base):
    __tablename__ = "platforms"
    id = Column(Integer, primary_key=True)
    name = Column(String(250))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Platform %r>' % (self.name)