from sqlalchemy import (
    Column,
    Index,
    Integer,
    Float,
    Text,
    String,
    Unicode,
    Boolean,
    ForeignKey,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class PlayerRoles(Base):
    __tablename__ = 'playerroles'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    label = Column(String)

    def __init__(self, name, label):
        self.name = name
        self.label = label


class Teams(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    shortname = Column(Unicode(4))
    fullname = Column(Unicode)

    def __init__(self, shortname, fullname):
        self.shortname = shortname
        self.fullname = fullname


class Player(Base):
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True)
    role_id = Column(Integer, ForeignKey('playerroles.id'))
    team_id = Column(Integer, ForeignKey('teams.id'))
    first_name = Column(Unicode(50))
    last_name = Column(Unicode(50))
    active = Column(Boolean, default=True)

    def __init__(self, role_id, team_id, first_name, last_name, active):
        self.role_id = role_id
        self.team_id = team_id
        self.first_name = first_name
        self.last_name = last_name
        self.active = active


class Statistics(Base):
    __tablename__ = 'statistics'
    
    id = Column(Integer, primary_key=True)
    season = Column(String(9), primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    played = Column(Integer)
    average = Column(Float)
    assists = Column(Integer)
    selfgoals = Column(Integer)
    goalsfor = Column(Integer)
    goalsagainst = Column(Integer)
    penaltiessaved = Column(Integer)
    penaltiesscored = Column(Integer)
    penaltieswrong = Column(Integer)
    yellowcards = Column(Integer)
    redcards = Column(Integer)

    def __init__(self, season, player_id, played, average, assists, selfgoals, goalsfor,
                 goalsagainst, penaltiessaved, penaltiesscored, penaltieswrong, 
                 yellowcards, redcards):
        self.season = season
        self.player_id = player_id
        self.played = played
        self.average = average
        self.assists = assists
        self.selfgoals = selfgoals
        self.goalsfor = goalsfor
        self.goalsagainst = goalsagainst
        self.penaltiessaved = penaltiessaved
        self.penaltiesscored = penaltiesscored
        self.penaltieswrong = penaltieswrong
        self.yellowcards = yellowcards
        self.redcards = redcards
