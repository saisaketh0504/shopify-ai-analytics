## Agent Workflow

The system follows an agentic workflow to answer user questions:

1. User submits a natural-language question via the Rails API.
2. The Python AI service parses the question.
3. Intent is detected (sales, inventory, or customers).
4. Required Shopify data source is selected.
5. A ShopifyQL query is generated.
6. The query is executed against Shopify data (mocked).
7. Raw results are post-processed.
8. A business-friendly explanation is returned to the user.

## Intent Classification

The agent classifies questions into the following intents:

- Inventory: stock levels, reorder quantities, stock-out risks
- Sales: revenue trends, top-selling products
- Customers: repeat buyers, purchase frequency

Intent detection is currently rule-based but can be replaced with an LLM classifier.


## ShopifyQL Generation

Based on detected intent, the agent generates ShopifyQL queries.

Examples:

Inventory:
FROM inventory_levels SHOW available GROUP BY product_id

Sales:
FROM orders SHOW sum(net_sales) GROUP BY product_id

These queries are template-based for the assignment but follow ShopifyQL syntax.


## Sample Questions & Responses

### 1. Inventory Reorder
Question:
How much inventory should I reorder for next week?

Answer:
You sell around 8 units per day. To avoid stockouts next week, you should reorder at least 56 units.

---

### 2. Stockout Risk
Question:
Which products are likely to go out of stock soon?

Answer:
The following products are at risk of stockout soon: Vintage T-Shirt, Notebook, Canvas Bag.

---

### 3. Top Selling Products
Question:
What were my top 5 selling products last week?

Answer:
Your top selling products last week were: Coffee Mug, Vintage T-Shirt, Notebook, Sticker Pack, Canvas Bag.

---

### 4. Repeat Customers
Question:
Which customers placed repeat orders in the last 90 days?

Answer:
32 customers placed repeat orders in the last 90 days.


## Assumptions & Mocking

- Shopify OAuth is mocked for simplicity.
- Shopify API responses are simulated using static JSON data.
- ShopifyQL queries are template-based.
- LLM reasoning is simplified to focus on agent workflow.
- The assignment prioritizes design clarity over production integration.


## Error Handling

- Invalid or empty user input returns a 400 error.
- Unknown or ambiguous questions return a low-confidence response.
- Missing data is handled gracefully with user-friendly messages.


## Future Improvements

- Real Shopify OAuth integration
- LLM-based intent classification
- ShopifyQL validation layer
- Caching frequent queries
- Conversation memory for follow-up questions
- Retry and fallback logic for API failures


## Architecture Overview

Client / Postman
      ↓
Rails API (Validation & Gateway)
      ↓
Python AI Service (Agent)
      ↓
Shopify API (Mocked via JSON)
