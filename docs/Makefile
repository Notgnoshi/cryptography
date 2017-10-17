PROJECT_NAME=docs

.PHONY: $(PROJECT_NAME).pdf all clean

all: $(PROJECT_NAME).pdf

$(PROJECT_NAME).pdf: $(PROJECT_NAME).tex
	latexmk -pdf -pdflatex="pdflatex -interaction=nonstopmode -shell-escape" -use-make $<

clean:
	latexmk -c

view:
	xdg-open $(PROJECT_NAME).pdf
