from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

# Subaplicação para v2
app = FastAPI(
    title="User API v2",
    version="2.0",
    description="Versão 2 da API — inclui campos adicionais e comportamento diferente."
)

# ----------------------------
# MODELOS
# ----------------------------
class User(BaseModel):
    id: int
    name: str = Field(..., min_length=2)
    email: Optional[str] = None
    age: Optional[int] = Field(None, ge=0)
    is_active: bool = True


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


# "Banco" em memória
users_db: List[User] = [
    User(id=1, name="Alice", email="alice@example.com", age=25),
    User(id=2, name="Bob", email="bob@example.com", age=30),
]


# ----------------------------
# ENDPOINTS
# ----------------------------

@app.get("/users", response_model=List[User])
def list_users():
    return users_db


@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/users", response_model=User)
def create_user(user: User):
    if any(u.id == user.id for u in users_db):
        raise HTTPException(status_code=400, detail="User ID already exists")
    users_db.append(user)
    return user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, updated_user: User):
    for i, u in enumerate(users_db):
        if u.id == user_id:
            users_db[i] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")


@app.patch("/users/{user_id}", response_model=User)
def partial_update_user(user_id: int, partial_data: UserUpdate):
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated = user.model_copy(update=partial_data.dict(exclude_unset=True))
    for i, u in enumerate(users_db):
        if u.id == user_id:
            users_db[i] = updated
            break
    return updated


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    global users_db
    users_db = [u for u in users_db if u.id != user_id]
    return {"message": f"User {user_id} deleted successfully"}
