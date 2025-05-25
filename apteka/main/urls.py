from .views import CatalogView, DrugItemDetailView
from django.urls import path


app_name = 'main'

urlpatterns = [
    path('', CatalogView.as_view(), name='catalog'),
    path('item/<slug:slug>/', DrugItemDetailView.as_view(),
         name='drug_item_detail')
]