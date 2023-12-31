#!/usr/bin/env bash
# will update all of the quartet dependency files
echo "Updating QU4RTET dependency files..."
pip-compile test.in -o test.txt --upgrade
pip-compile local.in -o local.txt --upgrade
pip-compile production.in -o production.txt --upgrade
pip-compile production.in -o ../requirements.txt --upgrade
pip-compile pypy.in -o pypy.txt --upgrade
pip-compile ec2.in -o ec2.txt --upgrade
pip-compile serial-lab.in -o serial-lab.txt --upgrade
pip-compile pypy-test.in -o pypy-test.txt --upgrade
echo "Complete."

