# vars
REQUIREMENTS_FILEPATH=./requirements.txt

# general commands (not depend on the used system)
init-general:
	@echo "> Initalize python virtual env"
	python -m venv venv

# init project for windows system
init-windows: init-general
	.\venv\Scripts\activate
	./venv/Scripts/python -m pip install --upgrade pip
	./venv/Scripts/python -m pip install -r $(REQUIREMENTS_FILEPATH)

# init project for unix system
init-unix: init-general
	./venv/bin/activate
	./venv/Scripts/python -m pip install --upgrade pip
	./venv/Scripts/python -m pip install -r $(REQUIREMENTS_FILEPATH)