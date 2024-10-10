import psycopg2
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from fastapi.middleware.cors import CORSMiddleware
from typing import List  # Import List from typing

app = FastAPI()

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Add CORS middleware to allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get a new session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Correcting model class to have a single name and age as an integer
class ModelClassget(BaseModel):
    name: str  # Use str for a single name
    age: int   # Assuming age should be an integer

class ModelClassCreate(BaseModel):
    name: str  # Use str for a single name
    age: int   # Assuming age should be an integer

class ModelClassupdate(BaseModel):
    name: str  # Use str for a single name
    age: int   # Assuming age should be an integer
# Specify response model as List[ModelClass]
@app.get("/get-data", response_model=List[ModelClassget])
def get_data(db: SessionLocal = Depends(get_db)):
    try:
        result = db.execute(text("SELECT name, age FROM third.thirdtable;"))
        data = result.fetchall()

        # Map the fetched rows to the ModelClass model
        datas = [ModelClassget(name=row[0], age=row[1]) for row in data]  # row[0] and row[1] should correspond to name and age

        return datas

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# POST method to create new data and insert into database
@app.post("/create-data", response_model=ModelClassCreate)
def create_data(data: ModelClassCreate, db: SessionLocal = Depends(get_db)):
    try:
        # Insert the data into the database
        insert_query = text(f"INSERT INTO third.thirdtable (name, age) VALUES (:name, :age)")
        db.execute(insert_query, {"name": data.name, "age": data.age})
        db.execute(insert_query, {"name": data.name, "age": data.age})
        db.commit()  # Commit the transaction

        return data  # Return the inserted data

    except Exception as e:
        db.rollback()  # Rollback if something goes wrong
        raise HTTPException(status_code=500, detail=str(e))


# DELETE method to delete data from the database by name
@app.delete("/delete-data/{name}")
def delete_data(name: str, db: SessionLocal = Depends(get_db)):
    try:
        # Execute the DELETE query to remove the record with the specified name
        delete_query = text(f"DELETE FROM third.thirdtable WHERE name = :name")
        result = db.execute(delete_query, {"name": name})

        # Check if any row was deleted
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Data with name '{name}' not found.")

        db.commit()  # Commit the transaction

        return {"detail": f"Data with name '{name}' has been deleted."}

    except Exception as e:
        db.rollback()  # Rollback if an error occurs
        raise HTTPException(status_code=500, detail=str(e))

# CREATE TABLE noun_mstr (
#     noun_id VARCHAR PRIMARY KEY,
#     noun VARCHAR NOT NULL,
#     abbreviation VARCHAR,
#     description TEXT,
#     isactive BOOLEAN NOT NULL
# );
