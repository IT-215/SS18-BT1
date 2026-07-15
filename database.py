from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ==== CONFIG ====
DATABASE_URL = "mysql+pymysql://root:password@localhost:3306/course_registration"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ==== DB SESSION ====
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
