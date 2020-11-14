from fastapi import FastAPI

from apis import v1

app = FastAPI()
app.include_router(v1, prefix="/v1")
