import os
from pymatgen.core import Structure
from mkite_core.models import JobInfo, CrystalInfo, Status
from mkite_core.recipes import BaseErrorHandler


class VaspErrorHandler(BaseErrorHandler):
    def handle(self) -> JobInfo:
        info = self.info.copy()
        if "relax" in info.recipe.get("name", ""):
            return self.handle_relax_errors(info)

    def handle_relax_errors(self, info: JobInfo):
        files = os.listdir(self.workdir)
        if "CONTCAR" in files:
            # we can restart the job by taking the relaxed
            # structure and re-adding it to the engine
            contcar = os.path.join(self.workdir, "CONTCAR")
            structure = Structure.from_file(contcar)
            crystal = CrystalInfo.from_pymatgen(structure)
            info.inputs = [crystal.as_dict()]

            # to continue the job, set status as ready
            self.set_status(info, "Y")

        else:
            self.set_status(info, "E")

        info.workdir = None
        return info
