import pandas as pd
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / "data" / "customer_data.csv"

def score_opportunities(customer_context, missing_opportunities, affinity_suggestions, top_n=3):
    df = pd.read_csv(CSV_PATH)
    
    customer_priority = customer_context.get("customer_priority", "Medium")
    usage_percentage = customer_context.get("product_usage_percent", 0)

    priority_score_map = {"High": 3, "Medium": 2, "Low": 1}

    # Prepare maps for fast lookup
    affinity_scores = {item["product"]: item["co_purchase_count"] for item in affinity_suggestions}
    missing_product_names = {item["product"] for item in missing_opportunities}

    scored_opportunities = []

    for product in missing_product_names.union(affinity_scores.keys()):
        score = 0
        rationale = []

        # Frequency among peers
        peer_frequency = df[df["Product"] == product].shape[0]
        if product in missing_product_names:
            score += min(peer_frequency, 5)
            rationale.append(f"Purchased {peer_frequency} times by industry peers.")

        # Product affinity (global)
        affinity_score = affinity_scores.get(product, 0)
        score += min(affinity_score, 5)
        if affinity_score > 0:
            rationale.append(f"Frequently co-purchased globally with customer's products ({affinity_score} times).")

        # If suggested by both → boost
        if product in missing_product_names and product in affinity_scores:
            score += 3
            rationale.append("Recommended by both peer and global product analysis (High confidence).")

        # Product Usage (%) → prioritize upsell
        if usage_percentage >= 80:
            score += 3
            rationale.append(f"Customer product usage is high ({usage_percentage}%). Upsell recommended.")

        # Customer Priority
        score += priority_score_map.get(customer_priority, 2)
        rationale.append(f"Customer priority: {customer_priority}.")

        scored_opportunities.append({
            "product": product,
            "score": score,
            "rationale": rationale
        })

    # Sort by descending score
    return sorted(scored_opportunities, key=lambda x: x["score"], reverse=True)[:top_n]

if __name__ == "__main__":
    from customer_context import get_customer_context
    from purchase_pattern_analysis import analyze_purchase_patterns
    from product_affinity import generate_product_affinity, suggest_affinity

    customer_id = "C003"  # Example customer ID
    context = get_customer_context(customer_id)

    # Get missing opportunities and frequent products
    analysis = analyze_purchase_patterns(context, top_n=3)
    missing_opportunities = analysis["missing_opportunities"]
    frequent_products = analysis["frequent_products"]

    # Generate product affinity suggestions
    affinity_suggestions = suggest_affinity(context, top_n=3)

    # Score the opportunities
    scored_opportunities = score_opportunities(context, missing_opportunities, affinity_suggestions, top_n=3)

    import pprint
    pprint.pprint(scored_opportunities)