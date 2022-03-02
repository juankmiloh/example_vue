
import json
import datetime
from flask import request

from src.controller import controller
from src.service import StockPriceService
from src.repository import TRSDRepository
from src.repository import PME140Repository
from src.util.constants import API_ROOT_PATH 
from src.util.web_util import to_date
from src.util.private_decorator import  privateDecorator

@controller.route(API_ROOT_PATH + 'pb', methods=['GET'])
def stock_price_indicator(stock_price_service: StockPriceService, trsd_repository: TRSDRepository):

    years = request.args.getlist('years[]', type = int)
    result = stock_price_service.get_prices(years, trsd_repository)
    return json.dumps(result)

@controller.route(API_ROOT_PATH + 'pme140', methods=['GET'])
def stock_price_reference(stock_price_service: StockPriceService, pme140_repository: PME140Repository):
    
    year = request.args.get('year', default = datetime.date.today().year, type = int)
    result = stock_price_service.get_references(year, pme140_repository)
    return json.dumps(result)
