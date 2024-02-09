from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse,HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import  Modelo, Utilizador, Comentario
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import CreateView

#View do index:
def index(request):
    promocoes = Modelo.objects.order_by('preço')[:5]
    resultados = Modelo.objects.all()
    novidades = Modelo.objects.order_by('data_lançamento')[:5]

    return render(request, 'website/index.html', {'promocoes': promocoes, 'resultados':resultados,'novidades':novidades}, )



def support(request):
    return render(request, 'website/supportView.html')

def contacts(request):
    return render(request, 'website/contactsView.html')

def aboutus(request):
    return render(request, 'website/aboutusView.html')





def searchView(request):


    if request.method == "POST":

        try:
             search = request.POST.get('search')
             resultados = Modelo.objects.filter(marca__contains=search)

        except KeyError:
             return render(request, 'website/index.html')
        if search is not None:
             return render(request, 'website/search.html', {'search':search,'resultados':resultados} )
        else:
             return render(request, 'website/index.html', {'search': search})
    else:
        return render(request, 'website/index.html',)





def pedeRegisto(request):
 return render(request,'website/register.html')

def register(request):
 email= request.POST.get('email')
 nome=request.POST.get('nome')
 password= request.POST.get('psw')
 foto_file= request.FILES.get('foto')
 pais = request.POST.get('pais')
 telemovel = request.POST.get('telemovel')
 ocupacao = request.POST.get('ocupacao')

 utilizador = authenticate(username=nome, email=email, password=password)

 fs = FileSystemStorage()
 if foto_file is not None:
  filename = fs.save(foto_file.name, foto_file)
  uploaded_file_url = fs.url(filename)
# utilizador = authenticate(username=nome, email=email,  password=password)
 if utilizador is not None:
  return render(request,'website/erroRegisto.html')
 else:
  u= User.objects.create_user(username=nome, email=email,  password=password)
  if foto_file is not None:
   u = Utilizador(user=u, foto=uploaded_file_url, pais=pais, ocupacao=ocupacao, telemovel = telemovel)
   u.save()
   return HttpResponseRedirect(reverse('website:index'))
  else:
   u = Utilizador(user=u, foto=fs.url('/static/default.jpg'), pais=pais, ocupacao=ocupacao, telemovel = telemovel)
   u.save()
   return HttpResponseRedirect(reverse('website:index'))



def pedeLogin(request):
 return render(request, 'website/loginView.html')

def loginView(request):
 username = request.POST['nome']
 password = request.POST['psw']
 user = authenticate(username=username, password=password)
 if user is not None:
   login(request, user)
   return HttpResponseRedirect(reverse('website:index'))
 else:
  return render(request,'website/erroLogin.html')

def pedeLogout(request):
 return render(request, 'website/index.html')



def logoutView(request):
     logout(request)
     request.session.flush()
     return HttpResponseRedirect(reverse('website:index'))



@login_required
def perfilView(request):
    utilizador = request.user.utilizador
    lista_modelos = Modelo.objects.order_by('-data_lançamento').filter( id_user=utilizador)
    return render(request, 'website/perfil.html', {'lista_modelos':lista_modelos})



@login_required
def addModelView(request):

    if request.method == 'POST' and request.FILES['foto']:
        try:
            user_id=request.user.utilizador
            marca      =request.POST.get('marca')
            nome_modelo=request.POST.get('nome_modelo')
            tamanho    =request.POST.get('tamanho')
            referência =request.POST.get('referência')
            preço      =request.POST.get('preço')
            tipo       =request.POST.get('tipo')
            foto       =request.FILES.get('foto')
            fs = FileSystemStorage()
        except KeyError:
            return render(request, 'website/addModel.html')
        if foto is not None:
            foto_f = fs.save(foto.name, foto)
            uploaded_foto_url = fs.url(foto_f)
            criar_modelo = Modelo(marca=marca, nome_modelo=nome_modelo, tamanho=tamanho,
                              referência=referência, preço=preço, data_lançamento=timezone.now(),
                              tipo=tipo, foto=uploaded_foto_url, id_user=user_id)
            criar_modelo.save()
            return HttpResponseRedirect(reverse('website:perfilView'))
        else:
         criar_modelo = Modelo(marca=marca, nome_modelo=nome_modelo, tamanho=tamanho,
                              referência=referência, preço=preço, data_lançamento=timezone.now(),
                              tipo=tipo, foto=fs.url('default.jpg'), id_user=user_id)
         criar_modelo.save()
         return HttpResponseRedirect(reverse('website:perfilView',))
    else:
     return render(request, 'website/addModel.html')

def detalhe(request, modelo_id):
    modelo=get_object_or_404(Modelo, pk=modelo_id)
    lista_coments = Comentario.objects.all()
    return render(request, 'website/detalhe.html', {'modelo':modelo,'lista_coments':lista_coments})


@login_required
def deleteModelView(request, modelo_id):
 modelo_id=get_object_or_404(Modelo, pk=modelo_id)
 modelo_id.delete()
 return HttpResponseRedirect(reverse('website:index'))



@permission_required('user.is_superuser')
def listaClientesView(request):
    usersList = Utilizador.objects.all()
    print(usersList)
    return render(request, 'website/listaClientes.html', {"usersList":usersList})



@permission_required('user.is_superuser')
def apagaCliente(request, user_id):
 user=get_object_or_404(User, pk=user_id)

 user.delete()
 #apaga o user não apaga o utilizador e redireciona mal
 return HttpResponseRedirect(reverse('website:listaClientesView'))


@login_required
def addComentView(request, modelo_id):
    lista_coments = Comentario.objects.all()
    user=request.user.utilizador
    modelo=get_object_or_404(Modelo, pk=modelo_id)
    if request.method == 'POST':
        try:
            texto=request.POST.get('texto')

        except KeyError:
            return render(request, 'website/detalhe.html',{'lista_coments':lista_coments,'modelo':modelo})

        comentario= Comentario(modelo=modelo, utilizador=user, texto=texto, data=timezone.now())
        comentario.save()

    return render(request,'website/detalhe.html',{'lista_coments':lista_coments, 'modelo':modelo})

def buyModelView(request, modelo_id):
 modelo_id=get_object_or_404(Modelo, pk=modelo_id)
 modelo_id.delete()
 return HttpResponseRedirect(reverse('website:index'))