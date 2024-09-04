import os

from mkite_core.models import ConformerInfo
from mkite_core.models import CrystalInfo
from mkite_core.recipes import BaseRecipe
from mkite_core.recipes import RecipeChain
from mkite_core.recipes import RecipeError
from mkite_vasp.parsers import VaspParser
from mkite_vasp.runners import CustodianRunner
from mkite_vasp.settings import VaspOptions
from mkite_vasp.settings import VaspSettings
from pymatgen.core import Molecule
from pymatgen.core import Structure
from pymatgen.io.vasp.sets import DictSet

from .errors import VaspErrorHandler


class VaspRecipe(BaseRecipe):
    _PACKAGE_NAME = "VASP"
    _METHOD = "DFT"

    SETTINGS_CLS = VaspSettings
    OPTIONS_CLS = VaspOptions
    PARSER_CLS = VaspParser
    RUNNER_CLS = CustodianRunner
    ERROR_CLS = VaspErrorHandler

    def setup(self, workdir):
        vasp_input = DictSet(
            structure=self.get_inputs(),
            config_dict=self.get_options(),
        )

        if not os.path.exists(workdir):
            os.mkdir(workdir)

        vasp_input.write_input(workdir)

    def get_options(self) -> VaspOptions:
        """Builds an options dictionary for VASP"""
        options = self.settings.VASP_DEFAULT_OPTIONS
        options = VaspOptions.dict_update(options, self.OPTIONS_CLS().model_dump())
        options = VaspOptions.dict_update(options, self.info.options)
        return options

    def get_inputs(self) -> Structure:
        inp = super().get_inputs()[0]

        if "@class" not in inp:
            raise RecipeError(
                "Could not interpret input for current recipe. `@class` not in input"
            )

        if inp["@class"] == "Crystal":
            info = CrystalInfo.from_dict(inp)
            return info.as_pymatgen()

        if inp["@class"] == "Conformer":
            info = ConformerInfo.from_dict(inp)
            molecule = info.as_pymatgen()
            return self.get_structure_from_molecule(molecule)

        raise RecipeError(
            "input class not recognized. This input likely cannot be simulated using this recipe."
        )

    def get_structure_from_molecule(
        self, molecule: Molecule, vacuum_size=15
    ) -> Structure:
        box = molecule.cart_coords.max(0) - molecule.cart_coords.min(0) + vacuum_size

        return molecule.get_boxed_structure(*box, no_cross=True)


class VaspChain(RecipeChain):
    _PACKAGE_NAME = "VASP"
    _METHOD = "DFT"
