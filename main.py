# install packages -> pip3 install fastapi uvicorn[standard]
# how to run -> uvicorn main:app --reload

import uvicorn
from typing import List
from uuid import UUID
from fastapi import FastAPI, HTTPException
from models import Gender, User, Role, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("74ef52b9-62d0-42ce-bb62-af7f8faa2d08"), 
        first_name="First", 
        last_name="Last", 
        gender=Gender.female,
        roles=[Role.student]
    ),
    User(
        id=UUID("31c51afd-4eaa-4e9c-8139-d8d808094691"), 
        first_name="First Teste", 
        last_name="Last Teste", 
        gender=Gender.male,
        roles=[Role.admin, Role.user]
    )
]

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/api/v1/users")
async def fetch_user():
    return db

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException (
        status_code = 404,
        detail = f"User with id: {user_id} does not exist"
    )
    
@app.put("/api/v1/users/{user_id}")
async def update_user(user_id: UUID, user_update: UserUpdateRequest):
    for user in db:
        if user.id == user_id:
            for key, value in user_update.dict().items():
                if value is not None:
                    setattr(user, key, value)
            return
    raise HTTPException (
        status_code = 404,
        detail = f"User with id: {user_id} does not exist"
    )
    
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 