build:
	pyinstaller --onedir egrep.py
clean:
	rm -rf ./build 
	rm -rf ./dist
	rm egrep.spec