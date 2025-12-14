# GraphQL Filtering Documentation

## Overview
The CRM system now supports comprehensive filtering capabilities for customers, products, and orders.

## Filter Classes (`crm/filters.py`)

### CustomerFilter
- **name**: Case-insensitive partial match
- **email**: Case-insensitive partial match
- **created_at__gte**: Filter by creation date (greater than or equal)
- **created_at__lte**: Filter by creation date (less than or equal)
- **phone_pattern**: Custom filter for phone numbers starting with a pattern

### ProductFilter
- **name**: Case-insensitive partial match
- **price__gte**: Minimum price
- **price__lte**: Maximum price
- **stock__gte**: Minimum stock
- **stock__lte**: Maximum stock
- **stock**: Exact stock match
- **low_stock**: Boolean filter for products with stock < 10

### OrderFilter
- **total_amount__gte**: Minimum total amount
- **total_amount__lte**: Maximum total amount
- **order_date__gte**: Filter by order date (greater than or equal)
- **order_date__lte**: Filter by order date (less than or equal)
- **customer_name**: Filter by customer name (case-insensitive partial match)
- **product_name**: Filter by product name (case-insensitive partial match)
- **product_id**: Filter orders containing a specific product

## GraphQL Query Examples

### 1. Filter Customers by Name and Creation Date

```graphql
query {
  allCustomers(name: "Ali", createdAtGte: "2025-01-01T00:00:00") {
    id
    name
    email
    createdAt
  }
}
```

### 2. Filter Products by Price Range and Sort by Stock

```graphql
query {
  allProducts(priceGte: 100.0, priceLte: 1000.0, orderBy: "-stock") {
    id
    name
    price
    stock
  }
}
```

### 3. Filter Orders by Customer Name, Product Name, and Total Amount

```graphql
query {
  allOrders(
    customerName: "Alice"
    productName: "Laptop"
    totalAmountGte: 500.0
  ) {
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
```

### 4. Filter Customers by Phone Pattern

```graphql
query {
  allCustomers(phonePattern: "+1") {
    id
    name
    phone
  }
}
```

### 5. Filter Products with Low Stock

```graphql
query {
  allProducts(lowStock: true) {
    id
    name
    stock
  }
}
```

### 6. Filter Orders by Date Range

```graphql
query {
  allOrders(
    orderDateGte: "2025-12-01T00:00:00"
    orderDateLte: "2025-12-31T23:59:59"
  ) {
    id
    customer {
      name
    }
    totalAmount
    orderDate
  }
}
```

### 7. Sort Customers by Name (Ascending)

```graphql
query {
  allCustomers(orderBy: "name") {
    id
    name
    email
  }
}
```

### 8. Sort Customers by Name (Descending)

```graphql
query {
  allCustomers(orderBy: "-name") {
    id
    name
    email
  }
}
```

### 9. Filter Products by Stock Range

```graphql
query {
  allProducts(stockGte: 10, stockLte: 50) {
    id
    name
    stock
  }
}
```

### 10. Filter Orders by Product ID

```graphql
query {
  allOrders(productId: 1) {
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
```

## Sorting

All queries support the `orderBy` parameter:

- **Ascending**: `orderBy: "field_name"`
- **Descending**: `orderBy: "-field_name"`

Examples:
- `orderBy: "name"` - Sort by name ascending
- `orderBy: "-price"` - Sort by price descending
- `orderBy: "created_at"` - Sort by creation date ascending
- `orderBy: "-total_amount"` - Sort by total amount descending

## Combining Filters

You can combine multiple filters in a single query:

```graphql
query {
  allCustomers(
    name: "Alice"
    phonePattern: "+1"
    createdAtGte: "2025-01-01T00:00:00"
    orderBy: "name"
  ) {
    id
    name
    email
    phone
    createdAt
  }
}
```

## Error Handling

- Invalid filter values will be ignored
- Date filters expect ISO 8601 format: `"YYYY-MM-DDTHH:MM:SS"`
- Numeric filters expect valid numbers
- Boolean filters expect `true` or `false`
