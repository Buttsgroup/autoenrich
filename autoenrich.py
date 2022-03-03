from mol_translator import aemol
import glob
import os
import subprocess

class Autoenrich:
    def __init__(self, opt_params={}, nmr_params={}):
        self.base_path = os.getcwd()
        self.opt_params = opt_params
        self.nmr_params = nmr_params

    def check_opt_params(self):
        if 'mol' not in self.opt_params:
            self.opt_params['mol'] = {}
        if 'charge' not in self.opt_params['mol'].keys():
            self.opt_params['mol']['charge'] = 0
        if 'multiplicity' not in self.opt_params['mol'].keys():
            self.opt_params['mol']['multiplicity'] = 1
        if 'optimisation' not in self.opt_params:
            self.opt_params['optimisation'] = {}
        if 'memory' not in self.opt_params['optimisation'].keys():
            self.opt_params['optimisation']['memory'] = 26
        if 'processor' not in self.opt_params['optimisation'].keys():
            self.opt_params['optimisation']['processor'] = 8
        if 'functional' not in self.opt_params['optimisation'].keys():
            self.opt_params['optimisation']['functional'] = 'mPW1PW'
        if 'basisset' not in self.opt_params['optimisation'].keys():
            self.opt_params['optimisation']['basisset'] = '6-311g(d,p)'
        if 'solvent' not in self.opt_params['optimisation'].keys():
            self.opt_params['optimisation']['solvent'] = None
        if 'solventmodel' not in self.opt_params['optimisation'].keys():
            self.opt_params['optimisation']['solventmodel'] = None
        if 'grid' not in self.opt_params['optimisation'].keys():
            self.opt_params['optimisation']['grid'] = 'ultrafine'
        if 'custom_cmd_line' not in self.opt_params['optimisation'].keys():
            self.opt_params['optimisation']['custom_cmd_line'] = None
        if 'nodes' not in self.opt_params['optimisation'].keys():
            self.opt_params['optimisation']['nodes'] = 1
        if 'walltime' not in self.opt_params['optimisation'].keys():
            self.opt_params['optimisation']['walltime'] = '120:00:00'

    def check_nmr_params(self):
        if 'mol' not in self.nmr_params:
            self.nmr_params['mol'] = {}
        if 'charge' not in self.nmr_params['mol'].keys():
            self.nmr_params['mol']['charge'] = 0
        if 'multiplicity' not in self.nmr_params['mol'].keys():
            self.nmr_params['mol']['multiplicity'] = 1
        if 'NMR' not in self.nmr_params:
            self.nmr_params['NMR'] = {}
        if 'memory' not in self.nmr_params['NMR'].keys():
            self.nmr_params['NMR']['memory'] = 26
        if 'processor' not in self.nmr_params['NMR'].keys():
            self.nmr_params['NMR']['processor'] = 8
        if 'functional' not in self.nmr_params['NMR'].keys():
            self.nmr_params['NMR']['functional'] = 'wB97XD'
        if 'basisset' not in self.nmr_params['NMR'].keys():
            self.nmr_params['NMR']['basisset'] = '6-311g(d,p)'
        if 'solvent' not in self.nmr_params['NMR'].keys():
            self.nmr_params['NMR']['solvent'] = None
        if 'solventmodel' not in self.nmr_params['NMR'].keys():
            self.nmr_params['NMR']['solventmodel'] = None
        if 'mixed' not in self.nmr_params['NMR'].keys():
            self.nmr_params['NMR']['mixed'] = True
        if 'custom_cmd_line' not in self.nmr_params['NMR'].keys():
            self.nmr_params['NMR']['custom_cmd_line'] = None
        if 'nodes' not in self.nmr_params['NMR'].keys():
            self.nmr_params['NMR']['nodes'] = 1
        if 'walltime' not in self.nmr_params['NMR'].keys():
            self.nmr_params['NMR']['walltime'] = '120:00:00'

    def make_opt_input(self, filepath):
        files = glob.glob(filepath)
        for file in files:
            id = file.split('/')[-1].split('.')[0]
            ext = file.split('.')[-1]
            mol = aemol(id)
            mol.from_file_pyb(file, ftype=ext)
            mol_name = f'autoenrich_{id}'
            file_name = f'{self.base_path}/OPT/{mol_name}.com'
            make_g09_optin(self.opt_params, mol_name, mol, file_name)
            with open('OPT_ARRAY.txt', 'a') as f:
                print(file_name, file=f)

    def check_opt_log(self,filepath):


    def make_nmr_input(self, filepath):
        files = glob.glob(filepath)
        for file in files:
            id = file.split('/')[-1].split('.')[0]
            ext = file.split('.')[-1]
            try:
                mol = aemol(id)
                mol.from_file_pyb(file, ftype=ext)
                mol_name = f'autoenrich_{id}'
                file_name = f'NMR/{mol_name}.com'
                if not os.path.exists(file_name):
                    make_g09_optin(self.nmr_params, mol_name, mol, file_name)
                    with open('NMR_ARRAY.txt', 'a') as f:
                        print(file_name, file=f)

            except Exception as e:
        		print('Exception: ', e)
        		file = f'OPT/{str(p)}.com'
        		with open('OPT_RESUB_ARRAY.txt', 'a') as f:
        			print(file, file=f)

