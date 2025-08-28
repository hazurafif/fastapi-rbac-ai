import logging
from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Session
from internal.db import Base, get_db
from passlib.hash import bcrypt

logger = logging.getLogger(__name__)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    password_hash = Column(String)
    
class Roles(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    

class Permissions(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    
class RolePermissions(Base):
    __tablename__ = "role_permissions"
    
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)


class UserRoles(Base):
    __tablename__ = "user_roles"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    

class LoginModel(BaseModel):
    email: EmailStr
    password: str
    
class UserRegistrationModel(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserModel(BaseModel):
    name: str
    email: str
    role: Optional[str] = None
    permissions: Optional[list[str]] = None

class UsersTable:
    def insert_new_user(self, user_data: UserRegistrationModel) -> Optional[UserModel]:
        with get_db() as db:
            try:
                hashed_pw = bcrypt.hash(user_data.password)
                new_user = User(
                    name=user_data.name,
                    email=user_data.email,
                    password_hash=hashed_pw,
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                return UserModel(
                    name=user_data.name,
                    email=user_data.email,
                )
            except Exception as e:
                logger.error("error")
                return None
       

    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        with get_db() as db:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return None

            roles = [ur.role for ur in user.roles]
            role_name = roles[0].name if roles else None

            permissions = []
            if roles:
                for r in roles:
                    for rp in r.permissions:
                        permissions.append(rp.permission.name)

            return UserModel(
                name=user.name,
                email=user.email,
                role=role_name,
                permissions=permissions
            )
    
    def authenticate_user(self, email: str, password: str) -> Optional[UserModel]:
        with get_db() as db:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return None

            if not bcrypt.verify(password, user.password_hash):
                return None
           
            return UserModel(
                name=user.name,
                email=user.email,
            )
        
Users = UsersTable()