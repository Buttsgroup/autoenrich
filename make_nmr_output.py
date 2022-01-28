
import pybel as pyb
import os

import glob
import copy

import sys
sys.path.append('INSERT_PATH_TO_MOL_TRANSLATOR_HERE')

from mol_translator.aemol import aemol
from mol_translator.properties.energy import energy_ops as eops
from mol_translator.properties.nmr.nmr_write import write_nmredata
from mol_translator.properties.nmr.nmr_ops import get_coupling_types, scale_chemical_shifts

files = glob.glob('NMR/*.log')
#files = glob.glob('nmredata_run1/*.sdf')

from tqdm import tqdm


amols = []
for file in tqdm(files):
	id = file.split('/')[-1].split('.')[0]
	try:
		outfile = 'OUTPUT/autoenrich_' + str(id) + '.nmredata.sdf'
		if os.path.isfile(outfile):
			continue

		amol = aemol(id)
		#amol.from_file(file, ftype='g09')
		amol.from_file_pyb(file, ftype='log')
		opt_file = f'OPT/{str(id)}.log'
		amol.prop_from_file(opt_file, 'g09', 'scf')

		assert amol.mol_properties['energy'] < 1000000, print(amol.mol_properties)

		amol.prop_from_file(file, 'g09', 'nmr')
		#amol.prop_fromfile(file, 'nmredata', 'nmr')

		amol.get_bonds()
		amol.get_path_lengths()
		get_coupling_types(amol)
		scale_chemical_shifts(amol)

		write_nmredata(outfile, amol)

		amols.append(amol)
	except:
		print('Bad file, ID', id)
		file = 'NMR/'+file
		with open('NMR_RESUB_ARRAY.txt', 'a') as f:
			print(file, file=f)

eops.calc_pops(amols)

with open('energies.txt', 'w') as f:
	string = "{0:<10s}\t{1:<10s}\t{2:<10s}".format("Molid", "Energy", "Pop")
	print(string, file=f)
for amol in amols:
	with open('energies.txt', 'a') as f:
		string = "{0:<10s}\t{1:<10f}\t{2:<10f}".format(amol.info['molid'], amol.mol_properties['energy'], amol.mol_properties['pop'])
		print(string, file=f)

boltz_atoms, boltz_pairs = eops.boltzmann_average(amols, pair_props=['coupling'], atom_props=['shift'])



newmol = copy.deepcopy(amols[0])
newmol.get_bonds()
newmol.get_path_lengths()
get_coupling_types(newmol)
newmol.atom_properties['shift'] = boltz_atoms['shift']
newmol.pair_properties['coupling'] = boltz_pairs['coupling']
outfile = 'OUTPUT/AE_AVERAGED.nmredata.sdf'
write_nmredata(outfile, newmol)
