try:
    import pandas as pd
    import matplotlib.pyplot as plt
except ImportError:
    print("Please install pandas and matplotlib using: pip install pandas matplotlib")
    exit()

import os
import shutil
from datetime import datetime

EXPENSES_FILE = 'expenses.csv'
BUDGET_FILE = 'budget.csv'
BACKUP_DIR = 'backup'

def log_expense():
    """Logs a new expense to the expenses.csv file."""
    name = input("Enter your name: ")
    date_str = input("Enter date (YYYY-MM-DD): ")
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return
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
    """Analyzes expenses from expenses.csv."""
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
    """Plots expense trends over the last month."""
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
    """Generates a monthly expense report."""
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

    # For simplicity, report on the latest month
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
    monthly_totals.index = monthly_totals.index.astype(str)
    
    plt.figure(figsize=(10, 5))
    monthly_totals.plot(kind='bar')
    plt.title('Monthly Expense Comparison')
    plt.xlabel('Month')
    plt.ylabel('Total Amount')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def manage_budget():
    """Manages and checks budget against expenses."""
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
    """Backs up the expenses.csv file."""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    if os.path.exists(EXPENSES_FILE):
        backup_file_path = os.path.join(BACKUP_DIR, f"expenses_backup_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv")
        shutil.copy(EXPENSES_FILE, backup_file_path)
        print(f"Backup successful: {backup_file_path}")
    else:
        print(f"{EXPENSES_FILE} not found. Nothing to backup.")

def restore_data():
    """Restores the expenses.csv file from a backup."""
    if not os.path.exists(BACKUP_DIR):
        print("Backup directory not found.")
        return

    backups = [f for f in os.listdir(BACKUP_DIR) if f.startswith('expenses_backup_') and f.endswith('.csv')]
    if not backups:
        print("No backups found.")
        return

    print("Available backups:")
    for i, backup in enumerate(backups):
        print(f"{i + 1}. {backup}")

    try:
        choice = int(input("Select a backup to restore: ")) - 1
        if 0 <= choice < len(backups):
            backup_to_restore = os.path.join(BACKUP_DIR, backups[choice])
            shutil.copy(backup_to_restore, EXPENSES_FILE)
            print(f"Restored from {backups[choice]}")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Invalid input.")

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
        print("7. Restore Data")
        print("8. Exit")
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
            restore_data()
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Check if data files exist, if not create them with headers
    if not os.path.exists(EXPENSES_FILE):
        pd.DataFrame(columns=['Name', 'Date', 'Description', 'Amount', 'Category']).to_csv(EXPENSES_FILE, index=False)
    if not os.path.exists(BUDGET_FILE):
        pd.DataFrame(columns=['Category', 'Budget']).to_csv(BUDGET_FILE, index=False)

    main_menu()
