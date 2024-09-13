from fastapi import FastAPI, APIRouter, Response
from fastapi.responses import JSONResponse
from app.plugins import AskarStorage
from config import settings

app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)


api_router = APIRouter()


@api_router.get("/{namespace}/{identifier}/did.json")
async def get_did_document(response: Response, namespace: str, identifier: str):
    did = f"did:web:{settings.DOMAIN}:{namespace}:{identifier}"
    did_document = await AskarStorage().fetch("did", did)
    response.headers["Content-Type"] = "application/ld+json"
    return did_document


@api_router.get("/contexts/{credential_type}/{version}")
async def get_context(response: Response, credential_type: str, version: str):
    context = await AskarStorage().fetch("context", f"{credential_type}:{version}")
    response.headers["Content-Type"] = "application/ld+json"
    return context


@api_router.get("/entities/{entity_id}/credentials/{credential_id}")
async def get_issued_credential(response: Response, entity_id: str, credential_id: str):
    vc = await AskarStorage().fetch("credential", f"{entity_id}:{credential_id}")
    response.headers["Content-Type"] = "application/ld+json"
    return vc


@api_router.get("/server/status", tags=["Server"], include_in_schema=False)
async def server_status():
    return JSONResponse(status_code=200, content={"status": "ok"})


app.include_router(api_router)
