from flask_wtf import Form, FlaskForm
from wtforms import StringField, validators, PasswordField

class LoginFrom(FlaskForm):
    username = StringField(u'用户名',
                           [validators.Length(min=4, max=16, message=u'用户名长度在4-16位'), validators.DataRequired()],
                           render_kw={'placeholder': u'请输入用户名'})
    password = PasswordField(u'密码', [validators.length(min=8, max=16, message=u'密码长度8-16位'), validators.DataRequired()],
                             render_kw={'placeholder': u'请输入密码'})
