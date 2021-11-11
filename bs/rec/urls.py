from django.urls import path
from .import views

#--- ADDED THIS SECTION TO UPLOAD PHOTOS !!!! ---
from django.conf.urls.static import static
from django.conf import settings

from django.conf.urls import url
from .models import Gldetail
#------------------------------------------------

urlpatterns = [
    path('import', views.import_data, name='gldetail-import'),
    path('', views.GldetailView.as_view(), name='gldetail-list'),
    path('status', views.StatusView.as_view(), name='status'),
    path('gldetail/add/', views.GldetailGlpostCreate.as_view(), name='gldetail-add'),
    path('gldetail/<int:pk>', views.GldetailGlpostUpdate.as_view(), name='gldetail-update'),
    path('gldetail/<int:pk>', views.GldetailDelete.as_view(), name='gldetail-delete'),
]

#--- ADDED THIS SECTION TO UPLOAD PHOTOS !!!! ---
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#