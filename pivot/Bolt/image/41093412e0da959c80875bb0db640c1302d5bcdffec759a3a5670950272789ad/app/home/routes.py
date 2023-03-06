# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import Flask, render_template, render_template_string, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager, db
from jinja2 import TemplateNotFound
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__, static_folder="static")
app.config.from_object('config.Config')
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
mail = Mail(app)

@blueprint.route('/index')
@login_required
def index():

    return render_template('index.html', segment='index.html')

@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request
def get_segment( request ):
    try:
        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment
    except:
        return None

@blueprint.route("/example-profile", methods=['GET', 'POST'])
@login_required
def profile():
    """Profiles"""
    if request.method == 'GET':
        return render_template('example-profile.html', user=user,current_user=current_user)
    else:
        """Experimental Feature"""
        cur_user = current_user
        user = current_user.username
        name = request.form['name']
        experience = request.form['experience']
        skills = request.form['skills']
        msg = Message(
                recipients=[f'{cur_user.email}'],
                sender = 'support@example.com',
                reply_to = 'support@example.com',
                subject = "Please confirm your profile changes"
            )
        try:
            cur_user.profile_update = name
        except:
            return render_template('page-500.html')
        db.session.add(current_user)
        db.session.commit()
        token = ts.dumps(user, salt='changes-confirm-key')
        confirm_url = url_for('home_blueprint.confirm_changes',token=token,_external=True)
        html = render_template('emails/confirm-changes.html',confirm_url=confirm_url)
        msg.html = html
        mail.send(msg)
        return render_template('index.html')

@blueprint.route('/confirm/changes/<token>')
def confirm_changes(token):
    """Confirmation Token"""
    try:
        email = ts.loads(token, salt="changes-confirm-key", max_age=86400)
    except:
        abort(404)
    user = User.query.filter_by(username=email).first_or_404()
    name = user.profile_update
    template = open('templates/emails/update-name.html', 'r').read()
    msg = Message(
            recipients=[f'{user.email}'],
            sender = 'support@example.com',
            reply_to = 'support@example.com',
            subject = "Your profile changes have been confirmed."
        )
    msg.html = render_template_string(template % name)
    mail.send(msg)

    return render_template('index.html')
