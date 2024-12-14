from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Listing, Category
from django.core.validators import MinValueValidator


class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control form-control-lg",
        "placeholder":"Username",
        "autofocus":True,
        "autocomplete":"off"}))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class":"form-control form-control-lg",
        "placeholder":"Email Address",
        "autocomplete":"email"}))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class":"form-control form-control-lg",
        "placeholder":"Password",
        "autocomplete":"new-password"}))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "class":"form-control form-control-lg",
        "placeholder":"Confirm Password",
        "autocomplete":"new-password"}))
    
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
        
    #     # Add is-invalid class to fields with errors
    #     for field_name, field in self.fields.items():
    #         if self.errors.get(field_name):
    #             field.widget.attrs['class'] += ' is-invalid'

class ListingForm(ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"Enter listing title",
        "autofocus":True}))
    
    description = forms.CharField(widget=forms.Textarea(attrs={
        "rows":3, 
        "placeholder":"Describe your item in detail"}), required=False)
    
    price = forms.DecimalField(label="Starting bid", widget=forms.NumberInput(attrs={
        "placeholder":"Enter price",
        "min":0.01,
        "step":0.01}),
        validators=[MinValueValidator(0.01)],
        error_messages={"min_value":"Price must be greater than 0.00"})
    
    category = forms.ModelChoiceField(queryset=Category.objects.all(), 
                                      empty_label="Select a category",
                                      required=False)
    
    class Meta:
        model = Listing
        fields = ["title", "description", "price", "image", "category"]
