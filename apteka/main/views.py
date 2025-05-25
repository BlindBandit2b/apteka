from django.views.generic import ListView, DetailView
from .models import Svoistvo, Category, DrugItem, DrugItemSvoistvo
from django.db.models import Q


class CatalogView(ListView):
    model = DrugItem
    template_name = 'main/product/list.html'
    context_object_name = 'drug_items'

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slugs = self.request.GET.getlist('category')
        svoistvo_names = self.request.GET.getlist('svoistvo')
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        search_query = self.request.GET.get('q')

        if category_slugs: 
            queryset = queryset.filter(category__slug__in=category_slugs)

        if svoistvo_names:
            queryset = queryset.filter(
                Q(svoistvos__name__in=svoistvo_names) & Q(svoistvos__drugitemsvoistvo__available=True)
            ).distinct()
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            ).distinct()

        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['svoistvo'] = Svoistvo.objects.all()
        context['selected_categories'] = self.request.GET.getlist('category')
        context['selected_svoistvo'] = self.request.GET.getlist('svoistvo')
        context['min_price'] = self.request.GET.get('min_price', '')
        context['max_price'] = self.request.GET.get('max_price', '')

        return context
    
class DrugItemDetailView(DetailView):
    model = DrugItem
    template_name = 'main/product/detail.html'
    context_object_name = 'drug_item'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        drug_item = self.object
        available_svoistvos = DrugItemSvoistvo.objects.filter(drug_item=drug_item, available=True)
        context['available_svoistvos'] = available_svoistvos
        return context
