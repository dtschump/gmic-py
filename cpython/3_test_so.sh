cd ./build/lib.linux-x86_64-3.6/ ; pip install -r ../../tests/requirements.txt ; pwd; ls; LD_LIBRARY_PATH=. python -m pytest ../../tests/test_gmic_install_and_run.py ; cd ../..
