import pandas as pd
import csv
from datetime import datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry added successfully!")

    @classmethod
    def get_transactions(cls, start_date, end_date):
        try:
            df = pd.read_csv(cls.CSV_FILE)
        except (FileNotFoundError, pd.errors.EmptyDataError):
            print("No data yet.")
            return pd.DataFrame(columns=cls.COLUMNS)
        if df.empty:
            print("No data yet.")
            return df

        df["date"] = pd.to_datetime(df["date"], format=cls.FORMAT, errors="coerce")
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

        start = datetime.strptime(start_date, cls.FORMAT)
        end = datetime.strptime(end_date, cls.FORMAT)

        mask = (df["date"] >= start) & (df["date"] <= end)
        filtered_df = df.loc[mask].copy()

        if filtered_df.empty:
            print("No transactions found in the given date range.")
            return filtered_df

        print(f"Transactions from {start.strftime(cls.FORMAT)} to {end.strftime(cls.FORMAT)}")
        out_df = filtered_df.copy()
        out_df["date"] = out_df["date"].dt.strftime(cls.FORMAT)
        print(out_df.to_string(index=False))

        inc_mask = filtered_df["category"].str.lower() == "income"
        exp_mask = filtered_df["category"].str.lower() == "expense"
        total_income = filtered_df.loc[inc_mask, "amount"].sum()
        total_expense = filtered_df.loc[exp_mask, "amount"].sum()

        print("\nSummary:")
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expense: ${total_expense:.2f}")
        print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df

def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or Enter for today's date: ")
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date, amount, category, description)

def plot_transactions(df):
    if df.empty: 
        print("No data to plot."); 
        return
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT, errors="coerce")
    df = df.set_index("date").sort_index()
    daily = df.groupby([pd.Grouper(freq="D"), "category"])["amount"].sum().unstack(fill_value=0)
    plt.figure(figsize=(10,5))
    plt.plot(daily.index, daily.get("Income", 0), label="Income")
    plt.plot(daily.index, daily.get("Expense", 0), label="Expense")
    plt.xlabel("Date"); plt.ylabel("Amount"); plt.title("Income and Expenses Over Time")
    plt.legend(); plt.grid(True); plt.show()


def main():
    while True:
        print("\n1. Add a new transaction")
        print("2. View transactions and a summary within a date range")
        print("3. Exit")
        choice =input("Enter your choice(1-3): ")

        if choice == "1":
            add()
        elif choice =="2":
            start_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date =get_date("Enter the end date (dd-mm-yyyy): ")
            df= CSV.get_transactions(start_date,end_date)
            if input("Do you want to se a plot? (Y/N)").lower() == "y":
                plot_transactions(df)
        elif choice == "3":
            print("Existing...")
            break
        else:
            print("Invalid choice, enter 1-3.")

if __name__ == "__main__":
    main()
