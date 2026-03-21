pythonexecutable := $(shell which python3)
cythoncomponents: cylifetree.pyx cygridops.pyx
	$(pythonexecutable) cython_setup.py build_ext --inplace
cylifetree.pyx:
	echo "cylifetree.pyx detected."
	touch cylifetree.pyx
cygridops.pyx:
	echo "cygridops.pyx detected."
