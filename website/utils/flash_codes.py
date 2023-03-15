from flask import flash, current_app
from inspect import stack

def flash_codes(flash_code='0', app=current_app, caller=""):
    if not caller:
        caller = stack()[1][3]

    with app.app_context():
        flash_code_map = current_app.config["FLASH_CODES"]

        flash(flash_code_map[caller][flash_code][0], 
              category=flash_code_map[caller][flash_code][1])
