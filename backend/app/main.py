from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.routes.analytics import router as analytics_router
from app.routes.reminders import router as reminders_router
from app.routes.settings import router as settings_router
from app.routes.tasks import router as tasks_router
from app.scheduler import shutdown_scheduler, start_scheduler


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    start_scheduler()
    try:
        yield
    finally:
        shutdown_scheduler()


app = FastAPI(
    title='SMARTFLOW API',
    version='1.0.0',
    description='Smart task management and workload optimization backend.',
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
app.include_router(tasks_router, prefix='/api')
app.include_router(analytics_router, prefix='/api')
app.include_router(reminders_router, prefix='/api')
app.include_router(settings_router, prefix='/api')


@app.get('/health', tags=['system'], summary='Health check', description='Verifies the SMARTFLOW backend is running and connected to the application service.')
def health_check():
    return {'status': 'ok', 'service': 'SMARTFLOW'}
