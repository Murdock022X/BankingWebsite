from flask import flash, current_app

def flash_codes(flash_code, flash_offset, app=current_app):
    with app.app_context():
        flash_code = str(int(flash_code) + flash_offset)
        flash_code_map = current_app.config["FLASH_CODES"]
        flash(flash_code_map[flash_code][0], category=flash_code_map[flash_code][1])
