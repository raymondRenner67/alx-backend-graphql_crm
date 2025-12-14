#!/usr/bin/env python
"""
Test script for GraphQL mutations
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_backend_graphql.settings')
django.setup()

from alx_backend_graphql.schema import schema


def test_create_customer():
    """Test creating a single customer"""
    print("\n" + "="*60)
    print("Testing CreateCustomer Mutation")
    print("="*60)
    
    mutation = '''
    mutation {
        createCustomer(input: {
            name: "Test User",
            email: "testuser@example.com",
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
    
    result = schema.execute(mutation)
    print(f"Success: {result.data}")
    if result.errors:
        print(f"Errors: {result.errors}")


def test_create_product():
    """Test creating a product"""
    print("\n" + "="*60)
    print("Testing CreateProduct Mutation")
    print("="*60)
    
    mutation = '''
    mutation {
        createProduct(input: {
            name: "Test Product",
            price: "199.99",
            stock: 5
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
    
    result = schema.execute(mutation)
    print(f"Success: {result.data}")
    if result.errors:
        print(f"Errors: {result.errors}")


def test_query_all():
    """Test querying all data"""
    print("\n" + "="*60)
    print("Testing Query All Customers")
    print("="*60)
    
    query = '''
    {
        allCustomers {
            id
            name
            email
        }
    }
    '''
    
    result = schema.execute(query)
    print(f"Customers: {result.data}")


if __name__ == "__main__":
    test_query_all()
    test_create_customer()
    test_create_product()
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)
