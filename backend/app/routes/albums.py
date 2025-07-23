from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional
import uuid

from app.database.albums import (
    db_create_albums_table,
    db_create_album_images_table,
    db_get_all_albums,
    db_get_album,
    db_insert_album,
    db_update_album,
    db_delete_album,
    db_get_album_images,
    db_add_images_to_album,
    db_remove_image_from_album,
    db_remove_images_from_album
)

router = APIRouter()

@router.on_event("startup")
def startup():
    db_create_albums_table()
    db_create_album_images_table()

@router.get("/")
def get_albums(show_hidden: bool = Query(False)):
    albums = db_get_all_albums(show_hidden)
    return {"success": True, "albums": albums}

@router.post("/")
def create_album(
    name: str = Body(...),
    description: Optional[str] = Body(""),
    is_hidden: bool = Body(False),
    password: Optional[str] = Body(None)
):
    album_id = str(uuid.uuid4())
    db_insert_album(album_id, name, description, is_hidden, password)
    return {"success": True, "album_id": album_id}

@router.get("/{album_id}")
def get_album(album_id: str):
    album = db_get_album(album_id)
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    return {"success": True, "data": album}

@router.put("/{album_id}")
def update_album(
    album_id: str,
    name: str = Body(...),
    description: str = Body(""),
    is_hidden: bool = Body(False),
    password: Optional[str] = Body(None)
):
    db_update_album(album_id, name, description, is_hidden, password)
    return {"success": True, "msg": "Album updated successfully"}

@router.delete("/{album_id}")
def delete_album(album_id: str):
    db_delete_album(album_id)
    return {"success": True, "message": "Album deleted successfully"}

@router.get("/{album_id}/images")
def get_album_images(album_id: str):
    images = db_get_album_images(album_id)
    return {"success": True, "images": images}

@router.post("/{album_id}/images")
def add_images_to_album(album_id: str, image_ids: List[str] = Body(...)):
    db_add_images_to_album(album_id, image_ids)
    return {"success": True}

@router.delete("/{album_id}/images/{image_id}")
def remove_image_from_album(album_id: str, image_id: str):
    db_remove_image_from_album(album_id, image_id)
    return {"success": True, "message": "Image deleted successfully"}

@router.delete("/{album_id}/images")
def remove_images_from_album(album_id: str, image_ids: List[str] = Body(...)):
    db_remove_images_from_album(album_id, image_ids)
    return {"success": True, "message": "Images deleted successfully"}
