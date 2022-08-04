from sqlalchemy import Column, ForeignKey
from sqlalchemy import String, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class keywordTable(Base):
    __tablename__ = 'Keyword'
    Keyword = Column(String(58))
    Username = Column(String(58), primary_key=True)
    # raw_data = relationship('rawInfoTable', back_populate='Keyword')
    # pro_data = relationship('processedInfoTable', back_populate='Keyword')

    def __repr__(self):
        return f"<Username {self.Username}"

class processedInfoTable(Base):
    __tablename__ = 'ProcessedInfo'
    RawInfo_Keyword_Username = Column(String(58), primary_key=True)
    Real_Followers = Column(Integer)
    Real_Like_Rate = Column(Float)
    Real_Comment_Rate = Column(Float)
    Real_Influence = Column(Float)
    # keyword = relationship('keywordTable', back_populate='ProcessedInfo')
    # raw_data = relationship('rawInfoTable', back_populate='ProcessedInfo')

    def __repr__(self):
        return f"<Username {self.Username}"

class rawInfoTable(Base):
    __tablename__ = 'RawInfo'
    Keyword_Username = Column(String(58), primary_key=True)
    Followers = Column(Integer)
    Avg_Likes = Column(Integer)
    # keyword = relationship('keywordTable', back_populate='RawInfo')
    # pro_data = relationship('processedInfoTable', back_populate='RawInfo')

    def __repr__(self):
        return f"<Username {self.Username}"

class attentionTable(Base):
    __tablename__ = 'attention'
    # target table name inside the accessed db
    influencer_id = Column(String(100), primary_key = True)
    followers = Column(Integer, nullable = False)
    real_influence = Column(Integer)
#    choices = relationship('choice', back_populates='test')

    def __repr__(self):
        return f"<Influencer {self.influencer_id}"