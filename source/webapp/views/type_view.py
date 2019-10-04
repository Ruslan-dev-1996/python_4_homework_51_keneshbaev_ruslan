from django.shortcuts import render, get_object_or_404, redirect
from webapp.forms import TypeForm
from webapp.models import Type
from django.views import View
from django.views.generic import TemplateView








class TypeView(TemplateView):
    template_name = 'type/type_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['types'] = Type.objects.all()
        return context



class TypeCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TypeForm()
        return render(request, 'type/create_type.html', context={'form': form, })

    def post(self, request, *args, **kwargs):
        form = TypeForm(data=request.POST)
        if form.is_valid():
            type = Type.objects.create(
                name=form.cleaned_data['name']
            )
            return redirect('type_view')
        else:
            return render(request, 'type/create_type.html', context={'form': form})




def type_update_view(request, pk):
    type = get_object_or_404(Type, pk=pk)
    if request.method == 'GET':
        form = TypeForm(data={
            'name': type.name
        })
        return render(request, 'type/update_type.html', context={'form': form, 'type': type})
    elif request.method == 'POST':
        form = TypeForm(data=request.POST)
        if form.is_valid():
            type.name = form.cleaned_data['name']
            type.save()
            return redirect('type_view', pk=type.pk)
        else:
            return render(request, 'type/update_type.html', context={'form': form, 'type': type})






def type_delete_view(request, pk):
    type = get_object_or_404(Type, pk=pk)
    if request.method == 'GET':
        return render(request, 'type/delete_type.html', context={'type': type})
    elif request.method == 'POST':
        type.delete()
        return redirect('type_view')