from fastapi import FastAPI
from precognito.work_orders.api import router as workorder_router

app = FastAPI()

app.include_router(workorder_router)
