#!/usr/bin/env python
"""
Test script for GraphQL filtering functionality
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

from alx_backend_graphql.schema import schema
import json


def print_result(title, result):
    """Helper to print results nicely"""
    print("\n" + "="*70)
    print(title)
    print("="*70)
    if result.errors:
        print("❌ ERRORS:", result.errors)
    else:
        print("✅ SUCCESS:")
        print(json.dumps(result.data, indent=2, default=str))


def test_filters():
    """Test all filtering capabilities"""
    
    # Test 1: Filter customers by name
    query1 = '''
    query {
        allCustomers(name: "Ali") {
            id
            name
            email
            createdAt
        }
    }
    '''
    result1 = schema.execute(query1)
    print_result("TEST 1: Filter Customers by Name (Ali)", result1)
    
    # Test 2: Filter products by price range and sort by stock
    query2 = '''
    query {
        allProducts(priceGte: 50.0, priceLte: 1000.0, orderBy: "-stock") {
            id
            name
            price
            stock
        }
    }
    '''
    result2 = schema.execute(query2)
    print_result("TEST 2: Filter Products by Price Range and Sort by Stock", result2)
    
    # Test 3: Filter orders by customer name
    query3 = '''
    query {
        allOrders(customerName: "Alice") {
            id
            customer {
                name
            }
            products {
                name
                price
            }
            totalAmount
            orderDate
        }
    }
    '''
    result3 = schema.execute(query3)
    print_result("TEST 3: Filter Orders by Customer Name", result3)
    
    # Test 4: Filter products with low stock
    query4 = '''
    query {
        allProducts(lowStock: true) {
            id
            name
            stock
        }
    }
    '''
    result4 = schema.execute(query4)
    print_result("TEST 4: Filter Products with Low Stock", result4)
    
    # Test 5: Filter customers by phone pattern
    query5 = '''
    query {
        allCustomers(phonePattern: "+1") {
            id
            name
            phone
        }
    }
    '''
    result5 = schema.execute(query5)
    print_result("TEST 5: Filter Customers by Phone Pattern (+1)", result5)
    
    # Test 6: Filter orders by total amount range
    query6 = '''
    query {
        allOrders(totalAmountGte: 100.0, totalAmountLte: 500.0) {
            id
            customer {
                name
            }
            totalAmount
        }
    }
    '''
    result6 = schema.execute(query6)
    print_result("TEST 6: Filter Orders by Total Amount Range", result6)
    
    # Test 7: Sort customers by name
    query7 = '''
    query {
        allCustomers(orderBy: "name") {
            id
            name
            email
        }
    }
    '''
    result7 = schema.execute(query7)
    print_result("TEST 7: Sort Customers by Name (Ascending)", result7)
    
    # Test 8: Filter orders by product name
    query8 = '''
    query {
        allOrders(productName: "Laptop") {
            id
            customer {
                name
            }
            products {
                name
            }
            totalAmount
        }
    }
    '''
    result8 = schema.execute(query8)
    print_result("TEST 8: Filter Orders by Product Name", result8)
    
    print("\n" + "="*70)
    print("ALL FILTER TESTS COMPLETED!")
    print("="*70)


if __name__ == "__main__":
    test_filters()
