set -e

if [[ -z "$1" ]]
then
  version=$1
else
  echo "missing version argument, v1.0 set as default"
  version="v1.0"
fi
version=v1.0

conda env remove -n imp_io_"${version}"
conda create -n imp_io_"${version}" python=3 -y
conda install -n imp_io_"${version}" numpy scipy pandas -y
conda install -n imp_io_"${version}" -c openbabel openbabel -y
conda install -n imp_io_"${version}" -c conda-forge xorg-libxrender -y
conda install -n imp_io_"${version}" -c rdkit rdkit -y
conda install -n imp_io_"${version}" -c conda-forge tqdm -y
conda install -n imp_io_"${version}" pytest -y
conda deactivate