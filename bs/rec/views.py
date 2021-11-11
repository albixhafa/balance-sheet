from django.db import transaction
from django.db.models import Count, Sum, F, Q, Case, When
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, View
from .forms import GlpostFormSet
from .models import Glpost, Gldetail, Entity, Period, Status
from django_filters.views import FilterView
from .forms import GldetailViewForm, GldetailForm, StatusViewForm
from tablib import Dataset
from .resources import GldetailResource
import tablib
from django.http import HttpResponse
from django.contrib import messages
from django.db.models.functions import Coalesce
from decimal import Decimal
import itertools
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.
def import_data(request):
    if request.method == 'POST':
        gldetail_resource = GldetailResource()
        dataset = Dataset()
        new_gldetails = request.FILES['myfile']

        imported_data = dataset.load(new_gldetails.read().decode('utf-8'), format='csv')
        result = gldetail_resource.import_data(dataset, dry_run=True)  # Test the data import

        if result.has_errors():
            messages.success(request, 'Import file contains errors!')
        else:
            gldetail_resource.import_data(dataset, dry_run=False)  # Actually import now
            messages.success(request, 'Import file uploaded successfully!')
     
    return render(request, 'rec/gldetail_import.html')

class GldetailView(View):

    def get(self, request):
        form = GldetailViewForm(request.user)
        return render(request, "rec/gldetail_list.html", {'form': form})

    def post(self, request):
        entities = None
        periods = None
        gldetails = None
        form = GldetailViewForm(request.user, request.POST)
        if request.method == 'POST':
            if form.is_valid():
                entities = Entity.objects.get(entity=form.cleaned_data['entity'])
                periods = Period.objects.get(period=form.cleaned_data['period'])
                post_field_name = Glpost._meta.get_field('gldetail').related_query_name()
                field_ref = f"{post_field_name}__jamt"
                gldetails = Gldetail.objects.filter(entity=entities, period=periods, entity__users=request.user).annotate(total_sales=Coalesce(Sum(field_ref),0))
            args = {'form': form, 'periods': periods, 'entities': entities, 'gldetails': gldetails}
        return render(request, "rec/gldetail_list.html", args)

class StatusView(View):

    def get(self, request):
        form = StatusViewForm()
        return render(request, "rec/status.html", {'form': form})

    def post(self, request):
        periods = None
        status = None
        form = StatusViewForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                periods = Period.objects.get(period=form.cleaned_data['period'])
                status = Gldetail.objects.filter(period=periods, entity__users=request.user).values(
                    "entity__entity").annotate(
                        count_pending=Count(Case(When(status=1, then=1))),
                        count_inprogress=Count(Case(When(status=2, then=1))),
                        count_completed=Count(Case(When(status=3, then=1))),
                    ).order_by("entity")
            args = {'form': form, 'periods': periods, 'status': status }
        return render(request, "rec/status.html", args)

class GldetailCreate(CreateView):
    model = Gldetail
    fields = ['entity', 'period', 'glnum', 'gldesc', 'glamt']

class GldetailGlpostCreate(CreateView):
    model = Gldetail
    fields = ['entity', 'period', 'glnum', 'gldesc', 'glamt']
    success_url = reverse_lazy('gldetail-list')

    def get_context_data(self, **kwargs):
        data = super(GldetailGlpostCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['glposts'] = GlpostFormSet(self.request.POST, self.request.FILES)
        else:
            data['glposts'] = GlpostFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        glposts = context['glposts']
        with transaction.atomic():
            self.object = form.save()
            if glposts.is_valid():
                glposts.instance = self.object
                glposts.save()
        return super(GldetailGlpostCreate, self).form_valid(form)

class PostMixin(LoginRequiredMixin):
    def form_valid(self, form):
        form.instance.username = self.request.user
        return super().form_valid(form)

class GldetailGlpostUpdate(PostMixin, UpdateView):
    model = Gldetail
    form_class = GldetailForm
    success_url = reverse_lazy('gldetail-list')

    def get_context_data(self, **kwargs):
        data = super(GldetailGlpostUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['glposts'] = GlpostFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['glposts'] = GlpostFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        glposts = context['glposts']
        with transaction.atomic():
            self.object = form.save()
            if glposts.is_valid():
                glposts.instance = self.object
                glposts.save()
        return super(GldetailGlpostUpdate, self).form_valid(form)

class GldetailDelete(DeleteView):
    model = Gldetail
    success_url = reverse_lazy('gldetail-list')

def password_success(request):
    return render(request, 'rec/password_success.html', {})