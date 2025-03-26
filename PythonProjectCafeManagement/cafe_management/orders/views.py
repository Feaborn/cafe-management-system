from django.shortcuts import render, get_object_or_404, redirect
from .models import Order
from .forms import OrderForm, OrderSearchForm
from rest_framework import generics
from .serializers import OrderSerializer
from django.db.models import Q

def order_list(request):
    # Получаем все заказы
    orders = Order.objects.all()

    # Инициализируем форму поиска
    search_form = OrderSearchForm(request.GET)

    # Если форма поиска отправлена и валидна
    if search_form.is_valid():
        search_query = search_form.cleaned_data['search_query']
        status = search_form.cleaned_data['status']

        # Фильтруем заказы по номеру стола или статусу
        if search_query:
            orders = orders.filter(table_number__icontains=search_query)
        if status:
            orders = orders.filter(status=status)

    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'search_form': search_form,
    })

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})

from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Order

def order_create(request):
    if request.method == "POST":
        # Отладочное сообщение: проверяем данные в POST-запросе
        print(f"Данные POST: {request.POST}")
        form = OrderForm(request.POST)
        if form.is_valid():

            # Сначала сохраняем заказ, чтобы получить ID
            order = form.save(commit=False)
            order.save()  # Сохраняем заказ в базу данных

            # Теперь можно сохранить связанные блюда (ManyToManyField)
            form.save_m2m()



            # Вычисляем общую стоимость заказа
            order.total_price = sum(dish.price for dish in order.dishes.all())



            order.save()  # Сохраняем заказ с обновленной общей стоимостью

            # Перенаправляем на страницу деталей заказа
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})

def order_update(request, pk):
    # Получаем заказ по ID или возвращаем 404, если заказ не найден
    order = get_object_or_404(Order, pk=pk)

    if request.method == "POST":
        # Передаем данные из POST-запроса и текущий заказ в форму
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            # Сохраняем заказ, но пока не сохраняем в базу данных
            order = form.save(commit=False)
            order.save()  # Сохраняем заказ в базу данных

            # Сохраняем связанные блюда (ManyToManyField)
            form.save_m2m()

            # Вычисляем общую стоимость заказа
            order.total_price = sum(dish.price for dish in order.dishes.all())
            order.save()  # Сохраняем заказ с обновленной общей стоимостью

            # Перенаправляем на страницу деталей заказа
            return redirect('order_detail', pk=order.pk)
    else:
        # Передаем текущий заказ в форму для редактирования
        form = OrderForm(instance=order)

    return render(request, 'orders/order_form.html', {'form': form})

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.delete()
    return redirect('order_list')

def revenue_report(request):
    # Фильтруем заказы со статусом "оплачено"
    paid_orders = Order.objects.filter(status='paid')

    # Вычисляем общую выручку
    total_revenue = sum(order.total_price for order in paid_orders)

    return render(request, 'orders/revenue_report.html', {
        'paid_orders': paid_orders,
        'total_revenue': total_revenue,
    })


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderSearchAPIView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all()
        search_query = self.request.query_params.get('search')
        table_number = self.request.query_params.get('table_number')
        status = self.request.query_params.get('status')

        if search_query:
            queryset = queryset.filter(
                Q(table_number__icontains=search_query) |
                Q(status__icontains=search_query)
            )
        if table_number:
            queryset = queryset.filter(table_number__icontains=table_number)
        if status:
            queryset = queryset.filter(status__icontains=status)

        return queryset