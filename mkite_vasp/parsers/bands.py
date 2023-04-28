from .base import VaspParser


class VaspBandsParser(VaspParser):
    def get_pymatgen_bands(self, **kwargs):
        return self.vasprun.get_band_structure(**kwargs)

    def get_calcs(self):
        self.load_files()
        self.check_convergence()

        properties = self.get_properties()
        properties.bandstructure = self.get_band_structure()

        calc = Munch(
            theory=self.theory,
            meta_data=self.get_meta_data(),
            properties=properties,
        )
        return [calc]

    def get_bands(self):
        self.bs = self.get_pymatgen_bands()
        bsprops = {}
        # fix this later
        bsprops["kpath"] = self.job_details("bs_kpath")
        bsprops["symlabel"] = self.job_details("bs_kpath_labels")
        bsprops["symindex"] = self.job_details("bs_kpath_indices")
        bsprops["efermi"] = self.vasprun.efermi

        bsprops["bandgap"] = self.bs.get_band_gap()["energy"]
        bsprops["directgap"] = self.bs.get_band_gap()["direct"]
        bsprops["cbm"] = self.bs.get_cbm()["energy"]
        bsprops["vbm"] = self.bs.get_vbm()["energy"]

        bsprops.energies = self.get_energies()
        bsprops.projections = self.get_projections()

        return bsprops

    def get_energies(self):
        return {str(spin): band.tolist() for spin, band in self.bs.bands.items()}

    def get_projections(self):
        spin_proj = {str(spin): proj for spin, proj in self.bs.projections.items()}

        element_indices = {
            s: [i for i, sym in enumerate(self.bs.structure.species) if str(sym) == s]
            for s in self.bs.structure.symbol_set
        }

        # useful numbers to reshape the contribution matrices later
        nb, nk = self.bs.nb_bands, len(self.bs.kpoints)

        # initializing the dictionary that will contain the final results
        projections = {
            element: {
                orb: {spin: None for spin in spin_proj} for orb in ORBITALS_INDICES
            }
            for element in element_indices
        }
        for element, orbital, spin in product(
            element_indices, ORBITALS_INDICES, spin_proj
        ):
            # proj is a (bands, kpts, orbitals, atoms) tensor
            # containing the contributions of each one of them
            proj = spin_proj[spin]
            ei = element_indices[element]
            oi = ORBITALS_INDICES[orbital]

            # we select only the part corresponding to the given orbital/element
            # and sum the contributions
            subset = proj[:, :, oi, :][..., ei]
            p = subset.reshape(nb, nk, -1).sum(-1)

            if np.sum(p) > 0:
                projections[element][orbital][spin] = p.tolist()

        return projections
