# clone repo
git clone https://github.com/intel/e2eAIOK.git
cd e2eAIOK
git submodule update --init -recursive

# apply patch
cd modelzoo/rnnt/pytorch && bash patch_rnnt.sh