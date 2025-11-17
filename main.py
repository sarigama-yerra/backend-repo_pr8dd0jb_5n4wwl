import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Congregationstats, Galleryimage, Contactmessage

app = FastAPI(title="Congregation Site API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Congregation API running"}

# Public endpoints to fetch content for the landing page

@app.get("/api/stats", response_model=List[Congregationstats])
async def get_stats():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    docs = get_documents("congregationstats", limit=5)
    # Convert ObjectId to str-safe by mapping without _id or converting
    result = []
    for d in docs:
        d.pop("_id", None)
        result.append(Congregationstats(**d))
    return result

@app.get("/api/gallery", response_model=List[Galleryimage])
async def get_gallery():
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    docs = get_documents("galleryimage", limit=8)
    result = []
    for d in docs:
        d.pop("_id", None)
        result.append(Galleryimage(**d))
    # sort by order
    result.sort(key=lambda x: x.order)
    return result

class ContactIn(Contactmessage):
    pass

@app.post("/api/contact")
async def submit_contact(payload: ContactIn):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    try:
        doc_id = create_document("contactmessage", payload)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
