PROJECT_NAME=hw1

.PHONY: $(PROJECT_NAME).pdf all clean

all: $(PROJECT_NAME).pdf

$(PROJECT_NAME).pdf: $(PROJECT_NAME).tex
	latexmk -pdf --synctex=1 -file-line-error -interaction=nonstopmode -shell-escape -use-make $<

clean:
	latexmk -C
	rm -rf _minted-*

view:
	xdg-open $(PROJECT_NAME).pdf &

