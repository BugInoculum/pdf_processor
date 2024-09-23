from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from pdf_app.views import PDFDocumentViewSet
router = routers.DefaultRouter()
router.register(r'documents', PDFDocumentViewSet, basename='documents')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
