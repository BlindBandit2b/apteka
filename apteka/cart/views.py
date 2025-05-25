from django.shortcuts import render, redirect, get_object_or_404
from .cart import Cart
from django.views import View
from main.models import DrugItem, DrugItemSvoistvo, Svoistvo


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})


def cart_add(request, item_id):
    cart = Cart(request)
    drug_item = get_object_or_404(DrugItem, id=item_id)
    svoistvo = request.POST.get('svoistvo')

    if svoistvo:
        try:
            svoistvo_obj = Svoistvo.objects.get(name=svoistvo)
            drug_item_svoistvo = DrugItemSvoistvo.objects.get(drug_item=drug_item,
                                                              svoistvo=svoistvo_obj)
            if not drug_item_svoistvo.available:
                return redirect('cart:cart_detail')
        except Svoistvo.DoesNotExist:
            return redirect('cart:cart_detail')
        except DrugItemSvoistvo.DoesNotExist:
            return redirect('cart:cart_detail')
    else:
        available_svoistvos = drug_item.svoistvos.filter(drugitemsvoistvo__available=True)
        if available_svoistvos.exists():
            svoistvo_obj = available_svoistvos.first()
            svoistvo = svoistvo_obj.name
        else:
            return redirect('cart:cart_detil')

    cart.add(drug_item, svoistvo)
    return redirect('cart:cart_detail')


def cart_remove(request, item_id):
    cart = Cart(request)
    drug_item = get_object_or_404(DrugItem, id=item_id)
    cart.remove(drug_item)
    return redirect('cart:cart_detail')


class CartUpdateView(View):
    def post(self, request, item_id):
        cart = Cart(request)
        quantity = request.POST.get('quantity', 1)
        try:
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
        drug_item = get_object_or_404(DrugItem, id=item_id)

        if quantity > 0:
            cart.add(drug_item, cart.cart[str(item_id)]['svoistvo'], quantity)
        else:
            cart.remove(drug_item)

        return redirect('cart:cart_detail')