# CRM GraphQL API - Test Queries

## Setup

1. Run migrations: `python manage.py migrate`
2. Seed database: `python seed_db.py`
3. Start server: `python manage.py runserver`
4. Visit: http://localhost:8000/graphql

## Test Mutations

### 1. Create a Single Customer

```graphql
mutation {
  createCustomer(input: {
    name: "Alice"
    email: "alice@example.com"
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
```

### 2. Bulk Create Customers

```graphql
mutation {
  bulkCreateCustomers(input: [
    { name: "Bob", email: "bob@example.com", phone: "123-456-7890" }
    { name: "Carol", email: "carol@example.com" }
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
```

### 3. Create a Product

```graphql
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
```

### 4. Create an Order with Products

```graphql
mutation {
  createOrder(input: {
    customerId: "1"
    productIds: ["1", "2"]
  }) {
    order {
      id
      customer {
        name
        email
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
```

## Test Queries

### Query All Customers

```graphql
{
  allCustomers {
    id
    name
    email
    phone
    orders {
      id
      totalAmount
      orderDate
    }
  }
}
```

### Query All Products

```graphql
{
  allProducts {
    id
    name
    price
    stock
  }
}
```

### Query All Orders

```graphql
{
  allOrders {
    id
    customer {
      name
      email
    }
    products {
      name
      price
    }
    totalAmount
    orderDate
  }
}
```

### Query Single Customer by ID

```graphql
{
  customer(id: "1") {
    id
    name
    email
    phone
    orders {
      id
      totalAmount
      products {
        name
        price
      }
    }
  }
}
```

### Query Single Product by ID

```graphql
{
  product(id: "1") {
    id
    name
    price
    stock
  }
}
```

### Query Single Order by ID

```graphql
{
  order(id: "1") {
    id
    customer {
      name
      email
    }
    products {
      name
      price
    }
    totalAmount
    orderDate
  }
}
```

## Error Handling Tests

### Test Duplicate Email

```graphql
mutation {
  createCustomer(input: {
    name: "Test"
    email: "alice@example.com"  # Already exists
  }) {
    customer {
      id
    }
    message
    success
  }
}
```

### Test Invalid Phone Format

```graphql
mutation {
  createCustomer(input: {
    name: "Test"
    email: "newuser@example.com"
    phone: "invalid-phone"
  }) {
    customer {
      id
    }
    message
    success
  }
}
```

### Test Invalid Price

```graphql
mutation {
  createProduct(input: {
    name: "Test Product"
    price: "-10.00"  # Negative price
  }) {
    product {
      id
    }
    message
    success
  }
}
```

### Test Invalid Customer ID

```graphql
mutation {
  createOrder(input: {
    customerId: "999"  # Non-existent
    productIds: ["1"]
  }) {
    order {
      id
    }
    message
    success
  }
}
```

### Test Empty Products List

```graphql
mutation {
  createOrder(input: {
    customerId: "1"
    productIds: []  # Empty list
  }) {
    order {
      id
    }
    message
    success
  }
}
```

## Combined Query Example

```graphql
{
  hello
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
```
