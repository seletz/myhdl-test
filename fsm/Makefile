PYTHON=~/.virtualenvs/myhdl/bin/python
NOSE=~/.virtualenvs/myhdl/bin/nosetests
GTKWAVE=open -a gtkwave

.SUFFIXES: .py .v


%.v: %.py
	$(PYTHON) $<

%.vhd: %.py
	$(PYTHON) $<

all: test hdl

clean:
	rm *.vcd?*
	rm *.pyc
	rm *.v
	rm *.vhd

test: fsm.py
	$(NOSE) --with-isolation $<

hdl: fsm.vhd

wave: test_fsm.vcd
	$(GTKWAVE) $<

