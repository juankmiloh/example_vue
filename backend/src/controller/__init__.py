from flask import Blueprint
from flask_cors import CORS

controller = Blueprint("controller", __name__, url_prefix="/")

from src.controller.electric_power import (
    agent_controller,
    fpp_controller,
    grip_controller,
    iag_controller,
    iar_controller,
    icoef_controller,
    ihh_controller,
    pivotal_controller,
    pivotal_index_controller,
    preofe_controller,
    stock_price_controller,
    trsd_controller,
)
from src.controller.fuel_gas import (
    daggi_controller,
    dp_controller,
    gmp_controller,
    goc_controller,
    gog_controller,
    gpd_controller,
    injection_controller,
    inventory_controller,
    price_import_national_controller,
    rc_controller,
    source_controller,
    contract_network_controller,
)

from . import front_controller, indicators_dates_controller
