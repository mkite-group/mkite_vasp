from custodian.custodian import Custodian
from custodian.vasp.jobs import VaspJob
from custodian.vasp.handlers import (
    VaspErrorHandler,
    StdErrHandler,
    UnconvergedErrorHandler,
    IncorrectSmearingHandler,
    WalltimeHandler,
)
from mkite_core.recipes.runner import BaseRunner


class CustodianRunner(BaseRunner):
    @property
    def cmd(self):
        return str(self.settings.VASP_STD).split(" ")

    def create_jobs(self):
        return [VaspJob(
            vasp_cmd=self.cmd,
            gamma_vasp_cmd=self.settings.VASP_GAM,
        )]

    def run(self):
        handlers = [
            VaspErrorHandler(),
            UnconvergedErrorHandler(),
            StdErrHandler(),
            WalltimeHandler(),
            IncorrectSmearingHandler(),
        ]
        jobs = self.create_jobs()
        c = Custodian(handlers, jobs, max_errors=5)
        c.run()
