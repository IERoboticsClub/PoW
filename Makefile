TOPIC ?= gans
TOPIC ?= cotracker

install:
	@echo "Installing to local directory..."
	cd $(TOPIC) && \
		python3 -m venv .venv && \
		. .venv/bin/activate && \
		pip install -r requirements.txt
	@echo "Done."
