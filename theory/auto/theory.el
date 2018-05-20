(TeX-add-style-hook
 "theory"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("article" "11pt")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("inputenc" "utf8") ("fontenc" "T1") ("ulem" "normalem") ("geometry" "margin=1.0in") ("biblatex" "backend=bibtex" "style=numeric" "sorting=none" "giveninits=true" "doi=true" "url=false" "isbn=false" "eprint=false")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art11"
    "inputenc"
    "fontenc"
    "graphicx"
    "grffile"
    "longtable"
    "wrapfig"
    "rotating"
    "ulem"
    "amsmath"
    "textcomp"
    "amssymb"
    "capt-of"
    "hyperref"
    "xcolor"
    "float"
    "tikz"
    "physics"
    "setspace"
    "titling"
    "authblk"
    "subcaption"
    "geometry"
    "biblatex")
   (LaTeX-add-labels
    "sec:orgd7f3c2c"
    "eqn:ufree_intro"
    "eqn:usfqexp_intro"
    "eqn:ideal"
    "sec:org6287d7d"
    "org5d759dd"
    "eqn:sfq"
    "eqn:sfqint"
    "eqn:ufree"
    "eqn:expansion"
    "eqn:usfq"
    "eqn:usfqclose"
    "eqn:usfqexp"
    "sec:orgde80004"
    "eqn:states"
    "eqn:gates"
    "sec:org3c861e5"
    "org949cc7d"
    "sec:orgdfdecfd"
    "eqn:spin"
    "eqn:ab"
    "sec:orgf77bd53"
    "sec:orgc45eb18"
    "eqn:rotate_a"
    "sec:org9234d63")
   (LaTeX-add-bibliographies
    "/Users/kangbo/Documents/ref/bib/library"))
 :latex)

