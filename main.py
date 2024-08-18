import pandas as pd
import csv
from datetime import datetime
from Data_collection import get_category, get_amount, get_date, get_description
import matplotlib.pyplot as plt


class CSV:
    CSV_file = "data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_file)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_file, index=False)

    @classmethod
    def add(cls, date, amount, category, description):
        new_add = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        with open(cls.CSV_file, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.COLUMNS)
            writer.writerow(new_add)
        print("New Entry Added successfully")

    @classmethod
    def get_transaction(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_file)
        df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y")
        start_date = datetime.strptime(start_date, "%d-%m-%Y")
        end_date = datetime.strptime(end_date, "%d-%m-%Y")
        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered = df.loc[mask]

        if filtered.empty:
            print("No dates in range")
        else:
            print(
                f"Transactions are {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
            )
            print(
                filtered.to_string(
                    index=False, formatters={"date": lambda x: x.strftime(CSV.FORMAT)}
                )
            )
            total_income = filtered[filtered["category"] == "Income"]["amount"].sum()
            total_expense = filtered[filtered["category"] == "Expense"]["amount"].sum()
            print("\nSummary: ")
            print(f"Total Income: Rs{total_income:.2f}")
            print(f"Total Expense: Rs{total_expense:.2f}")
            print(f"Net Savings: Rs{(total_income - total_expense):.2f}")
        return filtered


def add_data():
    CSV.initialize_csv()
    date = get_date("Enter the date of transaction: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add(date, amount, category, description)


def plot(df):
    df.set_index('date', inplace=True)
    income = df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense = df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)
    plt.figure(figsize=(10,5))
    plt.plot(income.index, income["amount"], label="Income", color="g")
    plt.plot(expense.index, income["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expenses in Rs")
    plt.legend()
    plt.grid(True)
    plt.show()


def main():
    while True:
        print("\n1. Add Transaction")
        print("\n2. View transactions")
        print("\n3. Exit")

        choice = input("Enter Choice from above three: ")
        if choice == "1":
            add_data()
        elif choice == "2":
            start_date = get_date("Enter a Start date: ")
            end_date = get_date("Enter a End date: ")
            df = CSV.get_transaction(start_date, end_date)
            if input("Do you want a chart").lower() == "y":
                plot(df)
        elif choice == "3":
            print("Exiting Program...")
            break
        else:
            print("Enter a right choice between 1, 2, 3")


if __name__ == "__main__":
    main()
