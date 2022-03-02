from flask_sqlalchemy import SQLAlchemy
from injector import Module, singleton

from .electric_power.agent_repository import AgentRepository
from .electric_power.fpp_repository import FPPRepository
from .electric_power.grip_repository import GRIPRepository
from .electric_power.icoef_repository import ICOEFRepository
from .electric_power.ihh_repository import IHHRepository
from .electric_power.pivotal_index_repository import PivotalIndexRepository
from .electric_power.pme140_repository import PME140Repository
from .electric_power.preofe_repository import PreofeRepository
from .electric_power.trsd_repository import TRSDRepository
from .fuel_gas.contrat_repository import ContratRepository
from .fuel_gas.daggi_repository import DaggiRepository
from .fuel_gas.dp_repository import DPRepository
from .fuel_gas.iag_repository import IAGRepository
from .electric_power.iar_repository import IARRepository
from .fuel_gas.inventory_repository import InventoryRepository
from .fuel_gas.offert_repository import OffertRepository
from .fuel_gas.rc_repository import RCRepository
from .fuel_gas.sector_repository import SectorRepository
from .fuel_gas.source_repository import SourceRepository
from .indicator_dates_repository import IndicatorDateRepository
from .fuel_gas.contract_network_repository import ContractNetworkRepository


class RepositoryModule(Module):
    def __init__(self, db):
        self.db = db

    def configure(self, binder):
        agent_repository = AgentRepository(self.db)
        contrat_repository = ContratRepository(self.db)
        daggi_repository = DaggiRepository(self.db)
        dp_repository = DPRepository(self.db)
        fpp_repository = FPPRepository(self.db)
        grip_repository = GRIPRepository(self.db)
        iag_repository = IAGRepository(self.db)
        iar_repository = IARRepository(self.db)
        icoef_repository = ICOEFRepository(self.db)
        ihh_repository = IHHRepository(self.db)
        indicator_date_repository = IndicatorDateRepository(self.db)
        inventory_repository = InventoryRepository(self.db)
        offert_repository = OffertRepository(self.db)
        pivotal_index_repository = PivotalIndexRepository(self.db)
        pme140_repository = PME140Repository(self.db)
        preofe_repository = PreofeRepository(self.db)
        rc_repository = RCRepository(self.db)
        sector_repository = SectorRepository(self.db)
        source_repository = SourceRepository(self.db)
        trsd_repository = TRSDRepository(self.db)
        contract_network_repository = ContractNetworkRepository(self.db)

        binder.bind(AgentRepository, to=agent_repository, scope=singleton)
        binder.bind(ContratRepository, to=contrat_repository, scope=singleton)
        binder.bind(DPRepository, to=dp_repository, scope=singleton)
        binder.bind(DaggiRepository, to=daggi_repository, scope=singleton)
        binder.bind(FPPRepository, to=fpp_repository, scope=singleton)
        binder.bind(GRIPRepository, to=grip_repository, scope=singleton)
        binder.bind(IAGRepository, to=iag_repository, scope=singleton)
        binder.bind(IARRepository, to=iar_repository, scope=singleton)
        binder.bind(ICOEFRepository, to=icoef_repository, scope=singleton)
        binder.bind(IHHRepository, to=ihh_repository, scope=singleton)
        binder.bind(
            IndicatorDateRepository, to=indicator_date_repository, scope=singleton
        )
        binder.bind(InventoryRepository, to=inventory_repository, scope=singleton)
        binder.bind(OffertRepository, to=offert_repository, scope=singleton)
        binder.bind(PME140Repository, to=pme140_repository, scope=singleton)
        binder.bind(
            PivotalIndexRepository, to=pivotal_index_repository, scope=singleton
        )
        binder.bind(PreofeRepository, to=preofe_repository, scope=singleton)
        binder.bind(RCRepository, to=rc_repository, scope=singleton)
        binder.bind(SectorRepository, to=sector_repository, scope=singleton)
        binder.bind(SourceRepository, to=source_repository, scope=singleton)
        binder.bind(TRSDRepository, to=trsd_repository, scope=singleton)
        binder.bind(ContractNetworkRepository, to=contract_network_repository, scope=singleton)
