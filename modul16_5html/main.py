from fastapi import FastAPI, Path, HTTPException, Path, Request
from typing import List, Annotated
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

    # Создаем экземпляр приложения FastAPI
app = FastAPI()
    # Создайте словарь users
users = []
templates = Jinja2Templates(directory="templates")

class User(BaseModel):
    id: int
    username: str
    age: int

@app.get("/")
async def start_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("user.html", {"request": request, "users": users})


 # 4 CRUD запроса:
@app.get('/user/{user_id}', response_class=HTMLResponse)
async def get_message(request: Request, user_id: int) -> HTMLResponse:
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user.html", {"request": request, "user": user})

@app.post('/user/{username}/{age}')
async def create_user(username: str = Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser'),
                      age: int = Path(ge=18, le=120, description='Enter age', example='77')) -> User:
    user_id = (users[-1].id + 1) if users else 1
    user = User(id=user_id, username=username, age=age)
    users.append(user)
    return user

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(
        username: str = Path(min_length=5, max_length=20, description="Enter username",
                                                     example="UrbanUser"),
        user_id: int = Path(ge=1, le=100, description="Enter User ID", example=1),
        age: int = Path(ge=18, le=120, description="Enter age", example="24")
) -> User:
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Обновляем информацию о пользователе
    user.username = username
    user.age = age
    return user

@app.delete('/user/{user_id}', response_model=User)
async def del_user(
        user_id: Annotated[int, Path(description="Enter User ID")]
       ) -> User:
    try:
        user = next(user for user in users if user.id == user_id)
        users.remove(user)
        return user
    except IndexError:
        raise HTTPException(status_code=404, detail="User not found")