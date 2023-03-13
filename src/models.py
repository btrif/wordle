#  Created by btrif Trif on 09-03-2023 , 12:14 PM.


from sqlalchemy import Column, Integer, String

from database import Base


class OxfordEnglishModel(Base):
    __tablename__ = "english_words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True)
    part_of_speech = Column(String)
    definition = Column(String)


    def __repr__(self):
        return f"id: {self.id}, word: {self.word}, PoS Tagging: {self.part_of_speech}, definition: {self.definition} "


class WordleModel(Base):
    __tablename__ = "wordle"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String, index=True)


    def __repr__(self):
        return f"id: {self.id}, word: {self.word}"
