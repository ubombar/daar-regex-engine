build:
	pyinstaller --onedir egrep.py
clean:
	rm -rf ./build 
	rm -rf ./dist
	rm egrep.spec
	rm ./tests/pg71838.txt
test:
	./test.sh