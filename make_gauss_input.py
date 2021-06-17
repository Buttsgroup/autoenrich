
import pybel as pyb

import glob

import os

import sys
sys.path.append('/newhome/bd20841/opt/bg_code/mol_translator/')
from mol_translator.aemol import aemol
#from mol_translator.properties.energy.energy_input import make_optin
from mol_translator.properties.nmr.nmr_input import make_g09_nmrin

files = glob.glob('OPT/*.log')

for file in files:

	print(file)
	p = file.split('_')[-1].split('.')[0]
	try:
		amol = aemol(p)
		amol.from_file(file, ftype='g09')

		prefs = {}
		prefs['mol'] = {}
		prefs['mol']['charge'] = 0
		prefs['mol']['multiplicity'] = 1
		prefs['NMR'] = {}
		prefs['NMR']['software'] = 'g09'
		prefs['NMR']['memory'] = 26
		prefs['NMR']['processors'] = 8
		prefs['NMR']['functional'] = 'wB97XD'
		prefs['NMR']['basisset'] = '6-311g(d,p)'
		prefs['NMR']['solvent'] = 'none'
		prefs['NMR']['solventmodel'] = ''
		prefs['NMR']['mixed'] = True
		prefs['NMR']['custom_cmd_line'] = False
		prefs['NMR']['nodes'] = 1
		prefs['NMR']['walltime'] = '120:00:00'

		molname = 'autoenrich_'+str(p)
		filename = 'NMR/'+molname+'.com'
		if not os.path.exists(filename):
			make_g09_nmrin(prefs, molname, amol, filename)
			print(filename)
			with open('NMR_IN_ARRAY.txt', 'a') as f:
				print(filename, file=f)

	except Exception as e:
		print('Exception: ', e)
		file = 'OPT/'+str(p)+'.com'
		with open('OPT_RESUB_ARRAY.txt', 'a') as f:
			print(file, file=f)
