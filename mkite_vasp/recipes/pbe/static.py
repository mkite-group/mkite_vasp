from mkite_core.recipes.pipes import SaveResultsPipe

from mkite_vasp import VaspOptions, VaspSettings
from mkite_vasp.parsers import VaspParser
from mkite_vasp.recipes import VaspRecipe, VaspChain
from mkite_vasp.runners import CustodianRunner


class StaticPBEVaspOptions(VaspOptions):
    INCAR: dict = {
        "IBRION": -1,
        "NSW": 0,
        "GGA": "PE",
    }


class StaticPBEVaspRecipe(VaspRecipe):
    OPTIONS_CLS = StaticPBEVaspOptions
    PARSER_CLS = VaspParser
    RUNNER_CLS = CustodianRunner


class StaticPBEVaspChain(VaspChain):
    JOBS = [
        StaticPBEVaspRecipe,
        SaveResultsPipe,
    ]
