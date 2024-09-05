import os

from flask import current_app, render_template
from werkzeug.utils import secure_filename

from . import tdd_blueprint
from project import db
from project.tdd.forms import MemberForm
from project.tdd.models import Member
from project.tdd.tasks import generate_avatar_thumbnail   # new


@tdd_blueprint.route('/member_signup/', methods=('GET', 'POST'))
def member_signup():
    form = MemberForm()
    if form.validate_on_submit():
        f = form.avatar.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            current_app.config['UPLOADS_DEFAULT_DEST'],
            filename
        ))

        try:
            member = Member(
                username=form.username.data,
                email=form.email.data,
                avatar=filename,
            )
            db.session.add(member)
            db.session.commit()
            member_id = member.id
        except Exception as e:
            db.session.rollback()
            raise

        generate_avatar_thumbnail.delay(member_id)            # new
        return 'Sign up successful'

    return render_template('member_signup.html', form=form)
