import os
import elf
from argparse import ArgumentParser

def ilog2(n):
    i = 0
    m = 1
    while m < n:
        m *= 2
        i += 1
    return i

def syms(filename, symbol_section_name='.dynsym'):
    eo = elf.ELF32(filename)
    print
    print os.path.realpath(filename)
    print
    print 'DYNAMIC SYMBOL TABLE:'
    symbol_section = eo.section(symbol_section_name)
    if symbol_section is None:
        return
    for sym in symbol_section:
        if sym.st_shndx == elf.SHN_UNDEF:
            section_name = '*UND*'
        elif sym.st_shndx == elf.SHN_ABS:
            section_name = '*ABS*'
        else:
            section_name = eo.section(index=sym.st_shndx).name()
        flags = [' ' for _ in range(7)]
        if sym.st_bind & elf.STB_GLOBAL:
            flags[0] = 'g'
        if sym.st_bind & elf.STB_WEAK:
            flags[1] = 'w'
        print '{:08x} {} {:5} {:08x} {}'.format(
                sym.st_value, ''.join(flags), section_name, sym.st_size, str(sym))

def section_headers(filename):
    eo = elf.ELF32(filename)
    print
    print os.path.realpath(filename)
    print
    print 'Sections:'
    print 'Idx Name          Size      VMA       LMA       File off  Algn'
    for i, section in enumerate(eo):
        if i == 0:
            continue
        print '{:>3} {:13} {:08x}  {:08x}  {:08x}  {:08x}  2**{}'.format(i - 1,
                section.name(), section.sh_size,
                section.sh_addr, section.sh_addr,
                section.sh_offset, ilog2(section.sh_addralign))
        properties = []
        if section.sh_type != elf.SHT_NOBITS:
            properties.append('CONTENTS')
        if section.sh_flags & elf.SHF_ALLOC:
            properties.append('ALLOC')
            if section.sh_type != elf.SHT_NOBITS:
                properties.append('LOAD')
        if section.sh_flags & elf.SHF_WRITE == 0:
            properties.append('READONLY')
        if section.sh_flags & elf.SHF_EXECINSTR:
            properties.append('CODE')
        elif 'LOAD' in properties:
            properties.append('DATA')
        print '                  {}'.format(', '.join(properties))

ARM32_RELOC_TYPE = {
    2: 'R_ARM_ABS32',
    3: 'R_ARM_REL32',
    21: 'R_ARM_GLOB_DAT',
    22: 'R_ARM_JUMP_SLOT',
    23: 'R_ARM_RELATIVE',
    28: 'R_ARM_CALL',
}

def relocs(filename):
    eo = elf.ELF32(filename)
    print
    print os.path.realpath(filename)
    print
    print 'DYNAMIC RELOCATION RECORDS:'
    print 'OFFSET   TYPE              VALUE'
    for section in eo:
        if section.sh_type != elf.SHT_REL:
            continue
        for rel in section:
            sym = rel.symbol()
            name = sym.name()
            if not name:
                name = eo.section(index=sym.st_shndx).name()
            print '{:08x} {:<17} {}'.format(
                    rel.r_offset,
                    ARM32_RELOC_TYPE.get(rel.r_type, ''),
                    name)

if __name__ == '__main__':
    parser = ArgumentParser('Display information from object <file(s)>.')
    parser.add_argument('-a', '--archive-headers', action='store_true',
            help='Display archive header information')
    parser.add_argument('-sh', '--section-headers', action='store_true',
            help='Display the contents of the section headers')
    parser.add_argument('-t', '--syms', action='store_true',
            help='Display the contents of the symbol table(s)')
    parser.add_argument('-T', '--dynamic-syms', action='store_true',
            help='Display the contents of the dynamic symbol table')
    parser.add_argument('-r', '--reloc', action='store_true',
            help='Display the relocation entries in the file')
    parser.add_argument('-R', '--dynamic-reloc', action='store_true',
            help='Display the dynamic relocation entries in the file')
    parser.add_argument('file')
    args = parser.parse_args()
    if args.syms:
        syms(args.file, symbol_section_name='.symtab')
    elif args.dynamic_syms:
        syms(args.file, symbol_section_name='.dynsym')
    elif args.section_headers:
        section_headers(args.file)
    elif args.reloc:
        relocs(args.file)
    elif args.dynamic_reloc:
        pass
    else:
        pass
