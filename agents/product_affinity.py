import pandas as pd
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / "data" / "customer_data.csv"

def generate_product_affinity():
    df = pd.read_csv(CSV_PATH)

    # Map customer_id -> set of products they purchased
    customer_products = df.groupby("Customer ID")["Product"].apply(set)
    # Count co-occurrence of product pairs
    co_occurrence = defaultdict(int)
    for products in customer_products:
        for prod1, prod2 in combinations(products, 2):
            co_occurrence[frozenset([prod1, prod2])] += 1

    return co_occurrence

def suggest_affinity(customer_context, top_n=3):
    co_occurrence = generate_product_affinity()
    customer_products = set(p["Product"] for p in customer_context["purchase_history"])

    # Count of products co-occurring with customer's products
    affinity_counter = Counter()
    for pair, count in co_occurrence.items():
        prods = list(pair)
        if prods[0] in customer_products and prods[1] not in customer_products:
            affinity_counter[prods[1]] += count
        elif prods[1] in customer_products and prods[0] not in customer_products:
            affinity_counter[prods[0]] += count

    return [{"product": prod, "co_purchase_count": count} for prod, count in affinity_counter.most_common(top_n)]

if __name__ == "__main__":
    from customer_context import get_customer_context
    customer_id = "C005"
    context = get_customer_context(customer_id)
    
    suggestions = suggest_affinity(context, top_n=3)
    
    import pprint
    pprint.pprint(suggestions)
