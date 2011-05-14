# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib import messages
from maap.models import PointBanner
from maap.forms import BannerForm

def new_banner(request):
    form = BannerForm
    if request.method == 'POST':
        form = BannerForm(request)

        if form.is_valid():
    
            messages.add_message(
                request, 
                messages.INFO, 
                u'Aviso creado con éxito',
            )
            form.save()
    
    return render(
        request,
        'banners/banner_form.html',
        {
            'form': form,
        }
    )
