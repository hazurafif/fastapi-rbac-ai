import logging

from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, Session
from internal.db import Base, get_db
from passlib.hash import bcrypt
from datetime import datetime

logger = logging.getLogger(__name__)


class Generation(Base):
    __tablename__ = "generations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    generation = Column(Text)
    created_at = Column(String)
    updated_at = Column(String)
    score = Column(Integer)


class GenerationModel(BaseModel):
    id: int
    user_id: str
    generation: str
    created_at: str
    updated_at: Optional[str] = None
    score: Optional[int] = None
    

class GenerationsTable:
    def insert_new_generation(self, data: GenerationModel) -> Optional[GenerationModel]:
        with get_db() as db:
            try:
                new_generation = Generation(
                    user_id=data.user_id,
                    generation=data.generation,
                    created_at=datetime.now(),
                )
                db.add(new_generation)
                db.commit()
                db.refresh(new_generation)
                return Generation(
                    generation=data.generation,
                )
            except Exception as e:
                logger.error("error")
                return None
    
    def get_generation_by_id(self):
        return None
    
    def update_generation_score(self):
        return None
    
    def delete_generation_by_id(self):
        return None
        
Generations = GenerationsTable()