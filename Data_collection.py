from datetime import datetime
CATEGORIES = {"I": "Income", "E": "Expense"}


def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime("%d-%m-%Y")

    try:
        valid = datetime.strptime(date_str, "%d-%m-%Y")
        return valid.strftime("%d-%m-%Y")
    except ValueError:
        print("Please enter the correct form of date")
        return get_date(prompt, allow_default)


def get_amount():
    try:
        amount = float(input("Enter Amount: "))
        if amount <= 0:
            raise ValueError("Enter proper amount")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


def get_category():
    category = input("Enter Income or Expense as I or E: ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]

    print("Invalid Category ")
    return  get_category()


def get_description():
    return input("Enter a description: ")
