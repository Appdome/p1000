# Structures

Elf32_Addr = 'L'
Elf32_Half = 'H'
Elf32_Off = 'L'
Elf32_Sword = 'l'
Elf32_Word = 'L'

Elf32_Ehdr = [
        ('e_type', Elf32_Half),
        ('e_machine', Elf32_Half),
        ('e_version', Elf32_Word),
        ('e_entry', Elf32_Addr),
        ('e_phoff', Elf32_Off),
        ('e_shoff', Elf32_Off),
        ('e_flags', Elf32_Word),
        ('e_ehsize', Elf32_Half),
        ('e_phentsize', Elf32_Half),
        ('e_phnum', Elf32_Half),
        ('e_shentsize', Elf32_Half),
        ('e_shnum', Elf32_Half),
        ('e_shstrndx', Elf32_Half),
    ]

Elf32_Shdr = [
        ('sh_name', Elf32_Word),
        ('sh_type', Elf32_Word),
        ('sh_flags', Elf32_Word),
        ('sh_addr', Elf32_Addr),
        ('sh_offset', Elf32_Off),
        ('sh_size', Elf32_Word),
        ('sh_link', Elf32_Word),
        ('sh_info', Elf32_Word),
        ('sh_addralign', Elf32_Word),
        ('sh_entsize', Elf32_Word),
    ]

Elf32_Rel = [
        ('r_offset', Elf32_Addr),
        ('r_info', Elf32_Word),
    ]

Elf32_Sym = [
        ('st_name', Elf32_Word),
        ('st_value', Elf32_Addr),
        ('st_size', Elf32_Word),
        ('st_info', 'B'),
        ('st_other', 'B'),
        ('st_shndx', Elf32_Half),
    ]

Elf32_Dyn = [
        ('d_tag', Elf32_Sword),
        ('d_val', Elf32_Sword),
    ]

def unpack_from(raw, offset, spec, little_endian=True):
    endianesse = '<' if little_endian else '>'
    names, types = zip(*spec)
    fmt = endianesse + ''.join(types)
    values = struct.unpack_from(fmt, raw, offset)
    return dict(zip(names, values))
