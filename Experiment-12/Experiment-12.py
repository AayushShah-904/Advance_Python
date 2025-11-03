import pandas as pd
import matplotlib.pyplot as plt
import os
import shutil
from datetime import datetime

EXPENSES_FILE = os.path.join('Experiment-12', 'expenses.csv')
BUDGET_FILE = os.path.join('Experiment-12', 'budget.csv')
BACKUP_DIR = os.path.join('Experiment-12', 'backup')

def log_expense():
    name = input("Enter your name: ")
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    description = input("Enter description: ")
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return
    category = input("Enter category (e.g., groceries, utilities): ")

    new_expense = pd.DataFrame([[name, date, description, amount, category]],
                               columns=['Name', 'Date', 'Description', 'Amount', 'Category'])
    
    new_expense.to_csv(EXPENSES_FILE, mode='a', header=False, index=False)
    print("Expense logged successfully.")

def analyze_expenses():
    try:
        expenses_df = pd.read_csv(EXPENSES_FILE)
    except FileNotFoundError:
        print(f"{EXPENSES_FILE} not found.")
        return

    if expenses_df.empty:
        print("No expenses logged yet.")
        return

    # Total expenses per family member
    expenses_by_member = expenses_df.groupby('Name')['Amount'].sum()
    print("\nTotal Expenses per Family Member:")
    print(expenses_by_member)

    # Average daily expense for the household
    expenses_df['Date'] = pd.to_datetime(expenses_df['Date'])
    total_days = (expenses_df['Date'].max() - expenses_df['Date'].min()).days + 1
    total_household_expense = expenses_df['Amount'].sum()
    average_daily_expense = total_household_expense / total_days
    print(f"\nAverage Daily Household Expense: {average_daily_expense:.2f}")

def plot_expense_trends():
    try:
        expenses_df = pd.read_csv(EXPENSES_FILE)
    except FileNotFoundError:
        print(f"{EXPENSES_FILE} not found.")
        return

    if expenses_df.empty:
        print("No expenses to plot.")
        return

    expenses_df['Date'] = pd.to_datetime(expenses_df['Date'])
    
    daily_expenses = expenses_df.groupby('Date')['Amount'].sum().reset_index()
    daily_expenses = daily_expenses.sort_values('Date')
    daily_expenses['Cumulative Amount'] = daily_expenses['Amount'].cumsum()

    plt.figure(figsize=(10, 5))
    plt.plot(daily_expenses['Date'], daily_expenses['Cumulative Amount'], marker='o')
    plt.title('Cumulative Expense Trends')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Amount')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def generate_monthly_report():
    try:
        expenses_df = pd.read_csv(EXPENSES_FILE)
    except FileNotFoundError:
        print(f"{EXPENSES_FILE} not found.")
        return

    if expenses_df.empty:
        print("No expenses to report.")
        return

    expenses_df['Date'] = pd.to_datetime(expenses_df['Date'])
    expenses_df['Month'] = expenses_df['Date'].dt.to_period('M')

    latest_month = expenses_df['Month'].max()
    monthly_df = expenses_df[expenses_df['Month'] == latest_month]

    if monthly_df.empty:
        print("No expenses for the latest month.")
        return

    print(f"\n--- Monthly Report for {latest_month} ---")

    # Total expenses per family member for the month
    expenses_by_member = monthly_df.groupby('Name')['Amount'].sum()
    print("\nTotal Expenses per Family Member:")
    print(expenses_by_member)

    # Breakdown of expenses by category
    expenses_by_category = monthly_df.groupby('Category')['Amount'].sum()
    print("\nExpenses by Category:")
    print(expenses_by_category)

    # Comparison of monthly expenses over different months using bar charts
    monthly_totals = expenses_df.groupby('Month')['Amount'].sum()
    #monthly_totals.index = monthly_totals.index.astype(str)
    
    plt.figure(figsize=(10, 5))
    monthly_totals.plot(kind='bar')
    plt.title('Monthly Expense Comparison')
    plt.xlabel('Month')
    plt.ylabel('Total Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def manage_budget():
    try:
        budget_df = pd.read_csv(BUDGET_FILE)
        expenses_df = pd.read_csv(EXPENSES_FILE)
    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found.")
        return

    if budget_df.empty:
        print("No budget set. Please add categories and budgets to budget.csv.")
        return
    if expenses_df.empty:
        print("No expenses logged yet.")
        return

    expenses_df['Date'] = pd.to_datetime(expenses_df['Date'])
    expenses_df['Month'] = expenses_df['Date'].dt.to_period('M')
    latest_month = expenses_df['Month'].max()
    monthly_expenses = expenses_df[expenses_df['Month'] == latest_month]

    monthly_expenses_by_category = monthly_expenses.groupby('Category')['Amount'].sum().reset_index()

    budget_analysis = pd.merge(budget_df, monthly_expenses_by_category, on='Category', how='left')
    budget_analysis['Amount'] = budget_analysis['Amount'].fillna(0)
    budget_analysis['Remaining'] = budget_analysis['Budget'] - budget_analysis['Amount']

    print(f"\n--- Budget Report for {latest_month} ---")
    print(budget_analysis)

    exceeded_budget = budget_analysis[budget_analysis['Remaining'] < 0]
    if not exceeded_budget.empty:
        print("\n--- WARNING: Budget Exceeded ---")
        print(exceeded_budget)

def backup_data():

    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    if os.path.exists(EXPENSES_FILE):
        backup_file_path = os.path.join(BACKUP_DIR, f"expenses_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
        shutil.copy(EXPENSES_FILE, backup_file_path)
        print(f"Backup successful: {backup_file_path}")
    else:
        print(f"{EXPENSES_FILE} not found. Nothing to backup.")

def main_menu():
    """Displays the main menu and handles user choices."""
    while True:
        print("\nHousehold Expense Tracker")
        print("1. Log an Expense")
        print("2. Analyze Expenses")
        print("3. View Expense Trends")
        print("4. Generate Monthly Report")
        print("5. Manage Budget")
        print("6. Backup Data")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            log_expense()
        elif choice == '2':
            analyze_expenses()
        elif choice == '3':
            plot_expense_trends()
        elif choice == '4':
            generate_monthly_report()
        elif choice == '5':
            manage_budget()
        elif choice == '6':
            backup_data()
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    
    if not os.path.exists(EXPENSES_FILE):
        pd.DataFrame(columns=['Name', 'Date', 'Description', 'Amount', 'Category']).to_csv(EXPENSES_FILE, index=False)
    if not os.path.exists(BUDGET_FILE):
        pd.DataFrame(columns=['Category', 'Budget']).to_csv(BUDGET_FILE, index=False)

    main_menu()
