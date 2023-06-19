import uuid
import os

from PIL import Image
from flask import current_app
from flask_login import current_user
from werkzeug.utils import secure_filename


def save_report_task(report_form):
    if report_form is None:
        raise ValueError('Missing file.')
    token = str(uuid.uuid4())
    name, extension = os.path.splitext(secure_filename(report_form.filename))
    report_fn = token + extension
    full_path = os.path.join(current_app.root_path, 'static', 'reports', current_user.username, f'{current_user.username}_report')

    if not os.path.exists(full_path):
        os.makedirs(full_path)

    rep_path = os.path.join(full_path, report_fn)
    output_size = (500, 500)

    file_formats = {
            '.pdf': lambda r, p: r.save(p),
            '.jpg': lambda r, p: (lambda img, path: (img.thumbnail(output_size) or img.save(path)))(Image.open(r), p),
            '.jpeg': lambda r, p: (lambda img, path: (img.thumbnail(output_size) or img.save(path)))(Image.open(r), p),
            '.png': lambda r, p: (lambda img, path: (img.thumbnail(output_size) or img.save(path)))(Image.open(r), p),
            '.gif': lambda r, p: (lambda img, path: (img.thumbnail(output_size) or img.save(path)))(Image.open(r), p)
        }
    if extension.lower() in file_formats.keys():
        file_handler = file_formats.get(extension.lower())
        if file_handler:
            file_handler(report_form, rep_path)
            return rep_path
        else:
            raise NotImplemented('Something went wrong.')

    else:
        raise ValueError('Unsupported  file extension')


def register_user_avatar(avatar_form):
    if avatar_form is None:
        raise ValueError('Missing file.')

    token = str(uuid.uuid4())
    extension = os.path.splitext(secure_filename(avatar_form.filename))[1]
    pic_fn = token + extension
    full_path = os.path.join(current_app.root_path, 'static', 'avatars', current_user.username)

    if not os.path.exists(full_path):
        os.makedirs(full_path)

    pic_path = os.path.join(full_path, pic_fn)
    avatar_form.save(pic_path)

    return pic_fn


