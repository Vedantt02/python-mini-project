import streamlit as st
from main import Bank

bank = Bank()

st.set_page_config(page_title="Bank Management System", layout="centered")
st.title("🏦 Bank Management System")

menu = st.sidebar.selectbox(
    "Select an option",
    ["Create Account", "Deposit", "Withdraw", "View Details", "Delete Account"]
)

# ---------- Create Account ----------
if menu == "Create Account":
    st.subheader("Create New Account")

    name = st.text_input("Name")
    email = st.text_input("Email")
    age = st.number_input("Age", min_value=0, step=1)
    phone = st.text_input("Phone Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Create"):
        result = bank.create_account(name, email, age, phone, int(pin))
        if result["success"]:
            st.success(f"Account created successfully 🎉")
            st.info(f"Account Number: {result['account_no']}")
        else:
            st.error(result["message"])

# ---------- Deposit ----------
elif menu == "Deposit":
    st.subheader("Deposit Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=0, step=1)

    if st.button("Deposit"):
        result = bank.deposit(acc, int(pin), amount)
        if result["success"]:
            st.success(f"New Balance: ₹{result['balance']}")
        else:
            st.error(result["message"])

# ---------- Withdraw ----------
elif menu == "Withdraw":
    st.subheader("Withdraw Money")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=0, step=1)

    if st.button("Withdraw"):
        result = bank.withdraw(acc, int(pin), amount)
        if result["success"]:
            st.success(f"New Balance: ₹{result['balance']}")
        else:
            st.error(result["message"])

# ---------- View Details ----------
elif menu == "View Details":
    st.subheader("Account Details")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("View"):
        result = bank.get_account_details(acc, int(pin))
        if result["success"]:
            st.json(result["data"])
        else:
            st.error(result["message"])

# ---------- Delete Account ----------
elif menu == "Delete Account":
    st.subheader("Delete Account")

    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")

    if st.button("Delete"):
        result = bank.delete_account(acc, int(pin))
        if result["success"]:
            st.success(result["message"])
        else:
            st.error(result["message"])