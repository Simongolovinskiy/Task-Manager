import uuid
import os
from flask import current_app
from flask_login import current_user
from PIL import Image


def save_report_task(report):
    token = str(uuid.uuid4())
    name, extension = os.path.splitext(report)
    report_fn = token + extension
    full_path = os.path.join(current_app.root_path, 'static', 'reports',
                             current_user.username, f'{current_user.username} report')

    if not os.path.exists(full_path):
        os.mkdir(full_path)

    rep_path = os.path.join(full_path, report_fn)
    size = (500, 500)
    file_rep = Image.open(report)
    file_rep.thumbnail(size)
    file_rep.save(rep_path)
    return report_fn

