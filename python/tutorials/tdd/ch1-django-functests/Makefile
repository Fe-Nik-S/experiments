
init_env: install_external_libs
	python3 -m venv env

install_requirements:
	source env/bin/activate && python3 -m pip install -r requirements.txt

install_external_libs:
	sudo apt install python3-venv

run_server:
	python3 testproject/manage.py runserver
