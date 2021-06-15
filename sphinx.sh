rm -r docs
cd sphinx
make clean
cd source
rm -r .ipynb_checkpoints
cd ..
make html
cd build
cp -r html docs
mv docs ../../
cd ../../docs
touch .nojekyll
cd ../
git add docs