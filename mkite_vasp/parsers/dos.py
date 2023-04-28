from .base import VaspParser


ORBITAL_INDICES = {
    "s": [0],
    "p": [1, 2, 3],
    "d": [4, 5, 6, 7, 8],
}


class VaspDosParser(VaspParser):
    def get_calcnodes(self):
        return [self.get_energy_calc(), self.get_dos_calc()]

    def get_dos_calc(self):
        dos = {
            "@module": "mkite.orm.calcs.models",
            "@class": "ProjectedDOS",
        }
        dos["efermi"] = float(self.vasprun.efermi)

        tdos = self.vasprun.tdos
        dos["bandgap"] = float(tdos.get_gap())
        dos["cbm"], dos["vbm"] = tdos.get_cbm_vbm()
        dos["cbm"], dos["vbm"] = float(dos["cbm"]), float(dos["vbm"])
        dos["emin"] = float(tdos.energies.min())
        dos["emax"] = float(tdos.energies.max())
        dos["npoints"] = len(tdos.energies)
        dos["tdos"] = self.get_tdos()
        dos["pdos"] = self.get_pdos()
        return dos

    def get_tdos(self):
        return self.vasprun.tdos.as_dict()["densities"]

    def get_pdos(self):
        pdos = self.vasprun.complete_dos.as_dict()["pdos"]
        return self.sparsify_pdos(pdos)

    def sparsify_pdos(self, pdos):
        """Removes projected DOS that have zero contributions. This is useful when
        the atom does not have d orbitals, since we'll save more than half of
        the memory required for the site DOS.
        """

        dos = []
        for site_dos in pdos:
            new_site_dos = {}
            for orbital, orb_dos in site_dos.items():
                new_orb_dos = {}
                for spin, spin_dos in orb_dos["densities"].items():
                    if sum(spin_dos) == 0:
                        new_orb_dos[spin] = None
                    else:
                        new_orb_dos[spin] = [float(d) for d in spin_dos]

                new_site_dos[orbital] = new_orb_dos
            dos.append(new_site_dos)

        return dos
