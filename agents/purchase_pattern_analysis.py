import pandas as pd
from collections import Counter
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / "data" / "customer_data.csv"

def analyze_purchase_patterns(customer_context: dict, top_n=3) -> dict:
    df = pd.read_csv(CSV_PATH)

    # Customer's own purchased products
    purchase_history = customer_context["purchase_history"]
    customer_products = set(p["Product"] for p in purchase_history)

    # Find peer customer IDs (excluding this customer) who purchased these products
    peer_customer_ids = df[
        (df["Product"].isin(customer_products)) & (df["Customer ID"] != customer_context["customer_id"])
    ]["Customer ID"].unique()

    # Get *all* products bought by these peer customers
    peer_products_df = df[df["Customer ID"].isin(peer_customer_ids)]
    peer_products = peer_products_df["Product"].tolist()

    # Count products, exclude ones already purchased by this customer
    product_counts = Counter(peer_products)
    missing_opportunities = [
        {"product": prod, "co_purchase_count": count}
        for prod, count in product_counts.items()
        if prod not in customer_products
    ][:top_n]

    # Frequent products: Customer’s own history
    own_product_counts = Counter([p["Product"] for p in purchase_history])
    frequent_products = [
        {"product": prod, "frequency": qty}
        for prod, qty in own_product_counts.most_common(top_n)
    ]

    return {
        "frequent_products": frequent_products,
        "missing_opportunities": missing_opportunities
    }


if __name__ == "__main__":
    from customer_context import get_customer_context
    customer_id = "C005"
    context = get_customer_context(customer_id)
    analysis = analyze_purchase_patterns(context, top_n=3)
    import pprint
    pprint.pprint(analysis)