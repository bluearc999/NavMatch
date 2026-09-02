import os
from sqlalchemy import create_engine, Column, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Irsaliye(Base):
    __tablename__ = 'irsaliyeler'
    
    irsaliye_no = Column(String, primary_key=True, unique=True, nullable=False)
    musteri_adi = Column(String, nullable=False)
    tutar = Column(Float, nullable=False)
    tarih = Column(DateTime, default=datetime.utcnow)

class Fatura(Base):
    __tablename__ = 'faturalar'
    
    fatura_no = Column(String, primary_key=True, unique=True, nullable=False)
    irsaliye_no = Column(String, nullable=False)  # Eşleştirme için referans
    tutar = Column(Float, nullable=False)
    kdv_orani = Column(Float, nullable=False)
    tarih = Column(DateTime, default=datetime.utcnow)

# SQLite Veritabanı Kurulumu
DB_PATH = 'sqlite:///otomasyon.db'
engine = create_engine(DB_PATH, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
