from __future__ import annotations
from flask import Blueprint, render_template, request, current_app, redirect, url_for, flash
from werkzeug.utils import secure_filename
from . import db
from .models import Destination, Image
import os

bp = Blueprint('admin', __name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def admin_index():
    places = Destination.query.order_by(Destination.created_at.desc()).all()
    return render_template('admin/index.html', places=places)

@bp.route('/destinations/new', methods=['GET', 'POST'])
def create_destination():
    from .forms import DestinationForm
    form = DestinationForm()
    if form.validate_on_submit():
        dest = Destination(
            name=form.name.data.strip(),
            location=form.location.data.strip(),
            description=form.description.data.strip(),
            category=form.category.data,
            has_wifi=bool(form.has_wifi.data),
            allows_screens=bool(form.allows_screens.data),
        )
        db.session.add(dest)
        db.session.commit()
        flash('Destination created', 'success')
        return redirect(url_for('admin.admin_index'))
    return render_template('admin/create_destination.html', form=form)

@bp.route('/destinations/<int:destination_id>/upload', methods=['GET', 'POST'])
def upload_image(destination_id: int):
    from .forms import ImageUploadForm
    dest = Destination.query.get_or_404(destination_id)
    form = ImageUploadForm()
    if form.validate_on_submit():
        file = form.image.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(save_path):
                filename = f"{base}_{counter}{ext}"
                save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                counter += 1
            file.save(save_path)

            img = Image(
                destination_id=dest.id,
                filename=filename,
                caption=form.caption.data.strip() if form.caption.data else None,
                is_primary=bool(form.is_primary.data),
            )
            if img.is_primary:
                for other in dest.images:
                    if other.is_primary:
                        other.is_primary = False
            db.session.add(img)
            db.session.commit()
            flash('Image uploaded', 'success')
            return redirect(url_for('admin.admin_index'))
        flash('Invalid file type', 'danger')
    return render_template('admin/upload_image.html', form=form, dest=dest)
