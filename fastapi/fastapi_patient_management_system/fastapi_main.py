# !pip install fastapi uvicorn pydantic

from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello World ip"}

@app.get('/about')
def about():
    return {"message": "This is website of Koyel hi"}