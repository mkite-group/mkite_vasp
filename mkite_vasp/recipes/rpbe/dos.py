from mkite_core.recipes.pipes import SaveResultsPipe, CopyWorkdirPipe

from mkite_vasp import VaspOptions
from mkite_vasp.recipes import VaspRecipe, VaspChain
from mkite_vasp.parsers.dos import VaspDosParser

from .static import StaticRPBEVaspRecipe


class DosRPBEVaspOptions(VaspOptions):
    INCAR: dict = {
        "IBRION": -1,
        "NSW": 0,
        "GGA": "RP",
        "NEDOS": 4000,
        "EMIN": -15,
        "EMAX": 25,
        "LORBIT": 11,
        "ALGO": "Normal",
        "LCHARG": True,
        "ICHARG": 1,
    }

    KPOINTS: dict = {
        "reciprocal_density": 64 * 3
    }


class DosRPBEVaspRecipe(VaspRecipe):
    OPTIONS_CLS = DosRPBEVaspOptions
    PARSER_CLS = VaspDosParser


class DosRPBEVaspChain(VaspChain):
    JOBS = [
        StaticRPBEVaspRecipe,
        CopyWorkdirPipe,
        DosRPBEVaspRecipe,
        SaveResultsPipe,
    ]
