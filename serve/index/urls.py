from .views import *

index.add_url_rule('/', view_func=RootView.as_view('root'))
index.add_url_rule('/index', view_func=IndexView.as_view('index'))
index.add_url_rule('/login', view_func=LoginView.as_view('login'))
index.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))
index.add_url_rule('/single', view_func=ExecSingleView.as_view('single'))
index.add_url_rule('/range', view_func=ExecRangeView.as_view('range'))
index.add_url_rule('/register', view_func=RegisterView.as_view('register'))

