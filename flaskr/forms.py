from wtforms.form import Form
from wtforms.fields import (StringField, PasswordField, 
                            SubmitField, SelectField, IntegerField, 
                            TextAreaField, HiddenField
)
from wtforms.validators import DataRequired, EqualTo
from wtforms import ValidationError

from flaskr.models import User, Horse


class RegisteForm(Form):
    userid = StringField('ユーザーID：', validators=[DataRequired()])
    password = PasswordField(
        'パスワード：',
        validators=[DataRequired(), EqualTo('password_confirm', message='パスワードが一致しません')])
    password_confirm = PasswordField('パスワード再入力:', validators=[DataRequired()])
    submit = SubmitField('登録')
    
    def validate_password(self, field):
        if len(field.data) < 8:
            raise ValidationError('パスワードは8文字以上です')
        
    def validate_userid(self, field):
        if User.select_by_userid(field.data):
            raise ValidationError('このIDは登録できません。')
        
                
class LoginForm(Form):
    userid = StringField('ユーザID：', validators=[DataRequired()])
    password = PasswordField('パスワード：', validators=[DataRequired()])
    submit = SubmitField('ログイン')
    
    
class HorseRegist(Form):
    horsename = StringField('馬名：', validators=[DataRequired()])
    comment = TextAreaField('コメント：')
    submit = SubmitField('登録')
    
    def validate_comment(self, field):
        if len(field.data) > 1000:
            raise ValidationError('コメントは1000文字以内です')
        
        
class ForgetPassword(Form):
    userid = StringField('ユーザーID：', validators=[DataRequired()])
    last_password = StringField('以前のパスワード：', validators=[DataRequired()])
    new_password = PasswordField(
        'パスワード：',
        validators=[DataRequired(), EqualTo('new_password_confirm', message='パスワードが一致しません')])
    new_password_confirm = PasswordField('パスワード再入力:', validators=[DataRequired()])
    submit = SubmitField('登録')
    
    def validate_password(self, field):
        if len(field.data) < 8:
            raise ValidationError('パスワードは8文字以上です')
        
    def validate_userid(self, field):
        if not User.select_by_userid(field.data):
            raise ValidationError('このIDは存在しません。')
    
     
class HorseDeleteForm(Form):
    id = HiddenField()
    submit = SubmitField('削除')
    
class HorseUpdateForm(Form):
    
    id = HiddenField()
    userid = HiddenField()
    horsename = StringField('馬名：')
    comment = TextAreaField('コメント：')
    submit = SubmitField('変更')
    
    def validate_comment(self, field):
        if len(field.data) > 1000:
            raise ValidationError('コメントは1000文字以内です')