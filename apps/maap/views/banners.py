# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import messages
from maap.models import PointBanner
from maap.forms import BannerForm
from django.contrib.auth.decorators import login_required

@login_required
def new_banner(request, point_id):
    form = BannerForm
    if request.method == 'POST':
        form = form(request.POST, request.FILES)
        if form.is_valid():
            messages.add_message(
                request, 
                messages.INFO, 
                u'Aviso creado con éxito',
            )
            form.save()
            return redirect('profile_detail', request.user.username,)
    else:
        
        form = form(initial={'point':point_id})
    return render(
        request,
        'maap/object_form.html',
        {
            'form': form,
        }
    )
