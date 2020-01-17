all:
	cd ecol; go build
	cd xc; make

deploy:
	mkdir -p hamilton
	tar -czvf hamilton/xc.tar.gz xc
	scp -i hamilton/id_rsa /home/eeojun/go/src/github.com/eugene-eeo/project/hamilton/xc.tar.gz  hvcs85@hamilton.dur.ac.uk:/ddn/home/hvcs85/eeojun
