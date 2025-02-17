"""
docstring
"""

import numpy as np


def roundify_geometry(output_string):
    """ Finds the smallest geometry (by volume) from a list of 
        conformer geometries
        :param str output_string: string for a conformer
                                  trajectory file
        :r
    """

    # Get lines for the output string
    lines = output_string.splitlines()

    # Get the number of atoms
    natom = int(lines[0])

    # loop over the lines to find the smallest geometry
    rrminmax = 1.0e10
    ngeom = 0
    small_geo_idx = 0
    while ngeom*(natom+2) < len(lines):
        rrmax = 0.0
        for i in range(natom):
            for j in range(i+1, natom):
                # Get the line
                xyz1 = lines[i+ngeom*(natom+2)+2].split()[1:]
                xyz2 = lines[j+ngeom*(natom+2)+2].split()[1:]
                # Get the coordinates
                atom1 = [float(val) for val in xyz1]
                atom2 = [float(val) for val in xyz2]
                # Calculate the interatomic distance
                rrtest = np.sqrt((atom1[0]-atom2[0])**2 +
                                 (atom1[1]-atom2[1])**2 +
                                 (atom1[2]-atom2[2])**2)
                # Check and see if distance is more than max
                if rrtest > rrmax:
                    rrmax = rrtest
        # If max below moving threshold, set to smallest geom
        if rrmax < rrminmax:
            rrminmax = rrmax
            small_geo_idx = ngeom
        ngeom += 1

    # Set the output geometry
    geom_str = '{}\n'.format(natom)
    for i in range(natom):
        geom_str += lines[i+small_geo_idx*(natom+2)+2] + '\n'

    return geom_str


if __name__ == '__main__':
    with open('obabel-confs.xyz', 'r') as f:
        OUTPUT_STR = f.read()
    print(roundify_geometry(OUTPUT_STR))
