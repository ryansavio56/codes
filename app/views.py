from __future__ import annotations
from flask import Blueprint, render_template, request, current_app, send_from_directory
from .models import Destination

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    query = Destination.query.order_by(Destination.created_at.desc())
    category = request.args.get('category')
    if category:
        query = query.filter(Destination.category == category)
    places = query.all()
    return render_template('index.html', places=places, active_category=category)

@bp.route('/destination/<int:destination_id>')
def destination_detail(destination_id: int):
    dest = Destination.query.get_or_404(destination_id)
    return render_template('detail.html', dest=dest)

@bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

