from flask import Flask, render_template, redirect, url_for , request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
import os
from instaloader.instaloader import Instaloader
from instaloader.structures import Post ,Profile
import os
import json
import pandas as pd
