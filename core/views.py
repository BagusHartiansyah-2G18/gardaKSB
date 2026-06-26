from django.shortcuts import render,redirect

from django.contrib.auth import authenticate, login as auth_login

from django.contrib import messages


# Create your views here.


def home(request):
    data =  [
        {
            "nama": "Kelompok Nelayan",
            "deskripsi": "Kelompok masyarakat yang melakukan penangkapan ikan di laut",
            "url": "https://png.pngtree.com/png-vector/20211015/ourlarge/pngtree-fishing-logo-png-image_3984708.png"
        },
        {
            "nama": "Pokdakan",
            "deskripsi": "Kelompok pembudidaya ikan (kolam, tambak, keramba)",
            "url": "https://1.bp.blogspot.com/-PAwtbR5Xp7Y/X2oXKU1fnCI/AAAAAAAALP0/P0NLN2cSKeoV1dUnl0lvQIr-1yQD_qc_ACNcBGAsYHQ/s400/LOGO%2BPOKDAKAN.jpg"
        },
        {
            "nama": "Poklahsar",
            "deskripsi": "Kelompok pengolah dan pemasaran hasil perikanan",
            "url": "https://img.icons8.com/color/96/fish-food.png"
        },
        {
            "nama": "Kelompok Usaha Bersama (KUB)",
            "deskripsi": "Kelompok usaha ekonomi bersama bidang perikanan",
            "url": "https://2.bp.blogspot.com/-XBzyP9GMol8/Vte34zUu-MI/AAAAAAAAEAo/-KNK48jOhrkOE1xyqPOj-iv3p1bxF5kQg/w1200-h630-p-k-no-nu/DUTA%2BLAUT.jpg"
        },
        {
            "nama": "Pokmaswas",
            "deskripsi": "Kelompok masyarakat pengawas kegiatan kelautan dan perikanan",
            "url": "https://img.icons8.com/color/96/shield.png"
        }
    ]




    return render(request, 'publik/home.html', {
        'features': data
    })
def login(request):
    return render(request, 'publik/login.html', {
        'features': []
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')  # ganti ke url kamu
        else:
            messages.error(request, 'Username atau password salah')

    return render(request, 'publik/login.html')


def dashboard(request):
    return render(request, 'dashboard/kelompok.html')

