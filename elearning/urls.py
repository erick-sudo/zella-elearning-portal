"""elearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from django.http import HttpResponse

def greeting(request):
    print('Welcome')
    return HttpResponse( """
    <style>
        html{
            background-color: ;
            font-weight: bolder;
        }
        #home {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
        }
        h1{
            font-size: 2.5em;
        }
        a{
            text-decoration: none;
            color: white;
            font-size: 1.5em;
            background-color: green;
            padding: 0.7em 1.5em;
            border-radius: 20px;
        }
    </style>
    <div id="home">
        <h1>Welcome to Zella</h1>
        <a href="/zella/">LOGIN</a>
    </div>
    """)

urlpatterns = [
    path('zella/', include('zella.urls')),
    path('', greeting),
    path('admin/', admin.site.urls)
]
