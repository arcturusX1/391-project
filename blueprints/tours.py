from flask import render_template, Blueprint, redirect, url_for
from model.model import Preset_Tour

tours_bp = Blueprint('tours_bp', __name__)

@tours_bp.route('/', methods=['GET', 'POST'])
def tours():
    tours = Preset_Tour.query.all()
    print([things for things in tours])
    return render_template('tours.html', tours=tours)

