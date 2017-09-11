# Constants

# ELF Identity indices
EI_MAG0 = 0
EI_MAG1 = 1
EI_MAG2 = 2
EI_MAG3 = 3
EI_CLASS = 4
EI_DATA = 5
EI_VERSION = 6
EI_OSABI = 7
EI_PAD = 8
EI_NIDENT = 16

# ELF "magic"
ELFMAG0 = 0x7f
ELFMAG1 = ord('E')
ELFMAG2 = ord('L')
ELFMAG3 = ord('F')

# ELF 32/64
ELFCLASSNONE = 0
ELFCLASS32 = 1
ELFCLASS64 = 2

# ELF endianesse
ELFDATANONE = 0
ELFDATA2LSB = 1
ELFDATA2MSB = 2

# ELF version
EV_NONE = 0
EV_CURRENT = 1

# ELF file types
ET_NONE = 0
ET_REL = 1
ET_EXEC = 2
ET_DYN = 3
ET_CORE = 4

# Section types
SHT_NULL = 0
SHT_PROGBITS = 1
SHT_SYMTAB = 2
SHT_STRTAB = 3
SHT_RELA = 4
SHT_HASH = 5
SHT_DYNAMIC = 6
SHT_NOTE = 7
SHT_NOBITS = 8
SHT_REL = 9
SHT_SHLIB = 10
SHT_DYNSYM = 11
SHT_NUM = 12

# Section flags
SHF_WRITE = 1 << 0
SHF_ALLOC = 1 << 1
SHF_EXECINSTR = 1 << 2
SHF_MASKPROC = 0xf0000000

# Symbol bind types
STB_LOCAL = 0
STB_GLOBAL = 1
STB_WEAK = 2

# Symbol types
STT_NOTYPE = 0
STT_OBJECT = 1
STT_FUNC = 2
STT_SECTION = 3
STT_FILE = 4
STT_COMMON = 5
STT_TLS = 6

# Special section indices
SHN_UNDEF = 0
SHN_LORESERVE = 0xff00
SHN_LOPROC = 0xff00
SHN_HIPROC = 0xff1f
SHN_ABS = 0xfff1
SHN_COMMON = 0xfff2
SHN_HIRESERVE = 0xffff

# Relocation types (Taken from the official ARM doc "ELF for ARM Architecture")
R_ARM_CALL = 28
R_ARM_JUMP24 = 29

# Dynamic section entry types
DT_NULL = 0
DT_SONAME = 14
