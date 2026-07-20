from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes_chargement import router as chargement_router
from api.routes_visualisation import router as visualisation_router
from api.routes_analyse import router as analyse_router

app = FastAPI(
    title="CelluleAnalyse API",
    description="Pipeline d'analyse de microscopie à fluorescence",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:5173"],
    allow_origins=[
    "http://localhost:5173",  # dev
    "http://localhost",       # docker production
    "http://localhost:80",    # docker production alt
    ],
    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chargement_router)
app.include_router(visualisation_router)
app.include_router(analyse_router)

@app.get("/")
def root():
    return {"message": "CelluleAnalyse API en ligne"}
