from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Renovation Price Finder API", version="1.1")

# Allow Bubble/browser calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    item: str
    store: str
    price: float
    link: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/search", response_model=dict)
def search(query: str = Query(..., description="Comma-separated list of renovation items")):
    keywords = [w.strip() for w in query.split(",") if w.strip()]
    results: List[Product] = []

    for kw in keywords:
        low = kw.lower()
        if "oven" in low:
            results.append(Product(item="Bosch Oven", store="Amazon", price=620,
                                   link="https://amazon.com/bosch-oven"))
        elif "countertop" in low or "worktop" in low:
            results.append(Product(item="Marble Countertop", store="IKEA", price=499,
                                   link="https://www.ikea.com/countertop"))
        elif "cabinet" in low:
            results.append(Product(item="White Shaker Cabinet Set", store="Home Depot", price=1200,
                                   link="https://www.homedepot.com/cabinets"))
        elif "dishwasher" in low:
            results.append(Product(item="Bosch 300 Series Dishwasher", store="Best Buy", price=420,
                                   link="https://www.bestbuy.com/site/searchpage.jsp?st=bosch+300+dishwasher"))
        else:
            results.append(Product(item=kw, store="Generic Store", price=100.0,
                                   link="https://example.com"))

    return {"query": query, "products": [r.dict() for r in results]}
