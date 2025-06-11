import pandas as pd
from pathlib import Path

# CSV file path
CSV_PATH = Path(__file__).parent.parent / "data" / "customer_data.csv"

def get_customer_context(customer_id: str) -> dict:
    df = pd.read_csv(CSV_PATH)

    # Filter rows for the given customer
    customer_rows = df[df["Customer ID"] == customer_id]
    if customer_rows.empty:
        raise ValueError(f"No data found for Customer ID: {customer_id}")

    # Extract static customer info from first row (same across rows for the customer)
    customer_info = customer_rows.iloc[0]

    # Extract purchase history (selecting product-specific info)
    purchase_history = customer_rows[[
        "Product", "Quantity", "Unit Price (USD)", "Total Price (USD)", "Purchase Date"
    ]].to_dict(orient="records")

    # Extract opportunities (these columns repeat for each row but that’s fine for now)
    opportunities = customer_rows[[
        "Opportunity Amount (USD)", "Opportunity Type", "Competitors",
        "Activity Status", "Activity Priority", "Activity Type", "Product SKU"
    ]].drop_duplicates().to_dict(orient="records")

    # Build context dictionary
    context = {
        "customer_id": customer_id,
        "customer_name": customer_info["Customer Name"],
        "industry": customer_info["Industry"],
        "annual_revenue": customer_info["Annual Revenue (USD)"],
        "number_of_employees": customer_info["Number of Employees"],
        "customer_priority": customer_info["Customer Priority"],
        "rating": customer_info["Rating"],
        "account_type": customer_info["Account Type"],
        "location": customer_info["Location"],
        "current_products": [x.strip() for x in str(customer_info["Current Products"]).split(",")],
        "product_usage_percent": customer_info["Product Usage (%)"],
        "cross_sell_synergy": customer_info["Cross-Sell Synergy"],
        "last_activity_date": customer_info["Last Activity Date"],
        "opportunity_stage": customer_info["Opportunity Stage"],

        "purchase_history": purchase_history,
        "opportunities": opportunities
    }

    return context

if __name__ == "__main__":
    context = get_customer_context("C002")
    import pprint
    pprint.pprint(context)