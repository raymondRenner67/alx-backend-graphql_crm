#!/usr/bin/env python
"""
Test script for DjangoFilterConnectionField queries
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


def test_connection_queries():
    """Test DjangoFilterConnectionField queries"""
    
    # Test 1: Filter customers by name using connection field
    query1 = '''
    query {
        allCustomers(name: "Ali") {
            edges {
                node {
                    id
                    name
                    email
                    createdAt
                }
            }
        }
    }
    '''
    result1 = schema.execute(query1)
    print_result("TEST 1: Filter Customers by Name (Connection Field)", result1)
    
    # Test 2: Filter products by price range
    query2 = '''
    query {
        allProducts(price_Gte: "50.0", price_Lte: "1000.0") {
            edges {
                node {
                    id
                    name
                    price
                    stock
                }
            }
        }
    }
    '''
    result2 = schema.execute(query2)
    print_result("TEST 2: Filter Products by Price Range", result2)
    
    # Test 3: Filter orders by customer name
    query3 = '''
    query {
        allOrders(customerName: "Alice") {
            edges {
                node {
                    id
                    customer {
                        name
                    }
                    products {
                        edges {
                            node {
                                name
                                price
                            }
                        }
                    }
                    totalAmount
                    orderDate
                }
            }
        }
    }
    '''
    result3 = schema.execute(query3)
    print_result("TEST 3: Filter Orders by Customer Name", result3)
    
    # Test 4: Simple query without filters
    query4 = '''
    query {
        allCustomers {
            edges {
                node {
                    id
                    name
                    email
                }
            }
        }
    }
    '''
    result4 = schema.execute(query4)
    print_result("TEST 4: All Customers (No Filter)", result4)
    
    print("\n" + "="*70)
    print("ALL CONNECTION FIELD TESTS COMPLETED!")
    print("="*70)


if __name__ == "__main__":
    test_connection_queries()
