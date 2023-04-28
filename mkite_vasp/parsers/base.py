import os
import warnings
from datetime import timedelta
from pymatgen.io.vasp.inputs import Kpoints
from pymatgen.io.vasp.outputs import Vasprun, Outcar

from mkite_core.models import NodeResults, JobInfo, RunStatsInfo, JobResults, CrystalInfo
from mkite_core.recipes.parser import BaseParser


class VaspParser(BaseParser):
    def __init__(self, workdir: os.PathLike, **kwargs):
        super().__init__(workdir)
        self.vasprun = self.load_vasprun(**kwargs)
        self.outcar = self.load_outcar()

    def load_vasprun(self, filename="vasprun.xml", **kwargs):
        path = self.get_path(filename)
        return Vasprun(
            path,
            parse_potcar_file=False,
            **kwargs,
        )

    def load_outcar(self, filename="OUTCAR"):
        path = self.get_path(filename)
        return Outcar(path)

    def load_kpoints(self, filename="KPOINTS"):
        path = self.get_path(filename)
        return Kpoints(path)

    @property
    def is_converged(self):
        return self.vasprun.converged

    def get_energy(self):
        return self.vasprun.ionic_steps[-1]["e_wo_entrp"]

    def get_forces(self):
        return self.vasprun.ionic_steps[-1]["forces"]

    def get_structure(self):
        return self.vasprun.ionic_steps[-1]["structure"]

    def get_ionic_steps(self):
        return self.vasprun.ionic_steps

    def get_runstats(self):
        outstats = self.outcar.run_stats
        info = super().get_runstats()
        info["duration"] = outstats["Elapsed time (sec)"]

        if "ncores" not in info:
            info["ncores"] = outstats["cores"]

        if "ngpus" not in info:
            info["ngpus"] = 0

        info["pkgversion"] = self.vasprun.vasp_version

        return info

    def get_chemnode(self):
        crystal = CrystalInfo.from_pymatgen(self.get_structure())
        return crystal.as_dict()

    def get_calcnodes(self):
        return [self.get_energy_calc()]

    def get_energy_calc(self):
        # TODO: use calcs.io
        return {
            "@module": "mkite.orm.calcs.models",
            "@class": "EnergyForces",
            "energy": self.get_energy(),
            "forces": self.get_forces(),
        }

    def get_nodes(self):
        return [
            NodeResults(
                chemnode=self.get_chemnode(),
                calcnodes=self.get_calcnodes(),
            )
        ]

    def parse(self) -> JobResults:
        nodes = self.get_nodes()
        runstats = self.get_runstats()

        return JobResults(job={}, nodes=nodes, runstats=runstats)
