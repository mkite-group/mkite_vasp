from mkite_vasp import VaspOptions, VaspSettings
from mkite_vasp.parsers import VaspParser
from mkite_vasp.recipes import VaspRecipe
from mkite_vasp.runners import CustodianRunner


class StaticRPBEVaspOptions(VaspOptions):
    INCAR = {
        "IBRION": -1,
        "NSW": 0,
        "GGA": "RP",
        "LCHARG": True,
    }


class StaticRPBEVaspRecipe(VaspRecipe):
    OPTIONS_CLS = StaticRPBEVaspOptions
    PARSER_CLS = VaspParser
    RUNNER_CLS = CustodianRunner
