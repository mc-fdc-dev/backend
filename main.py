from fastapi import FastAPI, WebSocket

app = FastAPI()


@app.get("/")
def main():
    return {"status": 200, "message": "Hello, World"}
