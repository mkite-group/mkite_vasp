from mkite_core.recipes.pipes import SaveResultsPipe

from mkite_vasp import VaspOptions, VaspSettings
from mkite_vasp.recipes import VaspRecipe, VaspChain, UpdateStructurePipe
from mkite_vasp.parsers import VaspParser
from mkite_vasp.runners import CustodianRunner

from .static import StaticPBEVaspRecipe


class RelaxPBEVaspOptions(VaspOptions):
    INCAR: dict = {
        "IBRION": 2,
        "ISIF": 3,
        "NSW": 99,
        "GGA": "PE",
    }


class RelaxPBEVaspRecipe(VaspRecipe):
    OPTIONS_CLS = RelaxPBEVaspOptions


class RelaxPBEVaspChain(VaspChain):
    JOBS = [
        RelaxPBEVaspRecipe,
        SaveResultsPipe,
    ]
