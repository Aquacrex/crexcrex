from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, random

app = FastAPI()
INAT_API = "https://api.inaturalist.org/v1"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/quiz")
async def get_quiz_question(taxon: str = "Fungi"):
    """Fetch a random observation from iNaturalist for the quiz."""
    params = {
        "taxon_name": taxon,
        "quality_grade": "research",
        "page": 1,
        "per_page": 200,
        "has": "photos",
    }
    response = requests.get(f"{INAT_API}/observations", params=params)
    observations = response.json().get("results", [])
    
    if not observations:
        return {"error": "No observations found"}
    
    # Pick a random observation with photos
    obs = random.choice([obs for obs in observations if obs.get("photos")])
    
    # Extract species and image
    species = obs.get("species_guess", "Unknown")
    image_url = obs["photos"][0]["url"]  # Larger image
    
    return {
        "image": image_url,
        "hints": {
            "date": obs.get("observed_on_string"),
            "location": obs.get("place_guess")
        },
        "answer": {
            "species": species,
            "taxon_id": obs.get("taxon", {}).get("id")
        }
    }