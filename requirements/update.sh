# will update all of the quartet dependency files
echo "Updating QU4RTET dependency files..."
pip-compile test.in -o test.txt --upgrade
pip-compile local.in -o local.txt --upgrade
pip-compile production.in -o production.txt --upgrade
echo "Complete."

