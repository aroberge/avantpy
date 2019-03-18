"""translations: fr.py"""

fr = {
    "IfNobreakError": """
    Exception AvantPy: IfNobreakError\n
    Erreur trouvée dans le fichier {filename} à la ligne {nobreak_linenumber}.\n
    Dialecte utilisé: {dialect}\n
{partial_source}

    Le mot-clé {nobreak_kwd} spécifique à Avantpy ne peut pas être utilisé
    dans un énoncé si/sinonsi/sinon (Python: if/elif/else).
""",
    "NobreakFirstError": """
    Exception AvantPy: NobreakFirstError\n
    Erreur trouvée dans le fichier {filename} à la ligne {linenumber}.\n
    Dialecte utilisé: {dialect}\n
{partial_source}

    Le mot-clé {nobreak_kwd} spécifique à Avantpy peut seulement être utilisé
    au lieu de sinon (Python: else) lorsqu'il débute un nouvel énoncé
    dans des boucles 'pour' ou 'tantque' (Python: for/while).
""",
    "NobreakSyntaxError": """
    Exception AvantPy: NobreakSyntaxError\n
    Erreur trouvée dans le fichier {filename} à la ligne {linenumber}.\n
    Dialecte utilisé: {dialect}\n
{partial_source}

    Le mot-clé {nobreak_kwd} spécifique à Avantpy peut seulement être utilisé
    au lieu de sinon (Python: else) lorsqu'il débute un nouvel énoncé
    dans des boucles 'pour' ou 'tantque' (Python: for/while)
""",
    "MissingRepeatError": """
    Exception AvantPy: MissingRepeatError\n
    Erreur trouvée dans le fichier {filename} à la ligne {linenumber}.\n
    Dialecte utilisé: {dialect}\n
{partial_source}

    Le mot-clé {keyword} spécifique à Avantpy peut seulement être utilisé
    s'il est précédé de 'répéter'.
""",
    "RepeatFirstError": """
    Exception AvantPy: RepeatFirstError\n
    Erreur trouvée dans le fichier {filename} à la ligne {linenumber}.\n
    Dialecte utilisé: {dialect}\n
{partial_source}

    Le mot-clé {repeat_kwd} spécifique à Avantpy peut seulement être utilisé
    pour débuter une nouvelle boucle 'pour' ou 'tantque'
    (équivalent Python: 'for' ou 'while').
""",
    "TryNobreakError": """
    Exception AvantPy: TryNobreakError\n
    Erreur trouvée dans le fichier {filename} à la ligne {nobreak_linenumber}.\n
    Dialecte utilisé: {dialect}\n
{partial_source}

    Le mot-clé {nobreak_kwd} spécifique à Avantpy ne peut pas être utilisé dans
    un énoncé essayer/siexception/sinon/finalement (Python: try/except/else/finally).
""",
    "MismatchedBracketsError": """
    Exception AvantPy: MismatchedBracketsError\n
    Erreur trouvée dans le fichier {filename} aux lignes
    [{open_linenumber} - {close_linenumber}].\n
    Dialecte utilisé: {dialect}\n
{partial_source}

    Le symbole gauche {open_bracket} ne correspond pas au symbole droit {close_bracket}.
""",
    "MissingLeftBracketError": """
    Exception AvantPy: MissingLeftBracketError\n
    Erreur trouvée dans le fichier {filename} à la ligne {linenumber}.\n
    Dialecte utilisé: {dialect}\n
{partial_source}

    Le symbole droit {bracket} n'a pas de symbole gauche correspondant.
""",
    "UnknownLanguage": """
    Exception AvantPy: UnknownLanguage\n

    Le langage inconnu suivant a été demandé: {lang}.
    Les langages connus sont: {all_langs}.
""",
    "UnknownDialect": """
    Exception AvantPy: UnknownDialect\n

    Le dialecte inconnu suivant a été demandé: {dialect}.
    Les dialectes connus sont: {all_dialects}.
""",
}
