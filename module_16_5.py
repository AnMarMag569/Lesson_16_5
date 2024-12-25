from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from fastapi.responses import HTMLResponse
from typing import List
from fastapi.templating import Jinja2Templates

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)

templates = Jinja2Templates(directory="templates")
class User(BaseModel):
    id: int
    username: str = Field(..., min_length=5, max_length=20)
    age: int = Field(..., gt=17, lt=100)

users : List[User] = []

@app.get('/', response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})
@app.get('/user/{user_id}', response_class=HTMLResponse)
async def read_users(request: Request, user_id: int):
    for i in users:
        if i.id == user_id:
            return templates.TemplateResponse("users.html", {"request": request, "user": users})
    raise HTTPException(status_code=404, detail="User was not found")

@app.post('/user/{username}/{age}/', response_class=HTMLResponse)
async def post_user(request: Request, username: str, age: int):
    new_id = max((u.id for u in users), default=0) + 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return templates.TemplateResponse("users.html", {"request": request, "user": new_user})

@app.put('/user/{user_id}/{username}/{age}/', response_class=HTMLResponse)
async def update_user(request: Request, user_id: int, username: str, age: int):
    for i in users:
        if i.id == user_id:
            i.username = username
            i.age = age
            return templates.TemplateResponse("users.html", {"request": request, "user": users})
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete('/user/{user_id}', response_class=HTMLResponse)
async def delete_user(request: Request, user_id: int):
    for i, d in enumerate(users):
        if d.id == user_id:
            del users[i]
            return templates.TemplateResponse("users.html", {"request": request, "user": users})
    raise HTTPException(status_code=404, detail="User was not found")

# uvicorn module_16_5:app --reload