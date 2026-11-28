from fastapi import APIRouter, Depends, HTTPException, Response

from app.routes.deps import current_user
from app.schemas import WidgetIn
from app.services import widgets as service

router = APIRouter(prefix="/widgets", tags=["widgets (owner)"])


def not_found():
    return HTTPException(status_code=404, detail="Widget not found")


@router.post("", status_code=201, summary="Create a widget")
def create_widget(payload: WidgetIn, user=Depends(current_user)):
    return service.create_widget(user.id, payload)


@router.get("", summary="List my widgets")
def list_widgets(user=Depends(current_user)):
    return service.list_widgets(user.id)


@router.get("/{widget_id}/manage", summary="Get one of my widgets")
def get_widget(widget_id: str, user=Depends(current_user)):
    widget = service.get_widget(user.id, widget_id)
    if widget is None:
        raise not_found()
    return widget


@router.put("/{widget_id}", summary="Replace one of my widgets")
def replace_widget(widget_id: str, payload: WidgetIn, user=Depends(current_user)):
    widget = service.replace_widget(user.id, widget_id, payload)
    if widget is None:
        raise not_found()
    return widget


@router.delete("/{widget_id}", status_code=204, summary="Delete one of my widgets")
def delete_widget(widget_id: str, user=Depends(current_user)):
    if not service.delete_widget(user.id, widget_id):
        raise not_found()
    return Response(status_code=204)

@router.get("/{widget_id}/snippet", summary="Get the embed snippet")
def get_snippet(widget_id: str, user=Depends(current_user)):
    widget = service.get_widget(user.id, widget_id)
    if widget is None:
        raise not_found()
    return {"snippet": service.build_snippet(widget["id"])}