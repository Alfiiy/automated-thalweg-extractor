.PHONY: all data build test clean lint fmt
## Makefile for terrain assessment project

## Example bounding box for the area of interest (can be modified as needed)
BBOX = "7.55,50.30,7.65,50.40"


##	"make all" will execute the build process, which includes fetching data and running the terrain assessment.
all: build

##	"make data" is a placeholder target to indicate that data fetching is handled dynamically via API during the build step.
data:
	@echo "Data fetching is dynamically handled via API during the build step."

## 	"make build" runs the terrain assessment script with the specified bounding box.
build:
	python terrain_assessment.py --bbox $(BBOX)

## 	"make test" runs unit tests located in the src directory that match the pattern *_test.py.
test:
	@echo "Running tests..."
	python -m unittest discover -s src -p "*_test.py"

##	"make clean" removes generated results, temporary files, and Python cache directories to maintain a clean workspace.
clean:
	@echo "Cleaning up generated results..."
ifeq ($(OS),Windows_NT)
	-del /Q /S results\*.tif 2>nul
	-del /Q /S results\*.png 2>nul
	-rmdir /S /Q results\temp 2>nul
	-rmdir /S /Q __pycache__ 2>nul
else
	-rm -rf results/*.tif results/*.png results/temp/* __pycache__
endif

## "make lint" and "make fmt" are placeholders to indicate that linting and formatting are skipped for this build, but can be implemented in the future if needed.
lint:
	@echo "Linting skipped for this build."

fmt:
	@echo "Formatting skipped for this build."