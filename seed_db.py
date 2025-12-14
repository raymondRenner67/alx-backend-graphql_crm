#!/usr/bin/env python
"""
Seed script for populating the CRM database with sample data
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

from crm.models import Customer, Product, Order
from decimal import Decimal
from django.db import transaction


def clear_database():
    """Clear all existing data"""
    print("Clearing existing data...")
    Order.objects.all().delete()
    Customer.objects.all().delete()
    Product.objects.all().delete()
    print("Database cleared!")


def seed_customers():
    """Create sample customers"""
    print("\nCreating customers...")
    customers = [
        {"name": "Alice Johnson", "email": "alice@example.com", "phone": "+1234567890"},
        {"name": "Bob Smith", "email": "bob@example.com", "phone": "123-456-7890"},
        {"name": "Carol Williams", "email": "carol@example.com", "phone": "+9876543210"},
        {"name": "David Brown", "email": "david@example.com", "phone": ""},
        {"name": "Eve Davis", "email": "eve@example.com", "phone": "+1122334455"},
    ]
    
    created_customers = []
    for customer_data in customers:
        customer = Customer.objects.create(**customer_data)
        created_customers.append(customer)
        print(f"  ✓ Created customer: {customer.name} ({customer.email})")
    
    return created_customers


def seed_products():
    """Create sample products"""
    print("\nCreating products...")
    products = [
        {"name": "Laptop", "price": Decimal("999.99"), "stock": 10},
        {"name": "Mouse", "price": Decimal("25.50"), "stock": 50},
        {"name": "Keyboard", "price": Decimal("75.00"), "stock": 30},
        {"name": "Monitor", "price": Decimal("299.99"), "stock": 15},
        {"name": "Headphones", "price": Decimal("49.99"), "stock": 40},
        {"name": "Webcam", "price": Decimal("89.99"), "stock": 20},
        {"name": "USB Cable", "price": Decimal("12.99"), "stock": 100},
        {"name": "External SSD", "price": Decimal("149.99"), "stock": 25},
    ]
    
    created_products = []
    for product_data in products:
        product = Product.objects.create(**product_data)
        created_products.append(product)
        print(f"  ✓ Created product: {product.name} (${product.price}, Stock: {product.stock})")
    
    return created_products


def seed_orders(customers, products):
    """Create sample orders"""
    print("\nCreating orders...")
    orders_data = [
        {"customer": customers[0], "products": [products[0], products[1]]},
        {"customer": customers[1], "products": [products[2], products[3], products[4]]},
        {"customer": customers[2], "products": [products[5]]},
        {"customer": customers[0], "products": [products[6], products[7]]},
        {"customer": customers[3], "products": [products[1], products[4], products[6]]},
    ]
    
    created_orders = []
    for order_data in orders_data:
        customer = order_data["customer"]
        products_list = order_data["products"]
        
        # Calculate total amount
        total_amount = sum(product.price for product in products_list)
        
        # Create order
        order = Order.objects.create(
            customer=customer,
            total_amount=total_amount
        )
        order.products.set(products_list)
        
        created_orders.append(order)
        product_names = ", ".join([p.name for p in products_list])
        print(f"  ✓ Created order #{order.id} for {customer.name}: {product_names} (Total: ${total_amount})")
    
    return created_orders


def main():
    """Main seeding function"""
    print("=" * 60)
    print("CRM Database Seeding Script")
    print("=" * 60)
    
    try:
        with transaction.atomic():
            # Clear existing data
            clear_database()
            
            # Seed data
            customers = seed_customers()
            products = seed_products()
            orders = seed_orders(customers, products)
            
            print("\n" + "=" * 60)
            print("Database seeded successfully!")
            print(f"  Customers: {len(customers)}")
            print(f"  Products: {len(products)}")
            print(f"  Orders: {len(orders)}")
            print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
