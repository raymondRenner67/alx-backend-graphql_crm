import django_filters
from django.db.models import Q
from .models import Customer, Product, Order


class CustomerFilter(django_filters.FilterSet):
    """Filter class for Customer model"""
    
    # Case-insensitive partial match for name
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    # Case-insensitive partial match for email
    email = django_filters.CharFilter(lookup_expr='icontains')
    
    # Date range filters for created_at
    created_at__gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    
    # Custom filter for phone number pattern (starts with +1)
    phone_pattern = django_filters.CharFilter(method='filter_phone_pattern')
    
    class Meta:
        model = Customer
        fields = ['name', 'email', 'created_at']
    
    def filter_phone_pattern(self, queryset, name, value):
        """Custom filter to match phone numbers starting with a specific pattern"""
        return queryset.filter(phone__istartswith=value)


class ProductFilter(django_filters.FilterSet):
    """Filter class for Product model"""
    
    # Case-insensitive partial match for name
    name = django_filters.CharFilter(lookup_expr='icontains')
    
    # Range filters for price
    price__gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    
    # Range filters for stock
    stock__gte = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    stock__lte = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')
    
    # Exact match for stock
    stock = django_filters.NumberFilter(field_name='stock', lookup_expr='exact')
    
    # Custom filter for low stock (stock < 10)
    low_stock = django_filters.BooleanFilter(method='filter_low_stock')
    
    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']
    
    def filter_low_stock(self, queryset, name, value):
        """Filter products with stock less than 10"""
        if value:
            return queryset.filter(stock__lt=10)
        return queryset


class OrderFilter(django_filters.FilterSet):
    """Filter class for Order model"""
    
    # Range filters for total_amount
    total_amount__gte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    total_amount__lte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    
    # Date range filters for order_date
    order_date__gte = django_filters.DateTimeFilter(field_name='order_date', lookup_expr='gte')
    order_date__lte = django_filters.DateTimeFilter(field_name='order_date', lookup_expr='lte')
    
    # Filter by customer name (related field lookup)
    customer_name = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    
    # Filter by product name (related field lookup through many-to-many)
    product_name = django_filters.CharFilter(field_name='products__name', lookup_expr='icontains')
    
    # Filter orders that include a specific product ID
    product_id = django_filters.NumberFilter(field_name='products__id', lookup_expr='exact')
    
    class Meta:
        model = Order
        fields = ['total_amount', 'order_date', 'customer_name', 'product_name']
