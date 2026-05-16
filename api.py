import json
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# ================= REQUEST MODEL ================= #
class ChatRequest(BaseModel):
    message: str
    user_id: str


# ================= LOAD USERS ================= #
def load_users():
    with open("users.json", "r") as f:
        return json.load(f)


# ================= ACCOUNT DETAILS ================= #
def account_details(user_id):
    users = load_users()

    if user_id not in users:
        return {
            "reply": "❌ User not found",
            "status": "failed"
        }

    user = users[user_id]

    return {
        "reply": (
            f"Name: {user['name']}, "
            f"Account: {user['account_type']}, "
            f"Balance: ₹{user['balance']}, "
            f"Status: {user['status']}, "
            f"KYC: {user['kyc']}"
        ),
        "status": "success"
    }


# ================= BALANCE ================= #
def check_balance(user_id):
    users = load_users()

    if user_id not in users:
        return {
            "reply": "❌ User not found",
            "status": "failed"
        }

    return {
        "reply": f"💰 Your balance is ₹{users[user_id]['balance']}",
        "status": "success"
    }


# ================= TRANSFER ================= #
def transfer_money(message, user_id):
    users = load_users()
    msg = message.lower().split()

    if user_id not in users:
        return {"reply": "❌ User not found", "status": "failed"}

    try:
        amount = None
        to_user = msg[-1]

        for w in msg:
            if w.isdigit():
                amount = int(w)
                break

        if not amount:
            return {"reply": "❌ Amount missing", "status": "failed"}

        if to_user not in users:
            return {"reply": "❌ Receiver not found", "status": "failed"}

        # update balances (temporary in-memory)
        users[user_id]["balance"] -= amount
        users[to_user]["balance"] += amount

        return {
            "reply": f"✅ ₹{amount} transferred from {user_id} to {to_user}",
            "status": "success"
        }

    except Exception as e:
        return {
            "reply": f"❌ Transfer error: {str(e)}",
            "status": "failed"
        }


# ================= INTENT ROUTER ================= #
def route_intent(message, user_id):

    msg = message.lower()

    # ---- BALANCE ---- #
    if "balance" in msg:
        return check_balance(user_id)

    # ---- ACCOUNT DETAILS ---- #
    elif "account" in msg:
        return account_details(user_id)

    # ---- TRANSFER ---- #
    elif "transfer" in msg:
        return transfer_money(message, user_id)

    # ---- DEFAULT ---- #
    else:
        return {
            "reply": "❌ Unknown request",
            "status": "unknown_intent"
        }


# ================= API ENDPOINT ================= #
@app.post("/chat")
def chat(req: ChatRequest):
    return route_intent(req.message, req.user_id)


# ================= ROOT ================= #
@app.get("/")
def root():
    return {"message": "FastAPI Backend Running"}