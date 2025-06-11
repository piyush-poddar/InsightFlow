from langgraph.graph import StateGraph
from typing import TypedDict, List

from agents.customer_context import get_customer_context
from agents.purchase_pattern_analysis import analyze_purchase_patterns
from agents.product_affinity import suggest_affinity
from agents.opportunity_scoring import score_opportunities
from agents.recommendation_report import generate_recommendation_report

# 1. Customer Context Agent
def customer_context_agent(state):
    customer_id = state["customer_id"]
    context = get_customer_context(customer_id)
    state["customer_context"] = context
    return state

# 2. Purchase Pattern Analysis Agent
def purchase_pattern_agent(state):
    context = state["customer_context"]
    pattern = analyze_purchase_patterns(context, top_n=3)
    state["purchase_pattern"] = pattern
    return state

# 3. Product Affinity Agent
def product_affinity_agent(state):
    context = state["customer_context"]
    suggestions = suggest_affinity(context, top_n=3)
    state["affinity_suggestions"] = suggestions
    return state

# 4. Opportunity Scoring Agent
def opportunity_scoring_agent(state):
    context = state["customer_context"]
    pattern = state["purchase_pattern"]
    affinity = state["affinity_suggestions"]

    scored = score_opportunities(context, pattern["missing_opportunities"], affinity, top_n=3)
    state["scored_opportunities"] = scored
    return state

# 5. Recommendation Report Agent
def recommendation_report_agent(state):
    context = state["customer_context"]
    scored = state["scored_opportunities"]
    report = generate_recommendation_report(context, scored)
    state["research_report"] = report
    return state

# Define state schema
class AgentState(TypedDict):
    customer_id: str
    customer_context: dict
    purchase_pattern: List[dict]
    affinity_suggestions: List[dict]
    scored_opportunities: List[dict]
    research_report: str

def get_graph():
    graph = StateGraph(AgentState)

    # Add agents/nodes
    graph.add_node("get_customer_context", customer_context_agent)
    graph.add_node("analyze_purchase_pattern", purchase_pattern_agent)
    graph.add_node("suggest_affinity", product_affinity_agent)
    graph.add_node("score_opportunities", opportunity_scoring_agent)
    graph.add_node("generate_report", recommendation_report_agent)

    # Add edges to define execution order
    graph.add_edge("get_customer_context", "analyze_purchase_pattern")
    graph.add_edge("analyze_purchase_pattern", "suggest_affinity")
    graph.add_edge("suggest_affinity", "score_opportunities")
    graph.add_edge("score_opportunities", "generate_report")

    graph.set_entry_point("get_customer_context")
    graph.set_finish_point("generate_report")

    app = graph.compile()
    
    return app

if __name__ == "__main__":
    # Example usage
    app = get_graph()
    result = app.invoke({"customer_id": "C002"})
    print(result["research_report"])
