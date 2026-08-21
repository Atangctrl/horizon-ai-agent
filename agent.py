"""
Horizon AI Africa - Full-Stack Financial Management & Agentic Hub
Architectural Reference: JavaScript Mastery Full-Stack Banking Platform
"""

import json
from strands import Agent, tool

# Mock In-Memory Database representing Appwrite / Plaid aggregation tables
USER_ACCOUNTS = {
    "acc_101": {"bank_name": "First National Bank", "type": "Checking", "balance": 4500.00, "currency": "BWP"},
    "acc_102": {"bank_name": "Absa Botswana", "type": "Savings", "balance": 12800.50, "currency": "BWP"},
    "acc_103": {"bank_name": "Orange Money Wallet", "type": "Mobile Money", "balance": 920.00, "currency": "BWP"}
}

TRANSACTIONS = [
    {"id": "tx_01", "account_id": "acc_101", "merchant": "Choppies Supermarket", "amount": 340.50, "category": "Groceries", "status": "Completed"},
    {"id": "tx_02", "account_id": "acc_101", "merchant": "BPC Electricity", "amount": 200.00, "category": "Utilities", "status": "Completed"},
    {"id": "tx_03", "account_id": "acc_103", "merchant": "Sefalana Cash & Carry", "amount": 1150.00, "category": "Inventory", "status": "Completed"}
]

# ----------------------------------------------------
# 1. Multi-Account Aggregation Tool
# ----------------------------------------------------
@tool
def get_account_balances() -> str:
    """Fetches real-time multi-account balances across connected traditional bank and mobile wallet endpoints."""
    total_bwp = sum(acc["balance"] for acc in USER_ACCOUNTS.values())
    summary = {
        "connected_accounts": USER_ACCOUNTS,
        "total_aggregated_balance_bwp": round(total_bwp, 2)
    }
    return json.dumps(summary, indent=2)

# ----------------------------------------------------
# 2. Real-Time Transaction Tracking & Categorization Tool
# ----------------------------------------------------
@tool
def get_transaction_history(account_id: str = None) -> str:
    """Retrieves transaction history with optional account filtering and category breakdowns."""
    if account_id:
        filtered = [tx for tx in TRANSACTIONS if tx["account_id"] == account_id]
        return json.dumps({"account_id": account_id, "transactions": filtered}, indent=2)
    return json.dumps({"all_transactions": TRANSACTIONS}, indent=2)

# ----------------------------------------------------
# 3. Secure Peer-to-Peer Transfer & Invoicing Engine
# ----------------------------------------------------
@tool
def execute_funds_transfer(sender_acc_id: str, recipient_acc_id: str, amount: float, reference: str) -> str:
    """Facilitates secure funds transfer between linked multi-bank or mobile wallets with validation."""
    if sender_acc_id not in USER_ACCOUNTS:
        return f"Error: Sender account '{sender_acc_id}' not found."
    if USER_ACCOUNTS[sender_acc_id]["balance"] < amount:
        return f"Error: Insufficient funds in {sender_acc_id}. Available: {USER_ACCOUNTS[sender_acc_id]['balance']} BWP."

    # Perform balance transfer execution
    USER_ACCOUNTS[sender_acc_id]["balance"] -= amount
    if recipient_acc_id in USER_ACCOUNTS:
        USER_ACCOUNTS[recipient_acc_id]["balance"] += amount

    new_tx = {
        "id": f"tx_0{len(TRANSACTIONS)+1}",
        "account_id": sender_acc_id,
        "merchant": f"Transfer to {recipient_acc_id} ({reference})",
        "amount": amount,
        "category": "Transfer",
        "status": "Completed"
    }
    TRANSACTIONS.append(new_tx)

    return f"Success: Transferred {amount:.2f} BWP from {sender_acc_id} to {recipient_acc_id}. Transaction Reference: {reference}."

# ----------------------------------------------------
# 4. Initialize Strands Financial Agent
# ----------------------------------------------------
horizon_agent = Agent(
    system_prompt=(
        "You are Horizon AI Africa, an agentic personal finance and business hub. "
        "You manage multi-account bank aggregations, transaction tracking, and peer-to-peer transfers "
        "for unbanked spenders and micro-merchants."
    ),
    tools=[get_account_balances, get_transaction_history, execute_funds_transfer]
)

if __name__ == "__main__":
    print("=== Testing Horizon AI Multi-Account Aggregation ===")
    print(get_account_balances())
    
    print("\n=== Testing Real-Time Transaction Tracking ===")
    print(get_transaction_history(account_id="acc_101"))

    print("\n=== Testing Secure Funds Transfer Engine ===")
    print(execute_funds_transfer("acc_101", "acc_103", 250.00, "Ref: Invoice #1042"))

    print("\n=== Updated Aggregated Balances ===")
    print(get_account_balances())