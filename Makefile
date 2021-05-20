all: where-was-i

where-was-i: container-build.log where-was-i.in
	LABEL=$$(tail -1 container-build.log); \
	sed s/@LABEL@/$$LABEL/ $@.in > $@
	chmod +x $@

container-build.log: Dockerfile
	[ -d dist ] && rm -rf dist
	python setup.py sdist
	podman build -f Dockerfile | tee container-build.log

Dockerfile: Dockerfile.in
	VER=$$(printf "from where_was_i import __version__\nprint(__version__)\n" | python -); \
	sed -e s/@VERSION@/$$VER/ Dockerfile.in > Dockerfile

clean:
	rm -f $$(echo $$(cat .gitignore))
