set -e

if [[ -z "$1" ]]
then
  version=$1
else
  echo "missing version argument, v1.0 set as default"
  version="v1.0"
fi
version=v1.0

conda env remove -n mol_translator-"${version}"
conda create -n mol_translator-_"${version}" python=3 -y
conda install -n mol_translator-_"${version}" numpy scipy pandas -y
conda install -n mol_translator-_"${version}" -c openbabel openbabel -y
conda install -n mol_translator-_"${version}" -c conda-forge xorg-libxrender -y
conda install -n mol_translator-_"${version}" -c rdkit rdkit -y
conda install -n mol_translator-_"${version}" -c conda-forge tqdm -y
conda install -n mol_translator-_"${version}" pytest -y
conda deactivate
