import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def generate_recommendation_report(customer_context, scored_opportunities):
    recommendations_list = "\n".join([
        f"- {opp['product']}: {'; '.join(opp['rationale'])}" for opp in scored_opportunities
    ])

    prompt = f"""
    You are an expert business analyst. Generate a professional research report suggesting cross-sell and upsell opportunities for the following customer. The tone should be concise, persuasive, and suitable for business executives.
    
    Customer Name: {customer_context['customer_name']}
    Industry: {customer_context['industry']}
    Annual Revenue: {customer_context['annual_revenue']} USD
    Recent Purchases: {customer_context['purchase_history']}

    Recommendations:
    {recommendations_list}

    For each recommendation, briefly explain *why* it is a good fit, using the rationale provided. Structure the report with these sections:

    1. Introduction
    2. Customer Overview
    3. Data Analysis (in bullet points)
    4. Recommendations (as a numbered list with Rationale and Benefits)
    5. Conclusion

    Make sure the language is polished and executive-level.
    Make sure the report is crisp and concise, focusing on actionable insights and clear recommendations.
    Use bullet points for clarity.
    Use explicit product names and avoid jargon.
    Ensure the report is formatted for easy reading, with clear headings and sections.
    """

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    from customer_context import get_customer_context
    from purchase_pattern_analysis import analyze_purchase_patterns
    from product_affinity import suggest_affinity
    from opportunity_scoring import score_opportunities

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

    # Generate the recommendation report
    recommendation_report = generate_recommendation_report(context, scored_opportunities)
    print("Generated Recommendation Report:")
    print(recommendation_report)
