from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
import fitz
from .schemas import DocumentCreate
from .database import Base, engine, SessionLocal, get_db
from .models import Document
from sqlalchemy.orm import Session
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

app = FastAPI(title= 'RAG knowledge engine')
embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")
semantic_chunker = SemanticChunker(embed_model, breakpoint_threshold_type='percentile')

@app.get('/')
def root():
    return {'endpoint' :'root'}

@app.get('/health')
def health():
    return {'status' : 'ok'}

@app.get('/test_db')
def test_connection(db: Session = Depends(get_db)):
    return {'message': 'Database session is active'}

@app.post('/ingest')
def ingest_document(doc: DocumentCreate, db: Session = Depends(get_db)):
    new_doc = Document(title=doc.title, content=doc.content)
    
    db.add(new_doc)    # Put it in the "To-Be-Saved" pile
    db.commit()        # Actually save it to Postgres
    db.refresh(new_doc) # Get the ID that Postgres assigned to it

    return {"message": "Document ingested!", "id": new_doc.id}


@app.post('/upload')
def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    total_chunks = 0
    file_content = file.file.read()
    document = fitz.open(stream=file_content, filetype='pdf')
    to_save = []

    for page in document:
        page_text = page.get_text()
        if not page_text.strip():
            continue
        chunks = semantic_chunker.create_documents([page_text])
    
        for chunk in chunks:
            db_chunk = Document(
                title = f'{file.filename}',
                content = chunk.page_content,
                page_number = f'Page {page.number + 1}'
            )
            total_chunks+=1
            to_save.append(db_chunk)
    db.add_all(to_save)        
    db.commit()

    return {
        'filename' : file.filename, 
        'chunks_created': total_chunks,
        'status': 'Success! Text extracted'
    }

Base.metadata.create_all(bind = engine)