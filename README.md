# autoENRICH

Update (28/01/2022)

  - Function renaming to comply with changes to mol_translator
  - bp1 branch added
  - Master branch rebased to bp1 code
  - Minor changes to naming method

------------------------------------------------------------------------------------------------------------
autoENRICH

Instructions to setup autoenrich on HPC cluster (BC3/BC4), last updated April 2021

1. Upload the autoenrich_scripts to your BC3/BC4 area:
   On Windows: Use winscp (if you're not sure how to use it, google it)
   On macOS/Linux, make sure you're in the area where the autoenrich_scripts folder is located in the terminal then type "scp -r autoenrich_scripts/ <YOUR_USERNAME>@bluecrystalp3.bris.ac.uk:~/."

   Or type "git clone git@github.com:Buttsgroup/autoenrich.git" in the desired area

   Connect to BC3, when you type "ls" you should see the autoenrich_scripts folder if you've successfully uploaded it. If it's not then redo the upload and double check you've done it right

2. Check if you have anaconda loaded:
   Type "module list" , if you see languages/python-anaconda... list then you can skip to step 4, otherwise:
   Type "module load languages/python-anaconda3.8.5-2020.11" or whichever latest version is available, it might ask you to restart the shell, if so disconnect and reconnect to BC3

3. Setup a conda environment for autoenrich:
   Type "cd autoenrich_scripts" and then "bash make_conda_env.sh", let the script run and it will make the conda environment.
   Again it might ask you to restart the shell so disconnect and reconnect.
   Check that the conda environment has been successfully created, type "conda activate imp_io" , if you see (imp_io) in the command line it's working

4. Clone mol_translator which autoenrich_scripts is built around. To do this:
   cd back into the home directory, type "cd"
   Created a folder and subfolder to store the mol_translator, type "mkdir -p opt/bg_code"
   cd into the new folder, type "cd opt/bg_code"
   Now clone the mol_translator into this area, type "git clone https://github.com/Buttsgroup/mol_translator.git" , if it says the git command is not available, install it by typing "conda install git" and rerun the git clone command

5. Final tweaks
   Return to the autoenrich_scripts area "cd ~/autoenrich_scripts/"

   using vim or nano open all the .py files and change the line:

   "sys.path.append('/newhome/bd20841/opt/bg_code/mol_translator/')" to "sys.path.append('/newhome/<YOUR_USERNAME>/opt/bg_code/mol_translator/')"

   Initial setup is done

Instructions to use autoenrich on HPC (BC3)
1. Make sure you're in the autoenrich_scripts area "cd autoenrich"
   activate conda env, "conda activate imp_io"

2. Place your molecules into the INPUT folders (accepts most file extentions such as .xyz, .mol2 .sdf)
   Tweak make_opt_input.py using vim/nano to your liking with whatever gaussian route line variables you need, they start with "prefs['optimisation']"

   Run the make_opt_input.py file "python make_opt_input.py", it should create an OPT_IN_ARRAY.txt file

   Tweak the submit_opt.qsub using vim/nano to adjust bc3 queueing parameters:
    The "#PBS -t" line should match the line count of the OPT_IN_ARRAY.txt file, check this by running "cat OPT_IN_ARRAY.txt | wc -l" in the autoenrich_scripts folder, the number it prints is the number you need in that line. For example if it returns "12" then the line in submit_opt.qsub should be "#PBS -t 1-12"

    Other things such as walltime and memory allocation can be tweaked at your discretion.

3. When the g09 opt finishes running repeat the previous step but with make_gauss_input.py instead with similar tweaks if needed prefs['NMR'].
   Running "python make_gauss_input.py" creates NMR_IN_ARRAY.txt file

   Tweak submit_nmr.qsub if needed and submit to queue. Same as with submit_opt.qsub, remember to change submit_nmr.qsub "#PBS -t" line but match it to NMR_IN_ARRAY.txt this time

4. Once nmr job have finished the output log files will be in the NMR/ folder, these can be converted to nmredata.sdf files by running make_nmr_output.py these files will be placed in the OUTPUT folder.
