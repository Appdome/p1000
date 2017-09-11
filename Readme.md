# *p1000*?
*p1000* is pronounced "PyELeF" (1000 in hebrew is אלף = elef).

# Ahhh, so what's that?
*p1000* is a library for parsing ELF files utilizing Python's strengths.

# Why not use binutils?
While binutils are extremely useful, ubiquitous and support multiple architectures, they all boil down to text output. And processing text is not always the most productive thing.

Take for example the following task:

    Find all the undefined (imported) symbols for which there is at least one relocation entry of a function-call type.

You could potentially use `objdump -r` and `objdump -t` and then somehow filter and cross reference them, but it will not look good.

Wouldn't it be nice if I could just do something like this:

    function_relocs = [rel.symbol() for rel in ELF('object.o').relocs() if rel.r_type in [R_ARM_CALL, R_ARM_JUMP24]]
    print [symbol.name() for symbol in function_relocs if symbol.st_shndx == SHN_UNDEF]

Or, for example, it makes sense to iterate over all the sections in an ELF file like this:

    for section in ELF('libsomething.so'):
        ...

# Support
* Platforms:
** ARM32
* Features:
** Iteration:
*** Sections in an ELF file
*** Symbols in symbol table sections
*** Relocation entries in relocation table sections
** Associate sections to their names
** Associate symbols to their names
** Associate relocation entries to their symbols
* Objdump implementation:
** `-h`
** `-t`/`-T`
** `-r`
