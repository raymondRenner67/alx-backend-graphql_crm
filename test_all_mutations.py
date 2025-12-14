#!/usr/bin/env python
"""
Comprehensive test script for all GraphQL mutations
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
        print(json.dumps(result.data, indent=2))


def test_all_mutations():
    """Test all CRM mutations"""
    
    # Test 1: Create a single customer
    mutation1 = '''
    mutation {
        createCustomer(input: {
            name: "Alice"
            email: "alice_new@example.com"
            phone: "+1234567890"
        }) {
            customer {
                id
                name
                email
                phone
            }
            message
            success
        }
    }
    '''
    result1 = schema.execute(mutation1)
    print_result("TEST 1: Create Single Customer", result1)
    
    # Test 2: Bulk create customers
    mutation2 = '''
    mutation {
        bulkCreateCustomers(input: [
            { name: "Bob", email: "bob_new@example.com", phone: "123-456-7890" }
            { name: "Carol", email: "carol_new@example.com" }
        ]) {
            customers {
                id
                name
                email
            }
            errors {
                email
                message
            }
            success
        }
    }
    '''
    result2 = schema.execute(mutation2)
    print_result("TEST 2: Bulk Create Customers", result2)
    
    # Test 3: Create a product
    mutation3 = '''
    mutation {
        createProduct(input: {
            name: "Laptop"
            price: "999.99"
            stock: 10
        }) {
            product {
                id
                name
                price
                stock
            }
            message
            success
        }
    }
    '''
    result3 = schema.execute(mutation3)
    print_result("TEST 3: Create Product", result3)
    
    # Test 4: Create an order with products
    mutation4 = '''
    mutation {
        createOrder(input: {
            customerId: "1"
            productIds: ["1", "2"]
        }) {
            order {
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
            message
            success
        }
    }
    '''
    result4 = schema.execute(mutation4)
    print_result("TEST 4: Create Order with Products", result4)
    
    # Test 5: Error handling - duplicate email
    mutation5 = '''
    mutation {
        createCustomer(input: {
            name: "Duplicate"
            email: "alice@example.com"
        }) {
            customer {
                id
            }
            message
            success
        }
    }
    '''
    result5 = schema.execute(mutation5)
    print_result("TEST 5: Error Handling - Duplicate Email", result5)
    
    # Test 6: Error handling - invalid phone
    mutation6 = '''
    mutation {
        createCustomer(input: {
            name: "Invalid Phone"
            email: "invalid_phone@example.com"
            phone: "invalid-format"
        }) {
            customer {
                id
            }
            message
            success
        }
    }
    '''
    result6 = schema.execute(mutation6)
    print_result("TEST 6: Error Handling - Invalid Phone", result6)
    
    # Test 7: Error handling - negative price
    mutation7 = '''
    mutation {
        createProduct(input: {
            name: "Invalid Product"
            price: "-10.00"
        }) {
            product {
                id
            }
            message
            success
        }
    }
    '''
    result7 = schema.execute(mutation7)
    print_result("TEST 7: Error Handling - Negative Price", result7)
    
    # Test 8: Query all data
    query8 = '''
    {
        allCustomers {
            id
            name
            email
        }
        allProducts {
            id
            name
            price
        }
        allOrders {
            id
            totalAmount
        }
    }
    '''
    result8 = schema.execute(query8)
    print_result("TEST 8: Query All Data", result8)
    
    print("\n" + "="*70)
    print("ALL TESTS COMPLETED!")
    print("="*70)


if __name__ == "__main__":
    test_all_mutations()
