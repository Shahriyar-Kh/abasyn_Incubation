def generate_receipt(order_id, customer_name, customer_phone, customer_address, total_price, table_number, delivery, items, tax=0.0, discount=0.0, restaurant_name="Restaurant", logo=""):
    """
    Generate a professional receipt with a clean and organized layout.
    """
    import datetime

    # Header with Restaurant Logo and Name
    receipt_data = f"{'=' * 50}\n"
    receipt_data += f"{restaurant_name.center(50)}\n"
    receipt_data += f"{'=' * 50}\n\n"

    # Order Information
    receipt_data += f"Order ID: {order_id:<10} Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    receipt_data += f"Customer: {customer_name}\n"
    receipt_data += f"Phone: {customer_phone}\n"
    receipt_data += f"Address: {customer_address}\n"
    receipt_data += f"Table: {table_number if table_number else 'N/A'}\n"
    receipt_data += f"Delivery: {'Yes' if delivery else 'No'}\n"
    receipt_data += f"{'-' * 50}\n"

    # Items List with Proper Alignment
    receipt_data += f"{'Item':<25}{'Price':>8}{'Qty':>8}{'Total':>10}\n"
    receipt_data += f"{'-' * 50}\n"

    item_total = 0
    for item in items:
        item_name = item['item_name']
        item_quantity = item['Quantity']
        item_price = item['Price']
        item_subtotal = item['Total_price']

        receipt_data += f"{item_name:<25}{float(item_price):>8.2f}{int(item_quantity):>8}{float(item_subtotal):>10.2f}\n"
        item_total += float(item_subtotal)

    # Summary Section
    receipt_data += f"{'-' * 50}\n"
    receipt_data += f"{'Subtotal:':<40}{item_total:>10.2f}\n"
    receipt_data += f"{'Tax:':<40}{tax:>10.2f}\n"
    receipt_data += f"{'Discount:':<40}{discount:>10.2f}\n"
    receipt_data += f"{'Total Price:':<40}{total_price:>10.2f}\n"
    receipt_data += f"{'=' * 50}\n"

    # Footer
    receipt_data += f"Thank you for dining with {restaurant_name}!\n"
    receipt_data += f"Visit us: www.{restaurant_name.lower().replace(' ', '')}.com\n"
    receipt_data += f"Follow us on Social Media: @{restaurant_name.lower().replace(' ', '')}\n"
    receipt_data += f"{'=' * 50}\n"

    # Save to a .txt file
    receipt_filename = f"Receipts/receipt_{order_id}.txt"
    with open(receipt_filename, "w") as file:
        file.write(receipt_data)

    print(f"Receipt generated and saved as {receipt_filename}")
