from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.schemas.document import DocumentCreate, DocumentResponse
from app.models import DocumentModel
from uuid import UUID
from sqlalchemy import select


app = FastAPI()


@app.get("/")
async def root(db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {
            "status": "success",
            "message": "Hello World",
            "database": "Connected successfully!",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database connection failed: {str(e)}"
        )


@app.post(
    "/documents/", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED
)
async def create_document(document: DocumentCreate, db: AsyncSession = Depends(get_db)):
    item = DocumentModel(**document.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@app.get("/documents/{document_id}", response_model=DocumentResponse)
async def read_document(document_id: UUID, db: AsyncSession = Depends(get_db)):
    document = await db.get(DocumentModel, document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@app.get("/documents/", response_model=list[DocumentResponse])
async def list_documents(db: AsyncSession = Depends(get_db)):
    query = select(DocumentModel)
    result = await db.execute(query)
    documents = result.scalars().all()

    return documents
