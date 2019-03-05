Special keyword: ``notimported``
=================================

To distinguish if a given module has been imported or is run as the
main script, Python programmers use the following programming idiom::

    if __name__ == '__main__':
        main()

For beginners, the meaning of this idiom is rather obscure.
AvantPy adds a new keyword, providing the following alternative
in the English dialect::

    if notimported:
        main()

