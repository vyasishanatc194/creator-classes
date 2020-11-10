from .auth import SignUpApiView, LoginAPIView, LogoutAPIView, FacebookLogin, TwitterLogin, GoogleLogin
from .review import CreatorReviewAPIView, ClassReviewAPIView
from .favourites import FavouriteClassAPIView, FavouriteCreatorAPIView
from .user_class import ClassFilterAPIView, ClassSearchAPIView