PROJECT=pygod
TR=tr
LOCALES=ru
TR_DIR=share
SOURCES=$(wildcard *.py monitor/*/*.py)

INSTALL_DIR=$(XDG_DATA_DIR)/$(PROJECT)
PO_FILES=$(LOCALES:%=$(TR_DIR)/$(PROJECT)_%.po)
MO_FILES=$(PO_FILES:%.po=%.mo)

all: mo

mo: $(MO_FILES)

%.mo: %.po
	pybabel compile -f -i $< -o $@

po: $(PO_FILES)

%.po: $(PROJECT).pot
	@if [ -f $@ ]; then \
		pybabel update -N -i $< -d $(TR_DIR) -l $(@:$(TR_DIR)/$(PROJECT)_%.po=%) -o $@; \
	else \
		pybabel init      -i $< -d $(TR_DIR) -l $(@:$(TR_DIR)/$(PROJECT)_%.po=%) -o $@; \
	fi

$(PROJECT).pot: $(SOURCES)
	@pybabel extract --omit-header --no-wrap -k $(TR) -o $@ .

clean:
	$(RM) $(PROJECT).pot
