from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv
load_dotenv()
from graph import get_graph

app = FastAPI(title="Cross-Sell/Upsell Recommendation API")

graph_app = get_graph()  

@app.get("/recommendation")
def get_recommendation(customer_id: str = Query(..., description="Customer ID to generate recommendations for")):
    result = graph_app.invoke({"customer_id": customer_id})
    
    return JSONResponse(content={
        "report": result.get("research_report", "No report generated"),
        "recommendations": result.get("scored_opportunities", [])
    })

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
