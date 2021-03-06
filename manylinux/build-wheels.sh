#!/bin/bash
# Adapted from https://github.com/pypa/python-manylinux-demo/blob/master/travis/build-wheels.sh
# Add --debug after the executable name to prevent optimization
set -e -x

export OMP_NUM_THREADS=16  # Fix for https://github.com/myselfhimself/gmic-py/issues/47

PYBIN_PREFIX=${PYBIN_PREFIX:-cp3}

# Install a system package required by our library
yum check-update || { echo "yum check-update failed but manylinux build-wheels script will continue" ; }
yum install fftw-devel libpng-devel zlib-devel libgomp libtiff-devel libjpeg-devel wget -y || { echo "Fatal yum dependencies install error" ; exit 1; }

cd /io/


# Compile wheels #Choosing only Python 3 executables
for PYBIN in /opt/python/$PYBIN_PREFIX*/bin; do
    # Skip Python35 executables, slated for end of support in september 2020 https://devguide.python.org/#status-of-python-branches
    if [[ $PYBIN == *"cp35"* ]]; then
        continue
    fi

    # home made patching for our scripts
    export PIP3="${PYBIN}/pip"
    export PYTHON3="${PYBIN}/python"

    bash /io/build_tools.bash 1_clean_and_regrab_gmic_src

    "${PYBIN}/pip" install -r /io/dev-requirements.txt  || { echo "Fatal pip requirements download error" ; exit 1; }
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/ -vvv || { echo "Fatal wheel build error" ; exit 1; }
done

find /opt/python -name auditwheel
cd /io/wheelhouse
# Bundle external shared libraries into the wheels
for whl in *gmic*$PYBIN_PREFIX*-linux*.whl; do
    which auditwheel
    auditwheel -v repair "$whl" --plat $PLAT -w /io/wheelhouse/  2>&1 | tee -a /io/REPAIRLOG || { echo "Fatal auditwheel repair error" ; exit 1; }
done
