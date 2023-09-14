from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm, EditItemForm
from django.db.models import Q

# Create your views here.
def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related = Item.objects.filter(category=item.category, isSold=False).exclude(pk=pk)[:3]
    return render(request, 'item/detail.html', {'item': item, 'related': related})

@login_required
def new_item(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.createdBy = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New Item'
    })


@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, createdBy=request.user)
    item.delete()
    return redirect('dashboard:index')


@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk, createdBy=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)
    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit Item'
    })

def browse(request):
    query = request.GET.get('query', '')
    qprice = float(request.GET.get('price', 0))
    items = Item.objects.filter(isSold=False)
    category_id = int(request.GET.get('category', 0))
    categories = Category.objects.all()
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if qprice > 0:
        items = items.filter(price__lte=qprice)
    if category_id > 0:
        items = items.filter(category=category_id)
    return render(request, 'item/browse.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': category_id,
        'price': qprice
    })