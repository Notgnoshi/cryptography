#!/bin/bash

main()
{
	patterns="*.aux *.fdb_latexmk *.fls *.log *.out *.pdf *.synctex.gz"
	for pattern in ${patterns}
	do
		find . -name ${pattern} -delete
	done
}

main
