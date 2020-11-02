# # -*- coding: utf-8 -*-
# from customadmin.mixins import HasPermissionsMixin
# from customadmin.views.generic import (
#     MyCreateView,
#     MyDeleteView,
#     MyListView,
#     MyLoginRequiredView,
#     MyUpdateView,
#     MyView,
# )
# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import AdminPasswordChangeForm
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.auth.models import Group
# from django.db.models import Q
# from django.http import JsonResponse, HttpResponse
# from django.template.loader import get_template
# from django.utils.text import Truncator
# from django.views.generic import TemplateView
# from django_datatables_too.mixins import DataTableMixin

# from creator.forms import MyCreatorChangeForm, MyCreatorCreationForm
# from django.shortcuts import reverse

# from creator.models import Creator 

# import csv


# # User = get_user_model()


# # Export CSV FILE

# # def export_user_csv(request):

# #     output = []
# #     response = HttpResponse (content_type='text/csv')
# #     filename = u"User.csv"
# #     response['Content-Disposition'] = u'attachment; filename="{0}"'.format(filename)
   
# #     writer = csv.writer(response)
# #     query_set = User.objects.all()

# #     #Header
# #     writer.writerow(['Name', "Username",'Bio', 'Email', 'Status','Phone','User Type',"is_staff", "is_superuser","avatar","company"])
# #     for user in query_set:
# #         if user.groups.all():
# #             gp = user.groups.all()[0].name
# #         else:
# #             gp = None 

# #         if not user.profile_image:
# #             avatar = None
# #         else:
# #             avatar = user.profile_image.url


# #         output.append([user.first_name, user.last_name, user.username, user.email, user.is_active,user.description,gp,user.is_staff, user.is_superuser, request.build_absolute_uri(avatar),])
# #     #CSV Data
# #     writer.writerows(output)
# #     return response





# class IndexView(LoginRequiredMixin, TemplateView): 
#     template_name = "customadmin/index.html"

# # -----------------------------------------------------------------------------
# # Users
# # -----------------------------------------------------------------------------


# class CreatorListView(MyListView):
#     """View for User listing"""

#     # paginate_by = 25
#     ordering = ["id"]
#     model = Creator
#     queryset = model.objects.all()
#     template_name = "customadmin/creator/creator_list.html"
#     permission_required = ("customadmin.view_creator",)

#     def get_queryset(self):
#         print(self.model)
#         print(self.model._meta)
#         print(type(self.model._meta))
#         return self.model.objects.all()


# class CreatorCreateView(MyCreateView):
#     """View to create User"""

#     model = Creator
#     form_class = MyCreatorCreationForm
#     template_name = "customadmin/creator/creator_form.html"
#     permission_required = ("customadmin.add_creator",)

#     # def get_form_kwargs(self):
#     #     kwargs = super().get_form_kwargs()
#     #     kwargs["user"] = self.request.user 
#     #     return kwargs

#     def get_success_url(self):
#         opts = self.model._meta
#         return reverse("customadmin:creator-list")

# class CreatorUpdateView(MyUpdateView):
#     """View to update User"""

#     model = Creator
#     form_class = MyCreatorChangeForm
#     template_name = "customadmin/creator/creator_form_update.html"
#     permission_required = ("customadmin.change_creator",)

#     # def get_form_kwargs(self):
#     #     kwargs = super().get_form_kwargs()
#     #     kwargs["user"] = self.request.user
#     #     return kwargs

#     def get_success_url(self):
#         opts = self.model._meta
#         return reverse("customadmin:creator-list")

# class CreatorDeleteView(MyDeleteView):
#     """View to delete User"""

#     model = Creator
#     template_name = "customadmin/confirm_delete.html"
#     permission_required = ("customadmin.delete_creator",)

#     def get_success_url(self):
#         opts = self.model._meta
#         return reverse("customadmin:creator-list")

# class CreatorAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
#     """Built this before realizing there is
#     https://bitbucket.org/pigletto/django-datatables-view."""

#     model = Creator
#     queryset = Creator.objects.all().order_by("key_skill")

#     def _get_is_superuser(self, obj):
#         """Get boolean column markup."""
#         t = get_template("customadmin/partials/list_boolean.html")
#         return t.render({"bool_val": obj.is_superuser})

#     def _get_actions(self, obj, **kwargs):
#         """Get actions column markup."""
#         # ctx = super().get_context_data(**kwargs)
#         t = get_template("customadmin/partials/list_basic_actions.html")
#         # ctx.update({"obj": obj})
#         # print(ctx)
#         return t.render({"o": obj})

#     def filter_queryset(self, qs):
#         """Return the list of items for this view."""
#         # If a search term, filter the query
#         if self.search:
#             return qs.filter(
#                 Q(username__icontains=self.search)
#                 | Q(first_name__icontains=self.search)
#                 | Q(last_name__icontains=self.search)
#                 # | Q(state__icontains=self.search)
#                 # | Q(year__icontains=self.search)
#             )
#         return qs

#     def prepare_results(self, qs):
#         # Create row data for datatables
#         data = []
#         for o in qs:
#             data.append(
#                 {
#                     "username": o.username,
#                     "first_name": o.first_name,
#                     "last_name": o.last_name,
#                     "is_superuser": self._get_is_superuser(o),
#                     # "modified": o.modified.strftime("%b. %d, %Y, %I:%M %p"),
#                     "actions": self._get_actions(o),
#                 }
#             )
#         return data