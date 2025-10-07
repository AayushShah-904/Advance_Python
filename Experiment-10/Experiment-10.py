import csv
import os
from datetime import datetime
from fpdf import FPDF
from PyPDF2 import PdfMerger
 
filename = "orders.csv"

# Sample order data
orders = [
    ["ORD001", "Amit Sharma", "Wireless Mouse", 2, 450.00],
    ["ORD002", "Priya Patel", "USB Keyboard", 1, 700.00],
    ["ORD003", "Rohit Verma", "Bluetooth Speaker", 3, 1200.00],
    ["ORD004", "Sneha Iyer", "Laptop Stand", 1, 1500.00],
    ["ORD005", "Karan Mehta", "External Hard Drive", 2, 3500.00]
]

# Write CSV file
with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(["Order ID", "Customer Name", "Product Name", "Quantity", "Unit Price"])
    # Write rows
    writer.writerows(orders)

print(f"{filename} has been created with 5 sample orders.")

# Step 1: Load Order Data
csv_file = "orders.csv"

# Create a folder for invoices
if not os.path.exists("invoices"):
    os.makedirs("invoices")

invoices = []

with open(csv_file, newline='') as file:
    reader = csv.DictReader(file)

    for row in reader:
        order_id = row['Order ID']
        customer_name = row['Customer Name']
        product_name = row['Product Name']
        quantity = int(row['Quantity'])
        unit_price = float(row['Unit Price'])

        # Step 2: Calculate total amount
        total_amount = quantity * unit_price

        # Step 3: Generate individual PDF invoice using fpdf
        invoice_filename = f"invoices/{order_id}.pdf"
        invoices.append(invoice_filename)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Invoice Header
        pdf.cell(200, 10, txt=f"Invoice Number: {order_id}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Date of Purchase: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Customer Name: {customer_name}", ln=True, align="L")

        pdf.ln(5)  # line break

        # Order Details
        pdf.cell(200, 10, txt=f"Product Name: {product_name}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Quantity: {quantity}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Unit Price: ${unit_price:.2f}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Total Amount: ${total_amount:.2f}", ln=True, align="L")

        pdf.ln(10)
        pdf.cell(200, 10, txt="Thank you for shopping with us!", ln=True, align="L")

        pdf.output(invoice_filename)

# Step 4: Merge all invoices into one PDF using PyPDF2
merger = PdfMerger()

for pdf_file in invoices:
    merger.append(pdf_file)

merged_file = "All_Invoices.pdf"
merger.write(merged_file)
merger.close()

print(f"All invoices generated and merged into '{merged_file}'")