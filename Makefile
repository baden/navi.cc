include version.mk

PROJECT_PATH = src/api

#all: www
all: compile

www:
	echo "Build www..."
	echo $(CURDIR)
	coffee

compile:
	echo "Compile..."
	echo $(CURDIR)
	#python tools/compile.py
	python -m compileall -f -l -q $(PROJECT_PATH)
	cp $(PROJECT_PATH)/*.pyc ./build/
	#cp servers/gevent-channel-server/server.key ./bin/
	#cp servers/gevent-channel-server/server.crt ./bin/
	#cd tools
	#copy2gsmcontrol.org.sh
	#popd
