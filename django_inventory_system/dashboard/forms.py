from django import forms
from .models import Product, Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'quantity', 'product_image', 'description']
        labels = {
            'name': 'Product Name',
            "price": "Product Price ₱/kg",
            'quantity': 'Product Quantity',
            'product_image': 'Product Image',
            'description': 'Product Description',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter product name', 'style': 'width: 400px;'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter product price', 'style': 'width: 400px;'}),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Enter product quantity', 'style': 'width: 400px;'}),
            'product_image': forms.ClearableFileInput(attrs={'style': 'width: 400px;'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter product description', 'style': 'width: 400px; height: 60px;'}),
        }

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True 
            field.help_text = ''  
            field.label_suffix = ''  


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'product', 'quantity', 'order_notes']
        labels = {
            'customer_name': 'Customer Name',
            'product': 'Product',
            'quantity': 'Quantity',
            'order_notes': 'Order Notes',
        }
        widgets = {
            'customer_name': forms.TextInput(attrs={'placeholder': 'Enter customer name' ,  'style': 'width: 400px;'}),
            'product': forms.Select(attrs={ 'style': 'width: 415px; height: 33px;' }),
            'quantity': forms.NumberInput(attrs={'placeholder': 'Enter quantity' ,  'style': 'width: 400px;'}),
            'order_notes': forms.Textarea(attrs={'placeholder': 'Enter order notes' , 'style': 'width: 400px; height: 60px;'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        # Filter products with quantity > 0
        self.fields['product'].queryset = Product.objects.filter(quantity__gt=0)

class CreateUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name', 'style': 'width: 500px;'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name', 'style': 'width: 500px;'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter username', 'style': 'width: 500px;'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email', 'style': 'width: 500px;'}),
        }