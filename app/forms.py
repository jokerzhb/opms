from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, IntegerField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('确定')


class PublishForm(FlaskForm):
    package_id = IntegerField('编号', validators=[DataRequired()])
    package_name = StringField('包名')
    package_version = StringField('版本号', validators=[DataRequired(), Length(0, 16)])
    package_content = TextAreaField('更新内容', validators=[DataRequired(), Length(0, 512)])
    pack = FileField('Package')
    submit = SubmitField('提交')


class SetpwdForm(FlaskForm):
    old_passwd = PasswordField('旧新密码', validators=[DataRequired(), Length(1, 12)])
    new_passwd = PasswordField('新密码', validators=[DataRequired(), Length(1, 12)])
    new_passwd2 = PasswordField('确认密码', validators=[DataRequired(), Length(1, 12)])
    submit = SubmitField('确定')


class UseraddForm(FlaskForm):
    user_name = StringField('用户名', validators=[DataRequired(), Length(4, 12)])
    user_email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 12)])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('确定')


class UpgradeFrom(FlaskForm):
    title = StringField('标题', validators=[DataRequired('标题不能为空'), Length(1, 32)])
    content = CKEditorField('更新内容', validators=[DataRequired(), Length(0, 1024, '长度请控制在1024字符以内')])
    submit = SubmitField('确定')