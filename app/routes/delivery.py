from pathlib import Path

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from app.services import widgets as service

router = APIRouter(tags=["public delivery"])

BUNDLE_PATH = Path(__file__).resolve().parent.parent / "static" / "widget.v1.js"


@router.get("/widget.v1.js", summary="Versioned widget script")
def widget_bundle():
    return Response(
        content=BUNDLE_PATH.read_bytes(),
        media_type="application/javascript",
        headers={"Cache-Control": "public, max-age=31536000, immutable"},
    )


@router.get("/widgets/{widget_id}/config", summary="Public widget config")
def widget_config(widget_id: str, request: Request):
    widget = service.get_public_config(widget_id)
    if widget is None:
        raise HTTPException(status_code=404, detail="Widget not found")

    etag = f'"{widget["id"]}-v{widget["version"]}"'
    headers = {
        "ETag": etag,
        "Cache-Control": "public, max-age=60",
        "Access-Control-Allow-Origin": "*",
    }

    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304, headers=headers)

    return JSONResponse(content=widget, headers=headers)