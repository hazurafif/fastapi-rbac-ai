from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from internal.db import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True)
    password_hash = Column(String)
    
    roles = relationship("UserRoles", back_populates="user")

class Roles(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    
    permissions = relationship("Permissions", back_populates="role")

class Permissions(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    

class RolePermissions(Base):
    __tablename__ = "role_permissions"
    
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)

    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission")


class UserRoles(Base):
    __tablename__ = "user_roles"
    
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    
    
    user = relationship("User", back_populates="roles")
    role = relationship("Role")

class LoginModel(BaseModel):
    email: EmailStr
    password: str

class UsersTable:
    def insert_new_user(self):
        return

Users = UsersTable()