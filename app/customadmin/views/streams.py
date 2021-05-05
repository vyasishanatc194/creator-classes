# -*- coding: utf-8 -*-
from customadmin.mixins import HasPermissionsMixin
from customadmin.views.generic import (
    MyDeleteView,
    MyListView,
    MyLoginRequiredView,
    MyDetailView,
    MyNewFormsetCreateView,
    MyNewFormsetUpdateView,
    get_aws_s3_creds
)
from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin
from django.views.generic import DetailView

from customadmin.forms import StreamChangeForm, StreamCreationForm, StreamKeywordCreationForm, StreamKeywordChangeForm, StreamCoversCreationForm, StreamCoversChangeForm
from django.shortcuts import reverse, render

from creator.models import Stream, StreamKeyword, StreamCovers
from user.models import StreamBooking
from extra_views import InlineFormSetFactory

from django.contrib import messages

MSG_CREATED = '"{}" created successfully.'
MSG_UPDATED = '"{}" updated successfully.'
MSG_DELETED = '"{}" deleted successfully.'
MSG_CANCELED = '"{}" canceled successfully.'

# -----------------------------------------------------------------------------
# Creator Stream
# -----------------------------------------------------------------------------


class StreamDetailView(MyDetailView):
    model = Stream
    template_name = "customadmin/streams/stream_detail.html"
    permission_required = ("customadmin.view_stream_detail",)
    context = {}

    def get(self, request, pk):
        self.context['stream_detail'] = Stream.objects.filter(pk=pk).first()
        self.context['sneak_peak_file_url'] = request.build_absolute_uri(self.context['stream_detail'].sneak_peak_file)
        self.context['sneak_peak_file_url'] = self.context['sneak_peak_file_url'][:22] + 'media' + self.context['sneak_peak_file_url'][50:]
        self.context['stream_keyword_list'] = StreamKeyword.objects.filter(stream=pk)
        self.context['stream_cover_list'] = StreamCovers.objects.filter(stream=pk)
        self.context['user_list'] = StreamBooking.objects.filter(stream=pk)
        return render(request, self.template_name, self.context)

class StreamListView(MyListView):
    """View for Creator Stream listing"""

    ordering = ["id"]
    model = Stream
    queryset = model.objects.all()
    template_name = "customadmin/streams/stream_list.html"
    permission_required = ("customadmin.view_stream",)

    def get_queryset(self):
        return self.model.objects.all().exclude(active=False).order_by('-created_at')

class StreamKeywordInline(InlineFormSetFactory):
    """Inline view to show Keyword within the Parent View"""

    model = StreamKeyword
    form_class = StreamKeywordCreationForm
    factory_kwargs = {'extra': 4, 'max_num': 4, 'can_order': False, 'can_delete': True}

class StreamCoversInline(InlineFormSetFactory):
    """Inline view to show Cover within the Parent View"""

    model = StreamCovers
    form_class = StreamCoversCreationForm
    factory_kwargs = {'extra': 4, 'max_num': 4, 'can_order': False, 'can_delete': True}

class StreamCreateView(MyNewFormsetCreateView):
    """View to create Stream"""

    model = Stream
    inlines = [StreamKeywordInline,StreamCoversInline,]
    form_class = StreamCreationForm
    template_name = "customadmin/streams/stream_form.html"
    permission_required = ("customadmin.add_stream",)

    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data( *args, **kwargs)
        context.update(get_aws_s3_creds())
        context['path'] = 'public/stream'
        return context


    def get_success_url(self):
        messages.success(self.request, MSG_CREATED.format(self.object))
        return reverse("customadmin:stream-list")

class StreamKeywordUpdateInline(InlineFormSetFactory):
    """View to update Keyword which is a inline view"""

    model = StreamKeyword
    form_class = StreamKeywordChangeForm
    factory_kwargs = {'extra': 4, 'max_num': 4, 'can_order': False, 'can_delete': True}

class StreamCoversUpdateInline(InlineFormSetFactory):
    """View to update Cover which is a inline view"""

    model = StreamCovers
    form_class = StreamCoversChangeForm
    factory_kwargs = {'extra': 4, 'max_num': 4, 'can_order': False, 'can_delete': True}

class StreamUpdateView(MyNewFormsetUpdateView):
    """View to update Stream"""

    model = Stream
    inlines = [StreamKeywordUpdateInline,StreamCoversUpdateInline, ]
    form_class = StreamChangeForm
    template_name = "customadmin/streams/stream_form.html"
    permission_required = ("customadmin.change_stream",)

    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data( *args, **kwargs)
        context.update(get_aws_s3_creds())
        context['path'] = 'public/stream'
        return context    

    def get_success_url(self):
        messages.success(self.request, MSG_UPDATED.format(self.object))
        return reverse("customadmin:stream-list")

class StreamDeleteView(MyDeleteView):
    """View to delete Stream"""

    model = Stream
    template_name = "customadmin/confirm_delete.html"
    permission_required = ("customadmin.delete_stream",)

    def get_success_url(self):
        return reverse("customadmin:stream-list")

class StreamAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """Built this before realizing there is
    https://bitbucket.org/pigletto/django-datatables-view."""

    model = Stream
    queryset = Stream.objects.all().order_by("title")

    def _get_is_superuser(self, obj):
        """Get boolean column markup."""
        t = get_template("customadmin/partials/list_boolean.html")
        return t.render({"bool_val": obj.is_superuser})

    def _get_actions(self, obj, **kwargs):
        """Get actions column markup."""
        # ctx = super().get_context_data(**kwargs)
        t = get_template("customadmin/partials/list_basic_actions.html")
        # ctx.update({"obj": obj})
        # print(ctx)
        return t.render({"o": obj})

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(username__icontains=self.search)
                | Q(first_name__icontains=self.search)
                | Q(last_name__icontains=self.search)
                # | Q(state__icontains=self.search)
                # | Q(year__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "username": o.username,
                    "first_name": o.first_name,
                    "last_name": o.last_name,
                    "is_superuser": self._get_is_superuser(o),
                    # "modified": o.modified.strftime("%b. %d, %Y, %I:%M %p"),
                    "actions": self._get_actions(o),
                }
            )
        return data