PROJECT_NAME=exam2

.PHONY: all clean view

all: $(PROJECT_NAME).pdf

# Adds the Maple stylesheets to the search path for LaTeX before running the command.
$(PROJECT_NAME).pdf: $(PROJECT_NAME).tex
	TEXINPUTS=:/opt/maple2015/etc latexmk -pdf -shell-escape -file-line-error -interaction=batchmode --synctex=1 $<

# A target to build with better error messages when latexmk craps itself.
error:
	TEXINPUTS=:/opt/maple2015/etc pdflatex -shell-escape -file-line-error $(PROJECT_NAME).tex

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
	1>/dev/null 2>/dev/null xdg-open $(PROJECT_NAME).pdf &
