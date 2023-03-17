from flask import flash, current_app
from inspect import stack

def flash_codes(flash_code='0', app=current_app, caller=""):
    """Get the calling function from the call stack, this is used to map 
    into the flash code table, then use the flash code from the function 
    to flash correct message. See flash_codes.json for flash code 
    definitions.

    Args:
        flash_code (str, optional): The code given from the function that tells
        us which message to flash. Defaults to '0'.
        app (Flask, optional): The Flask object currently in use. 
        Defaults to current_app.
        caller (str, optional): The calling function, should usually be left 
        blank and gotten from the stack. Defaults to "".
    """    

    # If we don't provide a caller get the the function from the stack.
    if not caller:
        caller = stack()[1][3]

    # In the apps context, map into the config to get the flash codes mapping. 
    # Then map into the flash code mapping using the caller function and then 
    # the flash code.
    with app.app_context():
        flash_code_map = current_app.config["FLASH_CODES"]

        flash(flash_code_map[caller][flash_code][0], 
              category=flash_code_map[caller][flash_code][1])
