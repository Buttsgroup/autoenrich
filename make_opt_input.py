
import pybel as pyb

import glob


import sys
sys.path.append('INSERT_PATH_TO_MOL_TRANSLATOR_HERE')
from mol_translator.aemol import aemol
from mol_translator.properties.energy.energy_input import make_g09_optin
from mol_translator.properties.nmr.nmr_input import make_g09_nmrin

files = glob.glob('INPUT/*')

for file in files:

	id = file.split('/')[-1].split('.')[0]
	ft = file.split('.')[-1]

	amol = aemol(id)
	amol.from_file_pyb(file, ftype=ft)

	prefs = {}
	prefs['mol'] = {}
	prefs['mol']['charge'] = 0
	prefs['mol']['multiplicity'] = 1
	prefs['optimisation'] = {}
	prefs['optimisation']['software'] = 'g09'
	prefs['optimisation']['memory'] = 26
	prefs['optimisation']['processors'] = 8
	prefs['optimisation']['opt'] = 'tight'
	prefs['optimisation']['freq'] = True
	prefs['optimisation']['functional'] = 'mPW1PW'
	prefs['optimisation']['basisset'] = '6-311g(d,p)'
	prefs['optimisation']['solvent'] = None
	prefs['optimisation']['solventmodel'] = None
	prefs['optimisation']['grid'] = 'ultrafine'
	prefs['optimisation']['custom_cmd_line'] = False
	prefs['optimisation']['nodes'] = 1
	prefs['optimisation']['walltime'] = '120:00:00'

	molname = 'autoenrich_'+str(id)
	filename = f'OPT/{molname}.com'
	make_g09_optin(prefs, molname, amol, filename)
	print(filename)
	with open('OPT_IN_ARRAY.txt', 'a') as f:
		print(filename, file=f)
