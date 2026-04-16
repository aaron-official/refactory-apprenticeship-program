"""
FastAPI Application Entry Point
-------------------------------
Defines the Todo API routes and integrates database models and schemas.
"""
from fastapi import FastAPI, Depends, HTTPException
from scalar_fastapi import get_scalar_api_reference
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo API", docs_url=None, redoc_url=None)

@app.get("/docs", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

@app.get("/todos", response_model=list[schemas.TodoResponse])
def get_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()

@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/todos", response_model=schemas.TodoResponse, status_code=201)
def create_todo(payload: schemas.TodoCreate, db: Session = Depends(get_db)):
    new_todo = models.Todo(**payload.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.put("/todos/{todo_id}", response_model=schemas.TodoResponse)
def update_todo(todo_id: int, payload: schemas.TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(todo, field, value)

    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()