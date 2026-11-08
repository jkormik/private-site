from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    """
    Form for Admin Login.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BlogPostForm(FlaskForm):
    """
    Form for creating and editing blog posts.
    Implements server-side validation for titles and content.
    """
    title = StringField('Title', validators=[
        DataRequired(), 
        Length(min=3, max=200, message="Title must be between 3 and 200 characters.")
    ])
    slug = StringField('Slug (Optional)')
    content = TextAreaField('Content', validators=[
        DataRequired(), 
        Length(min=10, message="Content is too short.")
    ])
    tag = StringField('Тег (например: ИИ-Агенты)')
    is_published = BooleanField('Publish Immediately')
    submit = SubmitField('Save Post')
