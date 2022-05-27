from django.shortcuts import render, redirect, HttpResponse
from perpustakaan.models import Buku
from perpustakaan.forms import FormBuku
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    template = 'home.html'
    return render(request, template)


@login_required(login_url=settings.LOGIN_URL)
def users(request):
    users = User.objects.all()
    template = 'users.html'
    context = {
        'users':users,
    }
    return render(request, template, context)


@login_required(login_url=settings.LOGIN_URL)
def signup(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User berhasil dibuat!")
            return redirect('signup')
        else:
            messages.error(request, "Terjadi kesalahan!")
            return redirect('signup')
    else:
        form = UserCreationForm()
        konteks = {
            'form':form,
        }        
    return render(request, 'signup.html', konteks)


@login_required(login_url=settings.LOGIN_URL)
def hapus_buku(request, id_buku):
    buku = Buku.objects.filter(id=id_buku)
    buku.delete()
    
    messages.success(request, "Data Berhasil dihapus !")
    return redirect('buku')

@login_required(login_url=settings.LOGIN_URL)
def ubah_buku(request, id_buku):
    buku = Buku.objects.get(id=id_buku)
    template = 'ubah-buku.html'
    if request.POST:
        form = FormBuku(request.POST, request.FILES, instance=buku)
        if form.is_valid():
            form.save()
            messages.success(request, "Data Berhasil diperbaharui!")
            return redirect('ubah_buku', id_buku=id_buku)
    else:
        form=FormBuku(instance=buku)
        konteks = {
            'form':form,
            'buku':buku,
        }
    return render(request, template, konteks)


@login_required(login_url=settings.LOGIN_URL)
def buku(request):
    # select * from Buku where jumlah = 90
    # inner join kelompok.id = id=buku.kelompok_id
    # where kelompok.nama='produktif'
    # di sql _> limit 3
    #books = Buku.objects.all(kelompok_id__nama='Produktif')[:4]
    books = Buku.objects.all()
    

    konteks = {
        'books': books,
    }
    return render(request,'buku.html',konteks)

@login_required(login_url=settings.LOGIN_URL)
def penerbit(request):
    return render(request,'penerbit.html')

@login_required(login_url=settings.LOGIN_URL)
def tambah_buku(request):
    if request.POST:
        form = FormBuku(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = FormBuku()
            pesan = "Data berhasil disimpan"

            konteks = {
                'form' : form,
                'pesan': pesan,
            }
            return render(request, 'tambah-buku.html', konteks)
    else:
        form = FormBuku()

        konteks = {
            'form': form,
        }

    return render(request,'tambah-buku.html', konteks)