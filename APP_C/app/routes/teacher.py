from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Cohort

teacher_bp = Blueprint('teacher', __name__, template_folder='../templates/teacher')

@teacher_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role.name!='teacher':
        return redirect(url_for('auth.login'))
    cohorts = Cohort.query.all()
    return render_template('dashboard.html', cohorts=cohorts)
