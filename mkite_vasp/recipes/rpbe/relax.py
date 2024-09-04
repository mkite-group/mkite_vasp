from mkite_core.recipes.pipes import SaveResultsPipe

from mkite_vasp import VaspOptions
from mkite_vasp.recipes import VaspRecipe, VaspChain, UpdateStructurePipe

from .static import StaticRPBEVaspRecipe


class RelaxRPBEVaspOptions(VaspOptions):
    INCAR: dict = {
        "IBRION": 2,
        "ISIF": 3,
        "NSW": 99,
        "GGA": "RP",
    }


class RelaxRPBEVaspRecipe(VaspRecipe):
    OPTIONS_CLS = RelaxRPBEVaspOptions


class RelaxRPBEVaspChain(VaspChain):
    JOBS = [
        RelaxRPBEVaspRecipe,
        SaveResultsPipe,
    ]
