VENV = venv
FLASK_APP = app.py

install:
	python3 -m venv $(VENV)  # Create a virtual environment
	./$(VENV)/bin/pip install --upgrade pip  # Upgrade pip inside the venv
	./$(VENV)/bin/pip install -r requirements.txt  # Install required dependencies

run:
	FLASK_APP=$(FLASK_APP) FLASK_ENV=development ./$(VENV)/bin/flask run --port 3000

clean:
	rm -rf $(VENV)

reinstall: clean install