from mkite_vasp import VaspOptions, VaspSettings
from mkite_vasp.parsers import VaspParser
from mkite_vasp.recipes import VaspRecipe
from mkite_vasp.runners import CustodianRunner


class StaticPBEVaspOptions(VaspOptions):
    INCAR = {
        "IBRION": -1,
        "NSW": 0,
        "GGA": "PE",
    }


class StaticPBEVaspRecipe(VaspRecipe):
    OPTIONS_CLS = StaticPBEVaspOptions
    PARSER_CLS = VaspParser
    RUNNER_CLS = CustodianRunner
