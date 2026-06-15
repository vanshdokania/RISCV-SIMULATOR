import sys
def read_file(file):
    data=[]
    with open(file,"r") as f:
        for line in f:
            data.append(line.strip())
    return data

register_value= {
    "x0": "0",  "x1": "0",  "x2": "380", "x3": "0",  "x4": "0",  "x5": "0",  "x6": "0",  "x7": "0",
    "x8": "0",  "x9": "0",  "x10": "0",  "x11": "0", "x12": "0", "x13": "0", "x14": "0", "x15": "0",
    "x16": "0", "x17": "0", "x18": "0",  "x19": "0", "x20": "0", "x21": "0", "x22": "0", "x23": "0",
    "x24": "0", "x25": "0", "x26": "0",  "x27": "0", "x28": "0", "x29": "0", "x30": "0", "x31": "0"
}

bin_to_reg= {
    "00000": "x0",  "00001": "x1",  "00010": "x2",  "00011": "x3",  "00100": "x4",  "00101": "x5",  "00110": "x6",  "00111": "x7",
    "01000": "x8",  "01001": "x9",  "01010": "x10", "01011": "x11", "01100": "x12", "01101": "x13", "01110": "x14", "01111": "x15",
    "10000": "x16", "10001": "x17", "10010": "x18", "10011": "x19", "10100": "x20", "10101": "x21", "10110": "x22", "10111": "x23",
    "11000": "x24", "11001": "x25", "11010": "x26", "11011": "x27", "11100": "x28", "11101": "x29", "11110": "x30", "11111": "x31"
}

stack_mem= {
    "0x00000100": "0", "0x00000104": "0", "0x00000108": "0", "0x0000010C": "0", "0x00000110": "0", "0x00000114": "0", "0x00000118": "0", "0x0000011C": "0",
    "0x00000120": "0", "0x00000124": "0", "0x00000128": "0", "0x0000012C": "0", "0x00000130": "0", "0x00000134": "0", "0x00000138": "0", "0x0000013C": "0",
    "0x00000140": "0", "0x00000144": "0", "0x00000148": "0", "0x0000014C": "0", "0x00000150": "0", "0x00000154": "0", "0x00000158": "0", "0x0000015C": "0",
    "0x00000160": "0", "0x00000164": "0", "0x00000168": "0", "0x0000016C": "0", "0x00000170": "0", "0x00000174": "0", "0x00000178": "0", "0x0000017C": "0"
}

data_mem= {
    "0x00010000": "0", "0x00010004": "0", "0x00010008": "0", "0x0001000C": "0", "0x00010010": "0", "0x00010014": "0", "0x00010018": "0", "0x0001001C": "0",
    "0x00010020": "0", "0x00010024": "0", "0x00010028": "0", "0x0001002C": "0", "0x00010030": "0", "0x00010034": "0", "0x00010038": "0", "0x0001003C": "0",
    "0x00010040": "0", "0x00010044": "0", "0x00010048": "0", "0x0001004C": "0", "0x00010050": "0", "0x00010054": "0", "0x00010058": "0", "0x0001005C": "0",
    "0x00010060": "0", "0x00010064": "0", "0x00010068": "0", "0x0001006C": "0", "0x00010070": "0", "0x00010074": "0", "0x00010078": "0", "0x0001007C": "0"
}

def instructions(pc, instruction):
    instruc = instruction[pc]
    func3 = instruc[17:20]
    opcode= instruc[25:32] 

    if func3 == "000" and opcode== "0110011":
        if instruc[0:7] == "0000000":
            return "add"
        elif instruc[0:7] == "0100000":
            return "sub"
    elif func3 == "101" and opcode== "0110011":
        return "srl"
    elif func3 == "010" and opcode== "0110011":
        return "slt"
    elif func3 == "111" and opcode== "0110011":
        return "and"
    elif func3 == "110" and opcode== "0110011":
        return "or"
    elif func3 == "000" and opcode== "0010011":
        return "addi"
    elif func3 == "010" and opcode== "0000011":
        return "lw"
    elif func3 == "000" and opcode== "1100111":
        return "jalr"
    elif func3 == "010" and opcode== "0100011":
        return "sw"
    elif func3 == "000" and opcode== "1100011":
        return "beq"
    elif func3 == "001" and opcode== "1100011":
        return "bne"
    elif func3 == "100" and opcode== "1100011":
        return "blt"
    elif opcode== "1101111":
        return "jal"
    else:
        return -1

def create_instr(instr_list):
    a={}
    pc = 0
    for instruction in instr_list:
        a[pc] = instruction
        pc += 4
    return a

def dec_to_bin(num):
    num = int(num)
    if num < 0:
        binary_result = format((1 << 32) + num, "032b")
    else:
        binary_result = format(num, "032b")
    return binary_result

def format_register_values(pc, register_map):
    output_string = "0b" + dec_to_bin(pc) + " "
    register_counter = 2
    for register_key, register_value in register_map.items():
        if register_counter == 4:
            output_string += "0b" + dec_to_bin(register_value) + " "
            register_counter = 1
        else:
            output_string += "0b" + dec_to_bin(register_value) + " "
            register_counter += 1

    output_string += "\n"
    return output_string

def calculate_twos_complement(binary_string):
    bit_count = len(binary_string)
    integer_value = int(binary_string, 2)

    if binary_string[0] == '1':
        integer_value -= 2 ** bit_count
    return integer_value

def convert_decimal_to_hex(decimal_value):
    hex_string = format(decimal_value & 0xFFFFFFFF, '08x')
    hex_string = "0x" + hex_string
    return hex_string

def lw_instr(instruc):
    destination_register = bin_to_reg[instruc[20:25]]
    source_register1 = bin_to_reg[instruc[12:17]]
    immediate_value = calculate_twos_complement(instruc[0:12])

    memory_address_integer = int(register_value[source_register1]) + immediate_value
    memory_address = convert_decimal_to_hex(memory_address_integer)
    if memory_address in data_mem:
        data_from_memory = data_mem[memory_address]
    else:
        data_from_memory = stack_mem[memory_address]
    register_value[destination_register] = data_from_memory
    register_value["x0"] = "0"
    return

def jalr_instr(pc, instruc):
    destination_register = bin_to_reg[instruc[20:25]]
    return_address = pc + 4
    register_value[destination_register] = str(return_address)
    register_value["x0"] = "0"
    return

def jalr_instr_jump(pc, instruc):
    source_register1 = bin_to_reg[instruc[12:17]]
    immediate_value = calculate_twos_complement(instruc[0:12])
    final_pc = int(register_value[source_register1]) + immediate_value
    final_pc_string = dec_to_bin(final_pc)
    final_pc_string = final_pc_string[:31] + "0"
    final_pc_value = calculate_twos_complement(final_pc_string)
    return final_pc_value

def sw_instr(instruc):
    source_register2 = bin_to_reg[instruc[7:12]]
    source_register1 = bin_to_reg[instruc[12:17]]
    immediate_part1 = instruc[0:7]
    immediate_part2 = instruc[20:25]
    immediate_value = calculate_twos_complement(immediate_part1 + immediate_part2)

    memory_address_integer = int(register_value[source_register1]) + immediate_value
    memory_address = convert_decimal_to_hex(memory_address_integer)

    if memory_address in data_mem:
        data_mem[memory_address] = register_value[source_register2]
        register_value["x0"] = "0"
        return

    else:
        stack_mem[memory_address] = register_value[source_register2]
        register_value["x0"] = "0"
        return

def beq_instr(pc, instruc):
    immediate_part12 = instruc[0]
    immediate_part10to5 = instruc[1:7]
    immediate_part4to1 = instruc[20:24]
    immediate_part11 = instruc[24]
    immediate_value = calculate_twos_complement(immediate_part12 + immediate_part11 + immediate_part10to5 + immediate_part4to1 + "0")
    source_register1 = bin_to_reg[instruc[12:17]]
    source_register2 = bin_to_reg[instruc[7:12]]

    if register_value[source_register1] == register_value[source_register2]:
        pc += immediate_value
        register_value["x0"] = "0"
        return pc
    else:
        register_value["x0"] = "0"
        return pc + 4

def bne_instr(pc, instruc):
    immediate_part12 = instruc[0]
    immediate_part10to5 = instruc[1:7]
    immediate_part4to1 = instruc[20:24]
    immediate_part11 = instruc[24]
    immediate_value = calculate_twos_complement(immediate_part12 + immediate_part11 + immediate_part10to5 + immediate_part4to1 + "0")
    source_register1 = bin_to_reg[instruc[12:17]]
    source_register2 = bin_to_reg[instruc[7:12]]

    if register_value[source_register1] != register_value[source_register2]:
        pc += immediate_value
        register_value["x0"] = "0"
        return pc
    else:
        register_value["x0"] = "0"
        return pc + 4

def blt_instr(pc, instruc):
    immediate_part12 = instruc[0]
    immediate_part10to5 = instruc[1:7]
    immediate_part4to1 = instruc[20:24]
    immediate_part11 = instruc[24]
    immediate_value = calculate_twos_complement(immediate_part12 + immediate_part11 + immediate_part10to5 + immediate_part4to1 + "0")
    source_register1 = bin_to_reg[instruc[12:17]]
    source_register2 = bin_to_reg[instruc[7:12]]

    if register_value[source_register1] < register_value[source_register2]:
        pc += immediate_value
        register_value["x0"] = "0"
        return pc
    else:
        register_value["x0"] = "0"
        return pc + 4

def jal_instr(pc, instruc):
    immediate_part20 = instruc[0]
    immediate_part19to12 = instruc[12:18]
    immediate_part11 = instruc[11]
    immediate_part10to1 = instruc[1:11]
    immediate_value = calculate_twos_complement(immediate_part20 + immediate_part19to12 + immediate_part11 + immediate_part10to1)
    destination_register = bin_to_reg[instruc[20:25]]
    return_address = pc + 4
    register_value[destination_register] = str(return_address)
    register_value["x0"] = "0"
    final_pc_string = dec_to_bin(immediate_value + pc)
    final_pc_string = final_pc_string[:31] + "0"
    final_pc_value = calculate_twos_complement(final_pc_string)
    return final_pc_value

def handle_instruction_error():
    print("error: instruction not found")

if len(sys.argv) != 3:
    print("Usage: python Simulator.py <input_file> <output_file>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

executing = []
instr_list = read_file(input_file)

instruction_memory = create_instr(instr_list)

