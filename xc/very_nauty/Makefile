PREFIX=/usr/local/
OPT=-g
OPT=-O3

#########################################################################

PKG=very_nauty-1.1

all: libvn_graph.a vn_graph_chi vn_graph_omega

install: all
	cp libvn_graph.a ${PREFIX}/lib
	cp vn_graph.h ${PREFIX}/include
	cp vn_graph_chi vn_graph_omega ${PREFIX}/bin
	/sbin/ldconfig

libvn_graph.a: vn_graph.o
	ar r libvn_graph.a vn_graph.o

vn_graph.o: vn_graph.c trick.c clique.c rainbow.c geng_reader.c
	gcc -c -Wall ${OPT} -fomit-frame-pointer vn_graph.c

vn_graph_chi: vn_graph_chi.c vn_graph.o
	gcc -Wall ${OPT} -fomit-frame-pointer vn_graph_chi.c vn_graph.o -o vn_graph_chi -lm
	
vn_graph_chi_dash: vn_graph_chi_dash.c vn_graph.o
	gcc -Wall ${OPT} -fomit-frame-pointer vn_graph_chi_dash.c vn_graph.o -o vn_graph_chi_dash -lm
	
vn_graph_omega: vn_graph_omega.c vn_graph.o
	gcc -Wall ${OPT} -fomit-frame-pointer vn_graph_omega.c vn_graph.o -o vn_graph_omega -lm

clean:
	rm -f *o *a a.out vn_graph_omega vn_graph_chi
