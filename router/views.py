from django.db.models import Q
from turtle import *
from django.shortcuts import render, redirect
from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from router.models import Device
from router.serializers import DeviceSerializer


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


"""Exercise number 1 : Question num 3 Answer is in /management/commands/py file """

"""Exercise number 1 : Question num 2 """
class RouterForm(ModelForm):
    class Meta:
        model = Device
        fields = ['loopback', 'hostname','sapid','mac_address','ip_address']


def router_list(request, template_name='router/list.html'):
    all_router = Device.objects.filter(is_deleted = False)
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
    router = get_object_or_404(Device, pk=pk)
    form = RouterForm(request.POST or None, instance=router)
    if form.is_valid():
        form.save()
        return redirect('router_list')
    return render(request, template_name, {'form': form})


def router_delete(request, pk, template_name='router/delete_router.html'):
    router = get_object_or_404(Device, pk=pk)
    if request.method == 'POST':
        router.is_deleted = True
        router.save()
        return redirect('router_list')
    return render(request, template_name, {'object':router})


"""Exercise number 3 : Question num 1 """


class CreateRouterDevice(generics.CreateAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class RouterListAPIView(generics.ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_text = ''
        if self.request.query_params.get('search'):
            search_text = self.request.query_params.get('search')
        return Device.objects.filter(Q(sapid__icontains=search_text))


class RouterBasedonIPRUDView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_object(self):
        queryset = self.get_queryset()
        try:
            return queryset.get(
                ip_address=self.kwargs['ip_addr']
            )
        except queryset.model.DoesNotExist:
            pass

    def get_queryset(self):
        return Device.objects.all()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response({})

    def perform_destroy(self, instance):
        instance.delete()
        return Response({})