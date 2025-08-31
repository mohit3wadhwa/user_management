from fastapi import FastAPI, HTTPException, Depends
import requests
from sqlalchemy.orm import Session
from typing import List  # Import List for type hinting
import models, schemas
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# home page
@app.get('/')
def home_page():
    return "this is homepage of user management. Please append /docs to URL to know more"

# Create user
@app.post('/users/', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Read all users
@app.get('/users/', response_model=List[schemas.User])  # Use List instead of list
def read_users(db: Session = Depends(get_db)):
    bot_token = '8495280080:AAFO0oUe9s0NXo3SaZEpvQbooPs-mZd8pQQ'
    chat_id = '8457396696'
    message = db.query(models.User).all()

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    print(response.json())
    return db.query(models.User).all()

# Read user by ID
@app.get('/users/{user_id}', response_model=schemas.User)
def read_student(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update user by ID
@app.put('/users/{user_id}', response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

# Delete user by ID
@app.delete('/users/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"ok": True}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
