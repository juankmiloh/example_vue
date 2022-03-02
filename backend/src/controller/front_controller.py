from flask import render_template, request
from src.controller import controller
from src.util.constants import API_ROOT_PATH 


@controller.route('', methods=['GET'], defaults={'path': ''})
def home(path):
    script_root  = request.script_root
    
    if script_root :
        script_root += "/"

    return render_template("dist/index.html", url_base=script_root + "front/dist" )
