from django.shortcuts import render, get_object_or_404, redirect
from webapp.forms import StatusForm
from webapp.models import Status
from django.views import View
from django.views.generic import TemplateView






class StatusView(TemplateView):
    template_name = 'status/status_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        return context

class StatusCreateView(View):
    def get(self, request, *args, **kwargs):
        form = StatusForm()
        return render(request, 'status/create_status.html', context={'form': form, })

    def post(self, request, *args, **kwargs):
        form = StatusForm(data=request.POST)
        if form.is_valid():
            status = Status.objects.create(
                name=form.cleaned_data['name']
            )
            return redirect('status_view')
        else:
            return render(request, 'status/create_status.html', context={'form': form})

def status_update_view(request, pk):
    status = get_object_or_404(Status, pk=pk)
    if request.method == 'GET':
        form = StatusForm(data={
            'name': status.name
        })
        return render(request, 'status/update_status.html', context={'form': form, 'status': status})
    elif request.method == 'POST':
        form = StatusForm(data=request.POST)
        if form.is_valid():
            status.name = form.cleaned_data['name']
            status.save()
            return redirect('status_view')
        else:
            return render(request, 'status/update_status.html', context={'form': form, 'status': status})


class StatusDeleteView(View):
    def get(self, request, *args, **kwargs):
        status = get_object_or_404(Status, pk=kwargs.get('pk'))
        return render(request, 'status/delete_status.html', context={'status': status})

    def post(self, request, *args, **kwargs):
        status = get_object_or_404(Status, pk=kwargs.get('pk'))
        status.delete()
        return redirect('status_view')
