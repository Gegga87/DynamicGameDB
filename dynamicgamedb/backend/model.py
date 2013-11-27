from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from database import Base

class Game(Base):
    __tablename__ = 'games'
    g_id = Column(Integer, primary_key=True)
    title = Column(String(250))
    platform_id = Column(Integer, ForeignKey('platforms.p_id'))
    platform = relationship("Platform", backref=backref('games'))
    picture = Column(String(250))
    info = Column(String(500), default="")
    release_date = Column(DateTime)
    developer = Column(String(250), default="")
    publisher = Column(String(250), default="")

    def __init__(self, title=None, platform=None):
        self.title = title
        self.platform_id = platform.p_id
        self.platform = platform

    def __repr__(self):
        return '<Game %r>' % (self.title)

class Platform(Base):
    __tablename__ = "platforms"
    p_id = Column(Integer, primary_key=True)
    name = Column(String(250))

    def __init__(self, name=None):
        self.name = name

    def __repr__(self):
        return '<Platform %r>' % (self.name)

class Relation(Base):
    __tablename__ = "relations"
    game1_id = Column(Integer, ForeignKey('games.g_id'), primary_key=True)
    game1 = relationship("Game", foreign_keys=[game1_id])
    game2_id = Column(Integer, ForeignKey('games.g_id'), primary_key=True)
    game2 = relationship("Game", foreign_keys=[game2_id])
    count = Column(Integer, default=1)

    def __init__(self, game1, game2):
        self.game1_id = game1.g_id
        self.game2_id = game2.g_id
        self.game1 = game1
        self.game2 = game2

    def __repr__(self):
        return '<Relation g1:%r g2:%r %r>' % (self.game1.title, self.game2.title, self.count)