from django.urls import include, path
from . import views
app_name= 'website'
urlpatterns = [
 path("", views.index, name="index"),
 path('search', views.searchView, name= 'searchView'),

path('support', views.support, name='support'),
path('aboutus', views.aboutus, name='aboutus'),
path('contacts', views.contacts, name='contacts'),
path('register', views.register, name='register'),
path('pedeRegisto', views.pedeRegisto, name='pedeRegisto'),

path('loginView', views.loginView, name='loginView'),
path('pedeLogin', views.pedeLogin, name='pedeLogin'),
path('logoutView', views.logoutView, name='logoutView'),

path('perfilView', views.perfilView, name='perfilView'),

path('addModelView', views.addModelView, name='addModelView'),

path('<int:modelo_id>/compraModel', views.buyModelView, name='buyModelView'),

path('addModelView', views.addModelView, name='addModelView'),
path('<int:modelo_id>', views.detalhe, name='detalhe'),
path('<int:modelo_id>/addComentView', views.addComentView, name='addComentView'),


path('<int:modelo_id>/deleteModel', views.deleteModelView, name='deleteModelView'),


path('listaClientesView', views.listaClientesView, name='listaClientesView'),
path('<int:user_id>/detalhe/apagaCliente', views.apagaCliente, name='apagaCliente'),
]