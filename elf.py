import struct

from constants import *
from structures import *

class Section(object):
    def __init__(self, elf, shdr):
        self.elf = elf
        self.shdr = shdr

    def name(self):
        return self.elf.shstrings.get(self.shdr['sh_name'])

    def __getattr__(self, attr):
        return self.shdr.get(attr, None)

    def __str__(self):
        return self.name()

class StringsSection(Section):
    def get(self, name_offset):
        chars = []
        offset = self.sh_offset + name_offset
        while self.elf.raw[offset] != '\0':
            chars.append(self.elf.raw[offset])
            offset += 1
        return ''.join(chars)

def ELF32_ST_BIND(st_info):
    return st_info >> 4

def ELF32_ST_TYPE(st_info):
    return st_info & 0xf

class Symbol(object):
    def __init__(self, symtab, sym):
        self.symtab = symtab
        self.sym = sym

    def __getattr__(self, attr):
        if attr == 'st_bind':
            return ELF32_ST_BIND(self.st_info)
        elif attr == 'st_type':
            return ELF32_ST_TYPE(self.st_info)
        else:
            return self.sym.get(attr, None)

    def name(self):
        return self.symtab.strtab().get(self.st_name)

    def __str__(self):
        return self.name()

class SymbolTable(Section):
    def strtab(self):
        return self.elf.section(index=self.sh_link)

    def symbol(self, index):
        offset = self.sh_offset + index * self.sh_entsize
        return Symbol(self, self.elf.unpack(offset, Elf32_Sym))
    
    def __iter__(self):
        n_entries = self.sh_size / self.sh_entsize
        for i in range(n_entries):
            yield self.symbol(i)

def ELF32_R_SYM(r_info):
    return r_info >> 8

def ELF32_R_TYPE(r_info):
    return r_info & 0xff

class Reloc(object):
    def __init__(self, table, rel):
        self.table = table
        self.rel = rel

    def __getattr__(self, attr):
        if attr == 'r_sym':
            return ELF32_R_SYM(self.r_info)
        elif attr == 'r_type':
            return ELF32_R_TYPE(self.r_info)
        else:
            return self.rel.get(attr, None)

    def symbol(self):
        return self.table.symtab().symbol(self.r_sym)

class RelocTable(Section):
    def symtab(self):
        return self.elf.section(index=self.sh_link)

    def __iter__(self):
        n_entries = self.sh_size / self.sh_entsize
        offset = self.sh_offset
        for i in range(n_entries):
            yield Reloc(self, self.elf.unpack(offset, Elf32_Rel))
            offset += self.sh_entsize

class ELF32(object):
    SECTION_PARSERS = {
        '.interp': Section,
        '.dynsym': SymbolTable,
        '.dynstr': StringsSection,
        '.hash': Section,
        '.gnu.version': Section,
        '.gnu.version_d': Section,
        '.gnu.version_r': Section,
        '.rel.dyn': RelocTable,
        '.rel.plt': RelocTable,
        '.plt': Section,
        '.text': Section,
        '.rodata': Section,
        '.fini_array': Section,
        '.init_array': Section,
        '.dynamic': Section,
        '.got': Section,
        '.data': Section,
        '.bss': Section,
        '.comment': Section,
        '.note.gnu.gold-version': Section,
        '.ARM.attributes': Section,
        '.symtab': SymbolTable,
        '.strtab': StringsSection,
        '.shstrtab': StringsSection,
    }

    SECTION_TYPES = {
        SHT_REL: RelocTable,
    }

    def __init__(self, filename):
        with open(filename, 'rb') as elf_file:
            self.raw = elf_file.read()

        self.ehdr = self.unpack(EI_NIDENT, Elf32_Ehdr)

        sh_off = lambda i: self.ehdr['e_shoff'] + i * self.ehdr['e_shentsize']
        self.shdrs = [self.unpack(sh_off(i), Elf32_Shdr) for i in range(self.ehdr['e_shnum'])]

        sh_shstrings = self.shdrs[self.ehdr['e_shstrndx']]
        self.shstrings = StringsSection(self, sh_shstrings)

        self.shdrs_dict = {self.shstrings.get(shdr['sh_name']): shdr for shdr in self.shdrs}

    def get_section_class(self, shdr):
        name = self.shstrings.get(shdr['sh_name'])
        if name in self.SECTION_PARSERS:
            return self.SECTION_PARSERS[name]
        elif shdr['sh_type'] in self.SECTION_TYPES:
            return self.SECTION_TYPES[shdr['sh_type']]
        else:
            return Section

    def section(self, name=None, index=None):
        if name is not None and index is not None:
            # User must select one indexing mode
            return None
        if name and index:
            # User can not select both indexing modes
            return None
        if index is not None:
            if index < 1 or index > self.ehdr['e_shnum']:
                return None
            shdr = self.shdrs[index]
            #name = self.shstrings.get(shdr['sh_name'])
        if name is not None:
            if name not in self.shdrs_dict:
                return None
            shdr = self.shdrs_dict[name]
        return self.get_section_class(shdr)(self, shdr)

    def __iter__(self):
        for shdr in self.shdrs:
            name = self.shstrings.get(shdr['sh_name'])
            yield self.get_section_class(shdr)(self, shdr)

    def unpack(self, offset, spec, little_endian=True):
        endianesse = '<' if little_endian else '>'
        names, types = zip(*spec)
        fmt = endianesse + ''.join(types)
        values = struct.unpack_from(fmt, self.raw, offset)
        return dict(zip(names, values))

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 2:
        filename = argv[1]
        with open(filename, 'rb') as elf_file:
            e_ident_raw = elf_file.read(EI_NIDENT)
            e_ident = struct.unpack_from('<16B', e_ident_raw, 0)
            if e_ident[EI_CLASS] == ELFCLASS32:
                eo = ELF32(filename)
                for i, section in enumerate(eo):
                    print i, section, section.shdr
            else:
                raise NotImplementedError('ELF64 not supported yet')
