
from openbabel import pybel as pyb

import glob


import sys
sys.path.append('INSERT_PATH_TO_MOL_TRANSLATOR_HERE')

from mol_translator.aemol import Aemol
from mol_translator.comp_chem.gaussian.gaussian_input import write_gaussian_com
from mol_translator.comp_chem.gaussian.gaussian_input import make_gaussian_rootline

files = glob.glob('INPUT/*')

for file in files:

	p = file.split('/')[-1].split('.')[0]
	ft = file.split('.')[-1]

	amol = Aemol(p)
	amol.from_file_ob(file, ftype=ft)

	prefs = {}
	prefs['calc_type']='optimisation'

	prefs['charge'] = 0
	prefs['multiplicity'] = 1
	
	prefs['software'] = 'g09'
	prefs['memory'] = 26
	prefs['processors'] = 8
	prefs['opt'] = 'tight'
	prefs['freq'] = True
	prefs['functional'] = 'mPW1PW'
	prefs['basis_set'] = '6-311g(d,p)'
	prefs['solvent'] = None
	prefs['solventmodel'] = None
	prefs['grid'] = 'ultrafine'
	prefs['custom_cmd_line'] = False
	prefs['nodes'] = 1
	prefs['walltime'] = '120:00:00'

	molname = str(p)
	filename = f'OPT/{molname}.com'
	rootline=make_gaussian_rootline(prefs)
	print(rootline)
	write_gaussian_com(prefs, molname, amol, rootline, filename)
	print(filename)
	with open('OPT_IN_ARRAY.txt', 'a') as f:
		print(filename, file=f)
