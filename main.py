#Importing Modules and Initializing Expenses Dictionary
import pandas as pd
import os
from datetime import datetime

#Initialize a dictionary to store expenses and budgets for each category
expenses = {
    "Rent": {"budget": 1000, "transactions": []},
    "Electricity": {"budget": 150, "transactions": []},
    "Water": {"budget": 50, "transactions": []},
    "Breakfast": {"budget": 20, "transactions": []},
    "Lunch": {"budget": 30, "transactions": []},
    "Dinner": {"budget": 40, "transactions": []},
    "Enjoyment": {"budget": 100, "transactions": []},
    "Misc": {"budget": 50, "transactions": []},
    "Other": {"budget": 0, "transactions": []}
}

#Function to Add an Expense
def add_expense():
    print("Expense Categories:")
    for category in expenses:
        print(category)

    category = input("Enter expense category: ")

    if category in expenses:
        description = input("Enter expense description: ")
        amount = float(input("Enter expense amount: "))
        date = input("Enter expense date (YYYY-MM-DD): ")

        expenses[category]["transactions"].append((description, amount, date))
        expenses[category]["budget"] -= amount
        print("Expense added successfully!")

        if expenses[category]["budget"] < 0:
            print("Warning: Budget exceeded!")

    else:
        print("Invalid category. Please choose a valid category.")

#Function to View Expenses and Remaining Budget
def view_expenses():
    category = input("Enter a category to view expenses: ")

    if category in expenses:
        print("Expenses in", category, "category:")
        for description, amount, date in expenses[category]["transactions"]:
            print("Description:", description, "Amount:", amount, "Date:", date)

        print("Remaining budget:", expenses[category]["budget"])
        if expenses[category]["budget"] < 0:
            print("Budget exceeded by:", -expenses[category]["budget"])
    else:
        print("No expenses found in the", category, "category.")

# Function to calculate total expenses for all categories in a specific week, month, or year
def calculate_total_expenses(expense_data, period_choice):
    total_expenses = []
    for category in expense_data:
        for transaction in expense_data[category]["transactions"]:
            if len(transaction) == 3:
                description, amount, date = transaction
                date = datetime.strptime(date, "%Y-%m-%d")
                if period_choice == "W":
                    start_of_week = date - pd.DateOffset(days=date.weekday())
                    if start_of_week.week == datetime.now().isocalendar()[1]:
                        total_expenses.append((category, description, amount, f"Week {start_of_week.week}"))
                elif period_choice == "M":
                    if date.month == datetime.now().month:
                        total_expenses.append((category, description, amount, date.strftime("%B")))
                elif period_choice == "Y":
                    if date.year == datetime.now().year:
                        total_expenses.append((category, description, amount, date.strftime("%Y")))
            else:
                print("Invalid transaction format:", transaction)

    return total_expenses

# Function to export expenses for all categories to Excel
def export_to_excel_all(expense_data, export_choice):
    total_expenses = calculate_total_expenses(expense_data, export_choice)

    filename = f"expenses_{export_choice}.xlsx"
    full_path = os.path.join(os.path.expanduser('~'), 'Documents', filename)

    # Check if the directory exists, if not, create it
    if not os.path.exists(os.path.join(os.path.expanduser('~'), 'Documents')):
        os.makedirs(os.path.join(os.path.expanduser('~'), 'Documents'))

    df = pd.DataFrame(total_expenses, columns=["Category", "Description", "Amount", "Date"])
    df.to_excel(full_path, index=False)
    print("Expenses exported to", full_path)


#Main Program Loop
while True:
    print("\nExpense Tracker")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Export Expenses to Excel")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_expense()
    elif choice == '2':
        view_expenses()
    elif choice == '3':
        export_choice = input("Export for (W)eek, (M)onth, or (Y)ear: ").upper()
        if export_choice in ["W", "M", "Y"]:
            export_to_excel_all(expenses, export_choice)
        else:
            print("Invalid choice. Please choose W, M, or Y.")
    elif choice == '4':
        print("Exiting the Expense Tracker. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a valid option.")

#End of the program