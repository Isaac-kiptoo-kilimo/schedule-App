from django.urls import path

from app import views
from app.views import AnnouncementViewSet, ModuleViewSet, SessionViewSet,CommentViewSet,AnnouncementCommentViewSet, like_comment

from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Schedule API",
        default_version="v1",
        description="Test description",
        #   terms_of_service="https://www.google.com/policies/terms/",
        #   contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


router = DefaultRouter()

router.register(r"modules", ModuleViewSet, basename="Module")
router.register(r"announcements", AnnouncementViewSet, basename="Announcement")
router.register(r"sessions",SessionViewSet,basename="session")
router.register(r'comments',CommentViewSet,basename="comment")
router.register(r'announ-comments',AnnouncementCommentViewSet,basename="announ_commment")


urlpatterns = [
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    
   path("api/like/comment/<int:comment_id>/",views.like_comment,name="likes"),
    # announcements comments likes
    path("api/like/announcement/comment/<int:announcomment_id>/",views.like_announ_comment,name="announ-likes"),

    # announcements
    path("api/announcements/", views.all_announcements, name=""),
    # sessions
    path("api/sessions/detail/", views.get_session_details, name=""),
    path("api/sessions/search/", views.get_available_session, name=""),
    # Create user api
    path("api/user/create/", views.UserCreateAPIView.as_view(), name=""),
    path("api/user/login/", views.LoginAPIView.as_view(), name=""),
    path("api/user/logout/", views.LogoutAPIView.as_view(), name=""),
    path('change_password/<int:pk>/', views.ChangePasswordView.as_view(), name='auth_change_password'),
    # Get profile
    path("api/student/profile" ,views.StudentProfileAPIview.as_view(),name="student_profile"),
    # update student profile
    path("api/student/<int:pk>/update/profile/", views.StudentProfileUpdateAPIview.as_view(), name="student_update_profile"),
    

] + router.urls
