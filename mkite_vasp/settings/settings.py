from typing import Any
from pydantic import Field
from mkite_core.external import load_config
from pkg_resources import resource_filename

from mkite_core.recipes import EnvSettings, BaseOptions


VASP_DEFAULT_OPTIONS = load_config(resource_filename("mkite_vasp.settings", "DefaultOptions.yaml"))


class VaspOptions(BaseOptions):
    INCAR: dict = {}
    KPOINTS: dict = {}
    POTCAR: dict = {}
    POTCAR_FUNCTIONAL: str = "PBE_54"

    @classmethod
    def get_defaults(cls):
        return cls(**VASP_DEFAULT_OPTIONS)


class VaspSettings(EnvSettings):
    VASP_DEFAULT_OPTIONS: Any = Field(
        default_factory=VaspOptions.get_defaults,
        description="File where to load the default calculation details\
            for VASP",
    )
    VASP_STD: str = Field("vasp_std", description="Command to run VASP (std)")
    VASP_GAM: str = Field("vasp_gam", description="Command to run VASP (gam)")
    VASP_NCL: str = Field("vasp_ncl", description="Command to run VASP (ncl)")
