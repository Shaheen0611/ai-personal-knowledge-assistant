import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteResponse, NoteUpdate

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)

@router.post(
    "",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED
)
def create_note(
    note_data: NoteCreate,
    database: Session = Depends(get_db)
) -> Note:
    note = Note(
        title=note_data.title,
        content=note_data.content,
    )

    database.add(note)
    database.commit()
    database.refresh(note)

    return note

@router.get(
    "",
    response_model=list[NoteResponse],
)
def list_notes(
    database: Session = Depends(get_db),
) -> list[Note]:
    statement = select(Note).order_by(Note.created_at.desc())

    notes = database.scalars(statement).all()

    return list(notes)

@router.get(
    "/{note_id}",
    response_model=NoteResponse,
)
def get_note(
    note_id: uuid.UUID,
    database: Session = Depends(get_db),
) -> Note:
    note = database.get(Note, note_id)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
    
    return note

@router.put(
    "/{note_id}",
    response_model=NoteResponse,
)
def update_note(
    note_id: uuid.UUID,
    note_data: NoteUpdate,
    database: Session = Depends(get_db),
) -> Note:
    note = database.get(Note, note_id)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    update_data = note_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(note, field, value)

    database.commit()
    database.refresh(note)

    return note


@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_note(
    note_id: uuid.UUID,
    database: Session = Depends(get_db),
) -> None:
    note = database.get(Note, note_id)

    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
    
    database.delete(note)
    database.commit()