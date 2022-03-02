from flask_sqlalchemy import SQLAlchemy
from injector import Module, singleton

from .agent_service import AgentService
from .contrat_service import ContratService
from .daggi_service import DaggiService
from .dp_service import DPService
from .fpp_service import FPPService
from .grip_service import GRIPService
from .iar_service import IARService
from .iag_service import IAGService
from .icoef_service import ICOEFService
from .ihh_service import IHHService
from .indicator_date_service import IndicatorDateService
from .injection_service import InjectionService
from .inventory_service import InventoryService
from .offert_service import OffertService
from .pivotal_index_service import PivotalIndexService
from .pivotal_service import PivotalService
from .preofe_service import PreofeService
from .rc_service import RCService
from .sector_service import SectorService
from .source_service import SourceService
from .stock_price_service import StockPriceService
from .trsd_service import TRSDService
from .contract_network_service import ContractNetworkService


class ServiceModule(Module):
    def configure(self, binder):
        agent_service = AgentService()
        contrat_service = ContratService()
        daggi_service = DaggiService()
        dp_service = DPService()
        fpp_service = FPPService()
        grip_service = GRIPService()
        iag_service = IAGService()
        iar_service = IARService()
        icoef_service = ICOEFService()
        ihh_service = IHHService()
        indicator_date_service = IndicatorDateService()
        injection_service = InjectionService()
        inventory_service = InventoryService()
        offert_service = OffertService()
        pivotal_index_service = PivotalIndexService()
        pivotal_service = PivotalService()
        preofe_service = PreofeService()
        rc_service = RCService()
        sector_service = SectorService()
        source_service = SourceService()
        stock_price_service = StockPriceService()
        trsd_service = TRSDService()
        contract_network_service = ContractNetworkService()

        binder.bind(AgentService, to=agent_service, scope=singleton)
        binder.bind(ContratService, to=contrat_service, scope=singleton)
        binder.bind(DPService, to=dp_service, scope=singleton)
        binder.bind(FPPService, to=fpp_service, scope=singleton)
        binder.bind(DaggiService, to=daggi_service, scope=singleton)
        binder.bind(GRIPService, to=grip_service, scope=singleton)
        binder.bind(IAGService, to=iag_service, scope=singleton)
        binder.bind(IARService, to=iar_service, scope=singleton)
        binder.bind(ICOEFService, to=icoef_service, scope=singleton)
        binder.bind(IHHService, to=ihh_service, scope=singleton)
        binder.bind(IndicatorDateService, to=indicator_date_service, scope=singleton)
        binder.bind(InjectionService, to=injection_service, scope=singleton)
        binder.bind(InventoryService, to=inventory_service, scope=singleton)
        binder.bind(OffertService, to=offert_service, scope=singleton)
        binder.bind(PivotalIndexService, to=pivotal_index_service, scope=singleton)
        binder.bind(PivotalService, to=pivotal_service, scope=singleton)
        binder.bind(PreofeService, to=preofe_service, scope=singleton)
        binder.bind(RCService, to=rc_service, scope=singleton)
        binder.bind(SectorService, to=sector_service, scope=singleton)
        binder.bind(SourceService, to=source_service, scope=singleton)
        binder.bind(StockPriceService, to=stock_price_service, scope=singleton)
        binder.bind(TRSDService, to=trsd_service, scope=singleton)
        binder.bind(ContractNetworkService, to=contract_network_service, scope=singleton)
        
