from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI()

class QuestionRequest(BaseModel):
    store_id: str
    question: str


def detect_intent(question):
    q = question.lower()
    if "inventory" in q or "stock" in q:
        return "inventory"
    if "sell" in q or "sales" in q:
        return "sales"
    if "customer" in q:
        return "customers"
    return "unknown"


def generate_shopifyql(intent):
    if intent == "inventory":
        return "FROM inventory_levels SHOW available GROUP BY product_id"
    if intent == "sales":
        return "FROM orders SHOW sum(net_sales) GROUP BY product_id"
    return ""


def execute_query():
    with open("../sample-data/shopify_mock.json") as f:
        return json.load(f)



def explain(intent, data, question):
    q = question.lower()

    if intent == "inventory":
        if "reorder" in q or "next week" in q:
            daily = data["sales"]["daily_average"]
            reorder = daily * 7
            return {
                "answer": f"You sell around {daily} units per day. "
                          f"To avoid stockouts next week, you should reorder at least {reorder} units.",
                "confidence": "medium"
            }

        if "out of stock" in q:
            low_stock = [
                product for product, qty in data["inventory"].items() if qty < 20
            ]
            return {
                "answer": f"The following products are at risk of stockout soon: {', '.join(low_stock)}.",
                "confidence": "high"
            }

    if intent == "sales":
        top_products = data["sales"]["top_products"][:5]
        products = ", ".join([p["product"] for p in top_products])
        return {
            "answer": f"Your top selling products last week were: {products}.",
            "confidence": "high"
        }

    if intent == "customers":
        repeat = data["customers"]["repeat_customers_last_90_days"]
        return {
            "answer": f"{repeat} customers placed repeat orders in the last 90 days.",
            "confidence": "medium"
        }

    return {
        "answer": "I could not clearly understand the question. Please provide more details.",
        "confidence": "low"
    }



@app.post("/ask")
def ask_question(req: QuestionRequest):
    intent = detect_intent(req.question)
    shopifyql = generate_shopifyql(intent)
    data = execute_query()
    result = explain(intent, data, req.question)
    return result
