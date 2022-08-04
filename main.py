from fastapi import FastAPI
import uvicorn

from testapi import attention_api, influencers_api, detail_api

def include_router(app):
    app.include_router(detail_api.router, prefix='/app/v1')
    app.include_router(attention_api.router, prefix='/app/v1')
    app.include_router(influencers_api.router, prefix='/app/v1')

def start_application():
    app = FastAPI()
    include_router(app)

    return app

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

app = start_application()
