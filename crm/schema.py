import graphene
from graphene_django import DjangoObjectType
from django.core.exceptions import ValidationError
from django.db import transaction
from decimal import Decimal
from datetime import datetime
import re

from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter


# GraphQL Types
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        fields = '__all__'


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = '__all__'


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = '__all__'


# Input Types
class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String(required=False)


class ProductInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    price = graphene.Decimal(required=True)
    stock = graphene.Int(required=False, default_value=0)


class OrderInput(graphene.InputObjectType):
    customer_id = graphene.ID(required=True)
    product_ids = graphene.List(graphene.ID, required=True)
    order_date = graphene.DateTime(required=False)


# Validation Helper Functions
def validate_phone(phone):
    """Validate phone number format"""
    if not phone:
        return True
    pattern = r'^\+?1?\d{9,15}$|^\d{3}-\d{3}-\d{4}$'
    return re.match(pattern, phone) is not None


def validate_email_unique(email, exclude_id=None):
    """Check if email is unique"""
    query = Customer.objects.filter(email=email)
    if exclude_id:
        query = query.exclude(id=exclude_id)
    return not query.exists()


# Mutations
class CreateCustomer(graphene.Mutation):
    class Arguments:
        input = CustomerInput(required=True)

    customer = graphene.Field(CustomerType)
    message = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, input):
        # Validate email uniqueness
        if not validate_email_unique(input.email):
            return CreateCustomer(
                customer=None,
                message="Email already exists",
                success=False
            )

        # Validate phone format
        if input.get('phone') and not validate_phone(input.phone):
            return CreateCustomer(
                customer=None,
                message="Invalid phone format. Use +1234567890 or 123-456-7890",
                success=False
            )

        try:
            customer = Customer.objects.create(
                name=input.name,
                email=input.email,
                phone=input.get('phone', '')
            )
            return CreateCustomer(
                customer=customer,
                message="Customer created successfully",
                success=True
            )
        except ValidationError as e:
            return CreateCustomer(
                customer=None,
                message=str(e),
                success=False
            )


class CustomerError(graphene.ObjectType):
    email = graphene.String()
    message = graphene.String()


class BulkCreateCustomers(graphene.Mutation):
    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    customers = graphene.List(CustomerType)
    errors = graphene.List(CustomerError)
    success = graphene.Boolean()

    def mutate(self, info, input):
        created_customers = []
        errors = []

        with transaction.atomic():
            for customer_data in input:
                # Validate email uniqueness
                if not validate_email_unique(customer_data.email):
                    errors.append(CustomerError(
                        email=customer_data.email,
                        message="Email already exists"
                    ))
                    continue

                # Validate phone format
                if customer_data.get('phone') and not validate_phone(customer_data.phone):
                    errors.append(CustomerError(
                        email=customer_data.email,
                        message="Invalid phone format"
                    ))
                    continue

                try:
                    customer = Customer.objects.create(
                        name=customer_data.name,
                        email=customer_data.email,
                        phone=customer_data.get('phone', '')
                    )
                    created_customers.append(customer)
                except ValidationError as e:
                    errors.append(CustomerError(
                        email=customer_data.email,
                        message=str(e)
                    ))
                except Exception as e:
                    errors.append(CustomerError(
                        email=customer_data.email,
                        message=str(e)
                    ))

        return BulkCreateCustomers(
            customers=created_customers,
            errors=errors,
            success=len(created_customers) > 0
        )


class CreateProduct(graphene.Mutation):
    class Arguments:
        input = ProductInput(required=True)

    product = graphene.Field(ProductType)
    message = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, input):
        # Validate price is positive
        if input.price <= 0:
            return CreateProduct(
                product=None,
                message="Price must be positive",
                success=False
            )

        # Validate stock is not negative
        stock = input.get('stock', 0)
        if stock < 0:
            return CreateProduct(
                product=None,
                message="Stock cannot be negative",
                success=False
            )

        try:
            product = Product.objects.create(
                name=input.name,
                price=input.price,
                stock=stock
            )
            return CreateProduct(
                product=product,
                message="Product created successfully",
                success=True
            )
        except ValidationError as e:
            return CreateProduct(
                product=None,
                message=str(e),
                success=False
            )


class CreateOrder(graphene.Mutation):
    class Arguments:
        input = OrderInput(required=True)

    order = graphene.Field(OrderType)
    message = graphene.String()
    success = graphene.Boolean()

    def mutate(self, info, input):
        # Validate customer exists
        try:
            customer = Customer.objects.get(id=input.customer_id)
        except Customer.DoesNotExist:
            return CreateOrder(
                order=None,
                message=f"Customer with ID {input.customer_id} does not exist",
                success=False
            )

        # Validate at least one product is selected
        if not input.product_ids or len(input.product_ids) == 0:
            return CreateOrder(
                order=None,
                message="At least one product must be selected",
                success=False
            )

        # Validate all product IDs exist and collect products
        products = []
        total_amount = Decimal('0.00')
        
        for product_id in input.product_ids:
            try:
                product = Product.objects.get(id=product_id)
                products.append(product)
                total_amount += product.price
            except Product.DoesNotExist:
                return CreateOrder(
                    order=None,
                    message=f"Product with ID {product_id} does not exist",
                    success=False
                )

        try:
            # Create order
            order = Order.objects.create(
                customer=customer,
                total_amount=total_amount,
            )
            
            # Associate products
            order.products.set(products)
            
            # Update order_date if provided
            if input.get('order_date'):
                order.order_date = input.order_date
                order.save()

            return CreateOrder(
                order=order,
                message="Order created successfully",
                success=True
            )
        except Exception as e:
            return CreateOrder(
                order=None,
                message=str(e),
                success=False
            )


# Query
class Query(graphene.ObjectType):
    # Filtered queries with arguments
    all_customers = graphene.List(
        CustomerType,
        name=graphene.String(),
        email=graphene.String(),
        created_at_gte=graphene.DateTime(),
        created_at_lte=graphene.DateTime(),
        phone_pattern=graphene.String(),
        order_by=graphene.String()
    )
    
    all_products = graphene.List(
        ProductType,
        name=graphene.String(),
        price_gte=graphene.Float(),
        price_lte=graphene.Float(),
        stock_gte=graphene.Int(),
        stock_lte=graphene.Int(),
        low_stock=graphene.Boolean(),
        order_by=graphene.String()
    )
    
    all_orders = graphene.List(
        OrderType,
        total_amount_gte=graphene.Float(),
        total_amount_lte=graphene.Float(),
        order_date_gte=graphene.DateTime(),
        order_date_lte=graphene.DateTime(),
        customer_name=graphene.String(),
        product_name=graphene.String(),
        product_id=graphene.Int(),
        order_by=graphene.String()
    )
    
    customer = graphene.Field(CustomerType, id=graphene.ID(required=True))
    product = graphene.Field(ProductType, id=graphene.ID(required=True))
    order = graphene.Field(OrderType, id=graphene.ID(required=True))

    def resolve_all_customers(self, info, **kwargs):
        queryset = Customer.objects.all()
        
        # Convert GraphQL camelCase to snake_case for filter
        filter_kwargs = {}
        order_by = None
        
        for key, value in kwargs.items():
            if key == 'order_by':
                order_by = value
            elif key == 'created_at_gte':
                filter_kwargs['created_at__gte'] = value
            elif key == 'created_at_lte':
                filter_kwargs['created_at__lte'] = value
            else:
                filter_kwargs[key] = value
        
        # Apply filters
        filterset = CustomerFilter(filter_kwargs, queryset=queryset)
        queryset = filterset.qs
        
        # Apply ordering
        if order_by:
            queryset = queryset.order_by(order_by)
        
        return queryset

    def resolve_all_products(self, info, **kwargs):
        queryset = Product.objects.all()
        
        # Convert GraphQL camelCase to snake_case for filter
        filter_kwargs = {}
        order_by = None
        
        for key, value in kwargs.items():
            if key == 'order_by':
                order_by = value
            elif key == 'price_gte':
                filter_kwargs['price__gte'] = value
            elif key == 'price_lte':
                filter_kwargs['price__lte'] = value
            elif key == 'stock_gte':
                filter_kwargs['stock__gte'] = value
            elif key == 'stock_lte':
                filter_kwargs['stock__lte'] = value
            else:
                filter_kwargs[key] = value
        
        # Apply filters
        filterset = ProductFilter(filter_kwargs, queryset=queryset)
        queryset = filterset.qs
        
        # Apply ordering
        if order_by:
            queryset = queryset.order_by(order_by)
        
        return queryset

    def resolve_all_orders(self, info, **kwargs):
        queryset = Order.objects.all().distinct()
        
        # Convert GraphQL camelCase to snake_case for filter
        filter_kwargs = {}
        order_by = None
        
        for key, value in kwargs.items():
            if key == 'order_by':
                order_by = value
            elif key == 'total_amount_gte':
                filter_kwargs['total_amount__gte'] = value
            elif key == 'total_amount_lte':
                filter_kwargs['total_amount__lte'] = value
            elif key == 'order_date_gte':
                filter_kwargs['order_date__gte'] = value
            elif key == 'order_date_lte':
                filter_kwargs['order_date__lte'] = value
            else:
                filter_kwargs[key] = value
        
        # Apply filters
        filterset = OrderFilter(filter_kwargs, queryset=queryset)
        queryset = filterset.qs.distinct()
        
        # Apply ordering
        if order_by:
            queryset = queryset.order_by(order_by)
        
        return queryset

    def resolve_customer(self, info, id):
        try:
            return Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return None

    def resolve_product(self, info, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None

    def resolve_order(self, info, id):
        try:
            return Order.objects.get(id=id)
        except Order.DoesNotExist:
            return None


# Mutation
class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
