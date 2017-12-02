PROJECT_NAME=hw2

.PHONY: all clean view

all: $(PROJECT_NAME).pdf

$(PROJECT_NAME).pdf: $(PROJECT_NAME).tex
	latexmk -pdf -shell-escape -file-line-error -interaction=batchmode --synctex=1 $<

clean:
	latexmk -c
	rm -rf _minted-*
	rm -f *.synctex\(busy\)

cleanall:
	latexmk -C
	rm -rf _minted-*
	rm -f *.synctex\(busy\)
	rm -f *.synctex.gz

view:
	xdg-open $(PROJECT_NAME).pdf &
