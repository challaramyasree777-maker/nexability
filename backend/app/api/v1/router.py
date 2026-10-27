from fastapi import APIRouter

from app.api.v1.endpoints import (
    accessibility,
    accommodation_requests,
    applications,
    auth,
    chat,
    interviews,
    jobs,
    profiles,
    resumes,
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(resumes.router, prefix="/resumes", tags=["resumes"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(accessibility.router, prefix="/accessibility", tags=["accessibility"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(
    accommodation_requests.router,
    prefix="/accommodation-requests",
    tags=["accommodation-requests"],
)
api_router.include_router(interviews.router, prefix="/interviews", tags=["interviews"])
api_router.include_router(chat.router, prefix="/chat", tags=["agent-chat"])
