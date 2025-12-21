from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DecimalField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=128)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    university = StringField("University", validators=[Length(max=200)])
    country = StringField("Country", validators=[Length(max=120)])
    city = StringField("City", validators=[Length(max=120)])
    submit = SubmitField("Create account")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class ProductForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Description")
    price = DecimalField("Price (USD)", validators=[DataRequired(), NumberRange(min=0)], places=2)
    condition = SelectField("Condition", choices=[("New","New"), ("Like New","Like New"), ("Used","Used")])
    city = StringField("City", validators=[Length(max=120)])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    image_url = StringField("Image URL (optional)", validators=[Length(max=500)])
    submit = SubmitField("Save")

class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=250)])
    tags = StringField("Tags (comma separated)", validators=[Length(max=250)])
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Publish")

class CategoryForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=120)])
    type = SelectField("Type", choices=[("product","product"), ("info","info")], validators=[DataRequired()])
    submit = SubmitField("Add")

class MessageForm(FlaskForm):
    text = TextAreaField("Message", validators=[DataRequired(), Length(min=1, max=2000)])
    submit = SubmitField("Send")

class QtyForm(FlaskForm):
    qty = IntegerField("Qty", validators=[DataRequired(), NumberRange(min=1, max=99)])
    submit = SubmitField("Update")
