from django import forms
from .models import Order, Dish

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['table_number', 'dishes', 'status']

    # Убедитесь, что поле dishes использует ModelMultipleChoiceField
    dishes = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.all(),  # Все доступные блюда
        widget=forms.CheckboxSelectMultiple,  # Или SelectMultiple для выпадающего списка
    )

class OrderSearchForm(forms.Form):
    search_query = forms.CharField(
        label='Поиск заказов',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Номер стола'})
    )
    status = forms.ChoiceField(
        label='Статус',
        choices=[('', 'Все статусы')] + Order.STATUS_CHOICES,
        required=False,
    )