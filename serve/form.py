from flask_wtf import Form, FlaskForm
from wtforms import StringField, validators, PasswordField

class LoginFrom(FlaskForm):
    username = StringField(u'用户名',
                           [validators.Length(min=4, max=16, message=u'用户名长度在4-16位'), validators.DataRequired()],
                           render_kw={'placeholder': u'请输入用户名'})
    password = PasswordField(u'密码', [validators.length(min=8, max=16, message=u'密码长度8-16位'), validators.DataRequired()],
                             render_kw={'placeholder': u'请输入密码'})
class RegFrom(Form):
    username = StringField(u'注册用户名(请使用公司常用英文名)', [validators.Length(min=3, max=16, message=u'用户名长度在3-16位'),
                                      validators.DataRequired(message=u'请输入用户名')], render_kw={'placeholder': u'请输入用户名'})
    password = PasswordField(u'注册密码', [validators.length(min=5, max=16, message=u'密码长度5-16位'),
                                       validators.DataRequired(message=u'请输入密码')], render_kw={'placeholder': u'请输入密码'})
    se_password = PasswordField(u'再次输入密码', [validators.length(min=5, max=16, message=u'密码长度5-16位'),
                                            validators.DataRequired(message=u'请输入确认密码')],
                                render_kw={'placeholder': u'请输入密码'})
    key = StringField(u'输入邀请码', validators=[validators.DataRequired(message=u'请输入邀请码')],
                        render_kw={'placeholder': u'输入邀请码'})
