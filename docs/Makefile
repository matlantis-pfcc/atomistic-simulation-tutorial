# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
LANG    ?=ja
SPHINXBUILD   ?= poetry run sphinx-build
SOURCEDIR     = ./
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)/tutorials/$(LANG)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	rm -rf "./$(BUILDDIR)"
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)/tutorials/$(LANG)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	cp -r "../tutorials/$(LANG)/output" "$(BUILDDIR)/html/output"
	cp "./_static/js/plotly.js" "$(BUILDDIR)/html/"
