.SUFFIXES: .py .v

%.v: %.py
	python $<

all: tests hdl

clean:
	rm *.vcd?*
	rm *.pyc
	rm *.v
	rm *.vhd

tests:
	nosetests --with-isolation

hdl: tests register.v mux2.v mem.v

