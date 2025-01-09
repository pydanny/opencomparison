from django.urls import path, re_path
from django.views.generic.dates import ArchiveIndexView
from django.db.models import Count

from package.models import Package
from package.views import (
    PackageListView,
    add_example,
    add_package,
    ajax_package_list,
    confirm_delete_example,
    delete_example,
    edit_documentation,
    edit_example,
    edit_package,
    flag_approve,
    flag_package,
    flag_remove,
    github_webhook,
    package_detail,
    package_details_rules,
    package_opengraph_detail,
    fetch_package_data,
    usage,
)

urlpatterns = [
    path(
        "",
        view=PackageListView.as_view(),
        name="packages",
    ),
    path(
        "latest/",
        view=ArchiveIndexView.as_view(
            queryset=Package.objects.filter().select_related(),
            paginate_by=50,
            date_field="created",
        ),
        name="latest_packages",
    ),
    path(
        "liked/",
        view=ArchiveIndexView.as_view(
            queryset=Package.objects.annotate(
            distinct_favs=Count("favorite__favorited_by", distinct=True)
        )
        .filter(distinct_favs__gt=0),
            paginate_by=50,
            date_field="created",
        ),
        name="liked_packages",
    ),
    path(
        "add/",
        view=add_package,
        name="add_package",
    ),
    path(
        "<slug:slug>/edit/",
        view=edit_package,
        name="edit_package",
    ),
    path(
        "<slug:slug>/fetch-data/",
        view=fetch_package_data,
        name="fetch_package_data",
    ),
    path(
        "<slug:slug>/example/add/",
        view=add_example,
        name="add_example",
    ),
    path(
        "<slug:slug>/example/<int:id>/edit/",
        view=edit_example,
        name="edit_example",
    ),
    path(
        "<slug:slug>/example/<int:id>/delete/",
        view=delete_example,
        name="delete_example",
    ),
    path(
        "<slug:slug>/example/<int:id>/confirm_delete/",
        view=confirm_delete_example,
        name="confirm_delete_example",
    ),
    path(
        "<slug:slug>/flag/",
        view=flag_package,
        name="flag",
    ),
    path(
        "<slug:slug>/flag/approve/",
        view=flag_approve,
        name="flag_approve",
    ),
    path(
        "<slug:slug>/flag/remove/",
        view=flag_remove,
        name="flag_remove",
    ),
    path(
        "p/<slug:slug>/opengraph/",
        view=package_opengraph_detail,
        name="package_opengraph",
    ),
    path(
        "p/<slug:slug>/rules/",
        view=package_details_rules,
        name="package",
    ),
    path(
        "p/<slug:slug>/",
        view=package_detail,
        name="package",
    ),
    path(
        "ajax_package_list/",
        view=ajax_package_list,
        name="ajax_package_list",
    ),
    re_path(
        r"^usage/(?P<slug>[-\w]+)/(?P<action>add|remove)/$",
        view=usage,
        name="usage",
    ),
    path(
        "<slug:slug>/document/",
        view=edit_documentation,
        name="edit_documentation",
    ),
    path("github-webhook/", view=github_webhook, name="github_webhook"),
]
