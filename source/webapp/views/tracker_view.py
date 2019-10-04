from django.shortcuts import render, get_object_or_404, redirect
from webapp.forms import TrackerForm
from webapp.models import Tracker
from django.views import View
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'tracker/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trackers'] = Tracker.objects.all()
        return context


class TrackerView(TemplateView):
    template_name = 'tracker/deteailed.html'

    def get_context_data(self, **kwargs):
        pk = kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        context['tracker'] = get_object_or_404(Tracker, pk=pk)
        return context


class TrackerCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TrackerForm()
        return render(request, 'tracker/create.html', context={'form': form, })

    def post(self, request, *args, **kwargs):
        form = TrackerForm(data=request.POST)
        if form.is_valid():
            issue = Tracker.objects.create(
                summary=form.cleaned_data['summary'],
                description=form.cleaned_data['description'],
                status=form.cleaned_data['status'],
                type=form.cleaned_data['type']
            )
            return redirect('tracker_view', pk=issue.pk)
        else:
            return render(request, 'tracker/create.html', context={'form': form})





class TrackerUpdateView(View):
    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(Tracker, pk=kwargs.get('pk'))
        form = TrackerForm(data={
            'summary': issue.summary,
            'description': issue.description,
            'status': issue.status_id,
            'type': issue.type_id
        })
        return render(request, 'tracker/update.html', context={'form': form, 'issue': issue})

    def post(self, request, *args, **kwargs):
        issue = get_object_or_404(Tracker, pk=kwargs.get('pk'))
        form = TrackerForm(data=request.POST)
        if form.is_valid():
            issue.summary = form.cleaned_data['summary']
            issue.description = form.cleaned_data['description']
            issue.status = form.cleaned_data['status']
            issue.type = form.cleaned_data['type']
            issue.save()
            return redirect('tracker_view', pk=issue.pk)
        else:
            return render(request, 'tracker/update.html', context={'form': form, 'issue': issue})



class TrackerDeleteView(View):
    def get(self, request, *args, **kwargs):
        issue = get_object_or_404(Tracker, pk=kwargs.get('pk'))
        return render(request, 'tracker/delete.html', context={'issue': issue})

    def post(self, request, *args, **kwargs):
         issue = get_object_or_404(Tracker, pk=kwargs.get('pk'))
         issue.delete()
         return redirect('index')

