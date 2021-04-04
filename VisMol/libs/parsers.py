#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  Copyright 2021 Carlos Eduardo Sequeiros Borja <carseq@amu.edu.pl>
#  

import VisMol.libs.objects as vmos

def parse_pdb(pdb_file):
    atoms = []
    with open(pdb_file, "r") as pdbin:
        for line in pdbin:
            if line.startswith("ATOM"):
                atom_id = int(line[6:11])
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                name = line[12:16].strip()
                atom = vmos.VMAtom(atom_id, x, y, z, name=name)
                atoms.append(atom)
    return vmos.GLContainer(atoms)
