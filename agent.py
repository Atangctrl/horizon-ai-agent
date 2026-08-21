import json
from strands import Agent, tool

# ----------------------------------------------------
# Regional Database (Botswana & Kenya Endpoints)
# ----------------------------------------------------
USER_ACCOUNTS = {
    # Motswana User Accounts
    "acc_bw_101": {"owner": "Thabo (Botswana)", "bank_name": "First National Bank BW", "type": "Checking", "balance": 4500.00, "currency": "BWP"},
    "acc_bw_102": {"owner": "Thabo (Botswana)", "bank_name": "Orange Money BW", "type": "Mobile Money", "balance": 1170.00, "currency": "BWP"},
    
    # Kenyan User Accounts
    "acc_ke_201": {"owner": "Wanjiku (Kenya)", "bank_name": "M-Pesa Kenya", "type": "Mobile Money", "balance": 25000.00, "currency": "KES"},
    "acc_ke_202": {"owner": "Wanjiku (Kenya)", "bank_name": "KCB Bank Kenya", "type": "Savings", "balance": 85000.00, "currency": "KES"}
}

# Bill Utility Providers
UTILITY_BILLS = {
    "BILL-001": {"biller": "BPC Electricity (Botswana)", "account_no": "9920148", "amount_due": 350.00, "currency": "BWP", "status": "UNPAID"},
    "BILL-002": {"biller": "Kenya Power (KPLC)", "account_no": "4481029", "amount_due": 2400.00, "currency": "KES", "status": "UNPAID"}
}

# FX Conversion Matrix (1 BWP = 10.20 KES)
EXCHANGE_RATES = {
    ("BWP", "KES"): 10.20,
    ("KES", "BWP"): 0.098
}

INVOICES = []
INVENTORY = {
    "ITEM-001": {"name": "Maize Meal 10kg", "stock": 45, "unit_price": 85.00, "currency": "BWP"},
    "ITEM-002": {"name": "Handmade Craft Pack", "stock": 15, "unit_price": 1200.00, "currency": "KES"}
}

# ----------------------------------------------------
# 1. Multi-Account Aggregation (JSM Architecture)
# ----------------------------------------------------
@tool
def get_account_balances() -> str:
    """Aggregates multi-account bank and mobile wallet balances across Botswana and Kenya."""
    return json.dumps({
        "aggregated_accounts": USER_ACCOUNTS
    }, indent=2)

# ----------------------------------------------------
# 2. Automated Bill Payment Engine
# ----------------------------------------------------
@tool
def pay_utility_bill(account_id: str, bill_id: str) -> str:
    """Automates utility and merchant bill payments from linked bank/wallet accounts."""
    if account_id not in USER_ACCOUNTS:
        return f"Payment Failed: Account '{account_id}' not found."
    if bill_id not in UTILITY_BILLS:
        return f"Payment Failed: Bill ID '{bill_id}' invalid."

    acc = USER_ACCOUNTS[account_id]
    bill = UTILITY_BILLS[bill_id]

    if acc["currency"] != bill["currency"]:
        return f"Payment Failed: Currency mismatch ({acc['currency']} vs {bill['currency']}). Use cross-border transfer."

    if acc["balance"] < bill["amount_due"]:
        return f"Payment Failed: Insufficient funds in {account_id}."

    # Process Payment
    acc["balance"] -= bill["amount_due"]
    bill["status"] = "PAID"

    return json.dumps({
        "status": "Bill Payment Successful",
        "biller": bill["biller"],
        "account_debited": account_id,
        "amount_paid": f"{bill['amount_due']:.2f} {bill['currency']}",
        "remaining_account_balance": f"{acc['balance']:.2f} {acc['currency']}"
    }, indent=2)

# ----------------------------------------------------
# 3. Cross-Border P2P & MSME Invoicing
# ----------------------------------------------------
@tool
def execute_cross_border_transfer(sender_acc_id: str, recipient_acc_id: str, amount: float) -> str:
    """Executes cross-border payments (BWP <-> KES) with real-time FX conversion."""
    if sender_acc_id not in USER_ACCOUNTS or recipient_acc_id not in USER_ACCOUNTS:
        return "Transfer Failed: Invalid account selection."

    sender = USER_ACCOUNTS[sender_acc_id]
    recipient = USER_ACCOUNTS[recipient_acc_id]

    if sender["balance"] < amount:
        return f"Transfer Failed: Insufficient balance."

    rate = EXCHANGE_RATES.get((sender["currency"], recipient["currency"]), 1.0) if sender["currency"] != recipient["currency"] else 1.0
    converted_amount = amount * rate

    sender["balance"] -= amount
    recipient["balance"] += converted_amount

    return json.dumps({
        "status": "Cross-Border Transfer Settled",
        "sender": f"{sender['owner']} ({sender_acc_id})",
        "recipient": f"{recipient['owner']} ({recipient_acc_id})",
        "sent_amount": f"{amount:.2f} {sender['currency']}",
        "received_amount": f"{converted_amount:.2f} {recipient['currency']}"
    }, indent=2)

@tool
def generate_msme_invoice(client_name: str, item_sku: str, quantity: int) -> str:
    """Generates automated MSME invoices and updates merchant stock levels in real time."""
    if item_sku not in INVENTORY or INVENTORY[item_sku]["stock"] < quantity:
        return "Invoice Creation Failed: Insufficient inventory."

    item = INVENTORY[item_sku]
    total_price = item["unit_price"] * quantity
    INVENTORY[item_sku]["stock"] -= quantity

    invoice = {
        "invoice_id": f"INV-{len(INVOICES) + 1001}",
        "client": client_name,
        "item": item["name"],
        "quantity": quantity,
        "total": f"{total_price:.2f} {item['currency']}",
        "status": "PAID"
    }
    INVOICES.append(invoice)
    return json.dumps({"status": "Invoice Generated", "invoice_details": invoice}, indent=2)

# ----------------------------------------------------
# Agent Setup
# ----------------------------------------------------
horizon_agent = Agent(
    system_prompt=(
        "You are Horizon AI Africa, a full-stack regional financial hub. "
        "You manage multi-account aggregation, bill payments, cross-border transfers (BWP/KES), "
        "and MSME inventory reconciliation."
    ),
    tools=[get_account_balances, pay_utility_bill, execute_cross_border_transfer, generate_msme_invoice]
)

if __name__ == "__main__":
    print("=== 1. Multi-Account Aggregation ===")
    print(get_account_balances())

    print("\n=== 2. Utility Bill Payment (BPC Electricity) ===")
    print(pay_utility_bill("acc_bw_101", "BILL-001"))

    print("\n=== 3. Cross-Border P2P (Motswana -> Kenyan M-Pesa) ===")
    print(execute_cross_border_transfer("acc_bw_101", "acc_ke_201", 200.00))

    print("\n=== 4. Regional MSME Invoicing & Inventory Reconcile ===")
    print(generate_msme_invoice("Regional Trade Partner", "ITEM-001", 2))