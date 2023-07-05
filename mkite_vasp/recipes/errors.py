import os
from pymatgen.core import Structure
from mkite_engines.status import Status
from mkite_core.models import JobInfo, CrystalInfo
from mkite_core.recipes import BaseErrorHandler


class VaspErrorHandler(BaseErrorHandler):
    def handle(self) -> JobInfo:
        info = self.info.copy()
        if "relax" in info.recipe.get("name", ""):
            return self.handle_relax_errors(info)

    def handle_relax_errors(self, info: JobInfo):
        files = os.listdir(self.workdir)
        if "CONTCAR" in files:
            structure = Structure.from_file("CONTCAR")
            crystal = CrystalInfo.from_pymatgen(structure)
            info.inputs = [crystal.as_dict()]

        self.set_status(info, Status.READY.value)

        return info
