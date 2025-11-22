from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path(
        "dashboard/",
        TemplateView.as_view(template_name="dashboard.html"),
        name="dashboard",
    ),
    path("users/", include("users.urls")),
    path("assessments/", include("assessments.urls")),
]

# Only include these URLs if the apps exist
try:
    import recommendations

    urlpatterns.append(path("recommendations/", include("recommendations.urls")))
except ImportError:
    pass

try:
    import jobs

    urlpatterns.append(path("jobs/", include("jobs.urls")))
except ImportError:
    pass

try:
    import learning

    urlpatterns.append(path("learning/", include("learning.urls")))
except ImportError:
    pass

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
