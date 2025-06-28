from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import navigation, nlp_handler, product_lookup, recom

app = FastAPI(
    title="In-Store Assistant API",
    description="Backend for AI-powered in-store shopping assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(navigation.router, prefix="/navigate", tags=["Navigation"])
app.include_router(nlp_handler.router, prefix="/nlp", tags=["NLP"])
app.include_router(product_lookup.router, prefix="/product", tags=["Product Lookup"])
app.include_router(recom.router, prefix="/recommend", tags=["Recommendation"])

@app.get("/")
def root():
    return {"message": "Welcome to the In-Store Assistant API"}

# Optional: health check
@app.get("/health")
def health_check():
    return {"status": "OK"}
