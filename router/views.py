from django.shortcuts import render
from turtle import *
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import ModelForm

from router.models import Device


def geometric_figure():
    """Exercise 1:4 : Write a program to draw geometric figures such as below using the coordinates"""
    setup()

    def circles(radius, colour):
        penup()
        pencolor(colour)
        goto(0, radius)
        pendown()
        setheading(180)
        circle(radius)
        penup()
    hideturtle()
    up()
    goto(0, 100)
    seth(-45)
    down()
    for _ in range(4):
        fd(60)
        left(0)
        fd(80)
        left(-90)

    circles(140, "black")

    hideturtle()
    up()
    goto(200, 0)
    seth(120)
    down()
    for _ in range(6):
        fd(200)
        left(60)
    exitonclick()

class RouterForm(ModelForm):
    class Meta:
        model = Device
        fields = ['loopback', 'hostname','sapid','mac_address','ip_address']


def router_list(request, template_name='router/list.html'):
    all_router = Device.objects.all()
    data = {}
    data['object_list'] = all_router
    return render(request, template_name, data)


def router_view(request, pk, template_name='router/details.html'):
    router= get_object_or_404(Device, pk=pk)
    return render(request, template_name, {'object':router})


def router_create(request, template_name='router/router_form.html'):
    form = RouterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('router_list')
    return render(request, template_name, {'form':form})


def router_update(request, pk, template_name='router/router_form.html'):
    router= get_object_or_404(Device, pk=pk)
    form = RouterForm(request.POST or None, instance=router)
    if form.is_valid():
        form.save()
        return redirect('router_list')
    return render(request, template_name, {'form':form})

def router_delete(request, pk, template_name='router/delete_router.html'):
    router = get_object_or_404(Device, pk=pk)
    if request.method =='POST':
        router.delete()
        return redirect('router_list')
    return render(request, template_name, {'object':router})