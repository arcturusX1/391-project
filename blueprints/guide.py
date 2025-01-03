from flask import render_template, Blueprint, redirect
from model.model import Guide

guide_bp = Blueprint('guide_bp', __name__)

@guide_bp.route('/guides', methods=['GET', 'POST'])
def guides():
    guides = Guide.query.all()
    return render_template('guides.html', guides=guides)