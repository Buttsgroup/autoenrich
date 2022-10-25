from openbabel import pybel as pyb

import glob

import os

import sys
sys.path.append('INSERT_PATH_TO_MOL_TRANSLATOR_HERE')
from mol_translator.aemol import Aemol

from mol_translator.comp_chem.gaussian.gaussian_input import write_gaussian_com
from mol_translator.comp_chem.gaussian.gaussian_input import make_gaussian_rootline


files = glob.glob('OPT/*log')

for file in files:

	print(file)
	p = file.split('/')[1].split('.')[0]
	print(p)
	try:
		amol = Aemol(p)
		amol.from_file_ob(file, ftype='g09')

		
		prefs = {}
		prefs['calc_type'] = 'nmr'
		prefs['charge'] = 0
		prefs['multiplicity'] = 1
		prefs['software'] = 'g09'
		prefs['memory'] = 26
		prefs['processors'] = 8
		prefs['functional'] = 'wB97XD'
		prefs['basis_set'] = '6-311g(d,p)'
		prefs['solvent'] = None
		prefs['solventmodel'] = ''
		prefs['mixed'] = True
		prefs['custom_cmd_line'] = False
		prefs['nodes'] = 1
		prefs['walltime'] = '120:00:00'

		molname = str(p)
		filename = f'NMR/{molname}.com'
		if not os.path.exists(filename):
			
			root_line=make_gaussian_rootline(prefs)
			write_gaussian_com(prefs, molname, amol, root_line, filename)
			print(filename)
			with open('NMR_IN_ARRAY.txt', 'a') as f:
				print(filename, file=f)
	except Exception as e:
		print('Exception: ', e)
		file = 'OPT/'+str(p)+'.com'
		with open('OPT_RESUB_ARRAY.txt', 'a') as f:
			print(file, file=f)
