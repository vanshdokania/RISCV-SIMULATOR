import sys

# Changed variable names to be more descriptive but kept same structure
register_name_mapping = {
    '00000': 'zero', '00001': 'ra',   '00010': 'sp',   '00011': 'gp',
    '00100': 'tp',   '00101': 't0',   '00110': 't1',   '00111': 't2',
    '01000': 's0',   '01001': 's1',   '01010': 'a0',   '01011': 'a1',
    '01100': 'a2',   '01101': 'a3',   '01110': 'a4',   '01111': 'a5',
    '10000': 'a6',   '10001': 'a7',   '10010': 's2',   '10011': 's3',
    '10100': 's4',   '10101': 's5',   '10110': 's6',   '10111': 's7',
    '11000': 's8',   '11001': 's9',   '11010': 's10',  '11011': 's11',
    '11100': 't3',   '11101': 't4',   '11110': 't5',   '11111': 't6'
}

# Memory configuration with more verbose names
STARTING_MEMORY_ADDRESS = 65536   # 0x10000
ENDING_MEMORY_ADDRESS = 65660     # 0x1007C
MEMORY_ADDRESS_INCREMENT = 4

# Changed to use more basic data structure and initialization
memory_data_storage = {}
for memory_location in range(STARTING_MEMORY_ADDRESS, ENDING_MEMORY_ADDRESS + 1, MEMORY_ADDRESS_INCREMENT):
    memory_data_storage[f"0x{memory_location:08X}"] = 0

# Register configuration with more basic initialization
NUMBER_OF_BITS_IN_REGISTER = 32
INITIAL_VALUE_FOR_STACK_POINTER = 0x17C  # 380 in decimal

# Changed to use more basic initialization
register_current_values = {}
for register_code in register_name_mapping.keys():
    register_current_values[register_code] = '0' * NUMBER_OF_BITS_IN_REGISTER

# Initialize stack pointer separately for clarity
stack_pointer_binary = bin(INITIAL_VALUE_FOR_STACK_POINTER)[2:].zfill(NUMBER_OF_BITS_IN_REGISTER)
register_current_values['00010'] = stack_pointer_binary

# Instruction definitions with more verbose structure
instruction_definitions = {
    # R-type instructions
    '0110011': {
        '0000000': {
            '000': 'add',  # Add
            '010': 'slt',  # Set less than
            '101': 'srl',  # Shift right logical
            '110': 'or',   # Bitwise OR
            '111': 'and'   # Bitwise AND
        },
        '0100000': {
            '000': 'sub'   # Subtract
        }
    },
    # I-type instructions
    '0000011': {'': {'010': 'lw'}},     # Load word
    '0010011': {'': {'000': 'addi'}},   # Add immediate
    '1100111': {'': {'000': 'jalr'}},   # Jump and link register
    # S-type instructions
    '0100011': {'': {'010': 'sw'}},     # Store word
    # B-type instructions
    '1100011': {
        '': {
            '000': 'beq',  # Branch equal
            '001': 'bne',  # Branch not equal
            '100': 'blt'   # Branch less than
        }
    },
    # J-type instructions
    '1101111': {'': 'jal'}  # Jump and link
}

def generate_state_snapshot(current_program_counter, memory_range_to_show=None):
    """Generate state snapshot including memory context - made more verbose"""
    snapshot_output = f"0b{current_program_counter:032b}"
    
    # Add register values in order
    sorted_register_codes = sorted(register_current_values.keys())
    for register_code in sorted_register_codes:
        snapshot_output += ' ' + f'0b{register_current_values[register_code]}'
    
    snapshot_output += '\n'
    
    # Add memory contents if requested
    if memory_range_to_show is not None:
        snapshot_output += "Memory Contents:\n"
        memory_start_address = memory_range_to_show[0]
        memory_end_address = memory_range_to_show[1]
        
        for memory_address in range(memory_start_address, memory_end_address + 1, 4):
            memory_address_hex = f"0x{memory_address:08X}"
            if memory_address_hex in memory_data_storage:
                memory_value = memory_data_storage[memory_address_hex]
                snapshot_output += f"{memory_address_hex}: 0b{memory_value:032b}\n"
    
    return snapshot_output

def validate_R_type_instruction(opcode_part, funct7_part, funct3_part):
    """Validate R-type instruction fields - made more verbose with checks"""
    try:
        if opcode_part not in instruction_definitions:
            return False
            
        if funct7_part not in instruction_definitions[opcode_part]:
            return False
            
        if funct3_part not in instruction_definitions[opcode_part][funct7_part]:
            return False
            
        return True
    except KeyError:
        return False

def validate_S_type_instruction(opcode_part, funct3_part):
    """Validate S-type instruction fields - made more verbose"""
    try:
        if opcode_part not in instruction_definitions:
            return False
            
        if '' not in instruction_definitions[opcode_part]:
            return False
            
        if funct3_part not in instruction_definitions[opcode_part]['']:
            return False
            
        return True
    except KeyError:
        return False

def validate_I_type_instruction(opcode_part, funct3_part):
    """Validate I-type instruction fields - made more verbose"""
    try:
        if opcode_part not in instruction_definitions:
            return False
            
        if '' not in instruction_definitions[opcode_part]:
            return False
            
        if funct3_part not in instruction_definitions[opcode_part]['']:
            return False
            
        return True
    except KeyError:
        return False

def validate_B_type_instruction(opcode_part, funct3_part):
    """Validate B-type instruction fields - made more verbose"""
    try:
        if opcode_part not in instruction_definitions:
            return False
            
        if '' not in instruction_definitions[opcode_part]:
            return False
            
        if funct3_part not in instruction_definitions[opcode_part]['']:
            return False
            
        return True
    except KeyError:
        return False

def validate_J_type_instruction(opcode_part):
    """Validate J-type instruction - made more verbose"""
    try:
        if opcode_part not in instruction_definitions:
            return False
            
        if '' not in instruction_definitions[opcode_part]:
            return False
            
        return True
    except KeyError:
        return False

# Instruction type mapping with more verbose names
instruction_type_categories = {
    '0110011': 'R',  # R-type
    '0000011': 'I',  # I-type (load)
    '0010011': 'I',  # I-type (immediate)
    '1100111': 'I',  # I-type (jalr)
    '0100011': 'S',  # S-type
    '1100011': 'B',  # B-type
    '1101111': 'J'   # J-type
}

def perform_sign_extension(binary_string_value, total_bits=32):
    """Sign extension with more basic implementation"""
    if len(binary_string_value) >= total_bits:
        return binary_string_value[-total_bits:]
    
    sign_bit = binary_string_value[0]
    extension_bits = sign_bit * (total_bits - len(binary_string_value))
    return extension_bits + binary_string_value

def compare_signed_binary_values(binary_value1, binary_value2):
    """Compare signed values with more basic implementation"""
    if len(binary_value1) != 32 or len(binary_value2) != 32:
        raise ValueError("Both values must be 32-bit binary strings")
        
    for char in binary_value1 + binary_value2:
        if char not in ['0', '1']:
            raise ValueError("Binary strings can only contain 0s and 1s")
    
    # Convert to integers
    int_value1 = int(binary_value1, 2)
    int_value2 = int(binary_value2, 2)
    
    # Handle two's complement negative numbers
    if binary_value1[0] == '1':
        int_value1 -= (1 << 32)
    if binary_value2[0] == '1':
        int_value2 -= (1 << 32)
        
    return int_value1 < int_value2

def convert_binary_string_to_integer(binary_string):
    """Binary to integer conversion with more basic implementation"""
    if not isinstance(binary_string, str):
        raise TypeError("Input must be a string")
        
    if not binary_string:
        return 0
        
    for char in binary_string:
        if char not in ['0', '1']:
            raise ValueError("Binary string can only contain 0s and 1s")
    
    if binary_string[0] == '0':
        return int(binary_string, 2)
    else:
        # For negative numbers in two's complement
        positive_part = int(binary_string[1:], 2)
        return -((1 << (len(binary_string)-1)) - positive_part)

def execute_R_type_instruction(opcode_part, funct7_part, source_register2, source_register1, funct3_part, destination_register):
    """Execute R-type instruction with more basic implementation"""
    operation_name = instruction_definitions[opcode_part][funct7_part][funct3_part]
    
    # Get register values as integers
    source1_value = int(register_current_values[source_register1], 2)
    source2_value = int(register_current_values[source_register2], 2)
    
    result = 0
    
    if operation_name == 'add':
        result = source1_value + source2_value
    elif operation_name == 'sub':
        result = source1_value - source2_value
    elif operation_name == 'slt':
        if compare_signed_binary_values(register_current_values[source_register1], register_current_values[source_register2]):
            result = 1
        else:
            result = 0
    elif operation_name == 'srl':
        shift_amount = int(register_current_values[source_register2][-5:], 2)
        result = source1_value >> shift_amount
    elif operation_name == 'or':
        result = source1_value | source2_value
    elif operation_name == 'and':
        result = source1_value & source2_value
    else:
        return
    
    # Store result in destination register (32-bit)
    register_current_values[destination_register] = format(result & 0xFFFFFFFF, '032b')

def execute_S_type_instruction(opcode_part, immediate_value, source_register1, source_register2, funct3_part, program_counter_value):
    """Execute S-type instruction with more basic implementation"""
    if instruction_definitions[opcode_part][''][funct3_part] == 'sw':
        # Sign extend immediate value
        extended_immediate = perform_sign_extension(immediate_value)
        immediate_number = convert_binary_string_to_integer(extended_immediate)
        
        # Calculate memory address
        base_address = int(register_current_values[source_register1], 2)
        memory_address = base_address + immediate_number
        
        # Store value in memory
        memory_address_hex = f"0x{memory_address:08X}"
        value_to_store = int(register_current_values[source_register2], 2)
        memory_data_storage[memory_address_hex] = value_to_store
    
    return program_counter_value + 4

def execute_J_type_instruction(opcode_part, immediate_value, destination_register, program_counter_value):
    """Execute J-type instruction with more basic implementation"""
    if instruction_definitions[opcode_part][''] == 'jal':
        # Sign extend and adjust immediate value
        extended_immediate = perform_sign_extension(immediate_value)
        immediate_number = convert_binary_string_to_integer(extended_immediate)
        
        # Save return address (PC+4)
        return_address = program_counter_value + 4
        register_current_values[destination_register] = format(return_address, '032b')
        
        # Calculate new PC
        return program_counter_value + immediate_number
    
    return program_counter_value

def execute_I_type_instruction(immediate_value, source_register1, funct3_part, destination_register, opcode_part, program_counter_value, instruction_string):
    """Execute I-type instruction with more basic implementation"""
    # Sign extend immediate value
    extended_immediate = perform_sign_extension(immediate_value)
    immediate_number = convert_binary_string_to_integer(extended_immediate)
    
    operation_name = instruction_definitions[opcode_part][''][funct3_part]
    
    if operation_name == 'addi':
        # Get source register value
        source_value = int(register_current_values[source_register1], 2)
        
        # Perform addition
        result = source_value + immediate_number
        
        # Store result (32-bit)
        register_current_values[destination_register] = format(result & 0xFFFFFFFF, '032b')
        return program_counter_value + 4

    elif operation_name == 'jalr':
        # Calculate new PC
        base_address = int(register_current_values[source_register1], 2)
        new_pc_value = (base_address + immediate_number) & ~1
        
        # Save return address
        return_address = program_counter_value + 4
        register_current_values[destination_register] = format(return_address, '032b')
        
        return new_pc_value

    elif operation_name == 'lw':
        # Calculate memory address
        base_address = int(register_current_values[source_register1], 2)
        memory_address = base_address + immediate_number
        
        # Load value from memory
        memory_address_hex = f"0x{memory_address:08X}"
        loaded_value = memory_data_storage[memory_address_hex]
        
        # Store in destination register
        register_current_values[destination_register] = format(loaded_value, '032b')
        return program_counter_value + 4

def execute_B_type_instruction(opcode_part, immediate_value, source_register1, source_register2, program_counter_value, funct3_part):
    """Execute B-type instruction with more basic implementation"""
    # Immediate value needs to be multiplied by 2 (add 0 at end)
    adjusted_immediate = immediate_value + '0'
    
    # Sign extend
    extended_immediate = perform_sign_extension(adjusted_immediate)
    immediate_number = convert_binary_string_to_integer(extended_immediate)
    
    operation_name = instruction_definitions[opcode_part][''][funct3_part]
    
    if operation_name == 'beq':
        if register_current_values[source_register1] == register_current_values[source_register2]:
            if immediate_number == 0:
                return "HALT"
            else:
                return program_counter_value + immediate_number
    elif operation_name == 'bne':
        if register_current_values[source_register1] != register_current_values[source_register2]:
            return program_counter_value + immediate_number
    elif operation_name == 'blt':
        value1 = convert_binary_string_to_integer(register_current_values[source_register1])
        value2 = convert_binary_string_to_integer(register_current_values[source_register2])
        if value1 < value2:
            return program_counter_value + immediate_number

    return program_counter_value + 4

def generate_full_state_dump(current_pc_value, show_memory=False, memory_address_range=None):
    """Generate full state dump with more basic implementation"""
    state_lines = []
    
    # Add PC line
    pc_line = f"PC: 0b{current_pc_value:032b} (0x{current_pc_value:08X})"
    state_lines.append(pc_line)
    
    # Add register values
    register_line_parts = []
    for register_code in sorted(register_current_values.keys()):
        register_line_parts.append(f'0b{register_current_values[register_code]}')
    register_line = "Registers: " + ' '.join(register_line_parts)
    state_lines.append(register_line)
    
    # Optionally add memory contents
    if show_memory:
        state_lines.append("\nMemory Contents:")
        
        if memory_address_range is None:
            mem_start = STARTING_MEMORY_ADDRESS
            mem_end = ENDING_MEMORY_ADDRESS
        else:
            mem_start, mem_end = memory_address_range
            
        for mem_address in range(mem_start, mem_end + 1, 4):
            mem_address_hex = f"0x{mem_address:08X}"
            if mem_address_hex in memory_data_storage:
                mem_value = memory_data_storage[mem_address_hex]
                mem_line = f"{mem_address_hex}: 0b{mem_value:032b}"
                state_lines.append(mem_line)
    
    return '\n'.join(state_lines) + '\n'

def simulate_program(instruction_list, output_file_path):
    """Main simulation function with more basic implementation"""
    simulation_output = ""

    # Clean and prepare instructions
    cleaned_instructions = []
    for instruction_line in instruction_list:
        stripped_line = instruction_line.strip()
        if stripped_line:
            cleaned_instructions.append(stripped_line)
    
    # Load instructions into memory
    instruction_memory_map = {}
    for instruction_index in range(len(cleaned_instructions)):
        instruction_address = instruction_index * 4
        instruction_memory_map[instruction_address] = cleaned_instructions[instruction_index]
    
    # Initialize program counter
    pc_value = 0
    
    # Main simulation loop
    while pc_value in instruction_memory_map:
        previous_pc_value = pc_value
        current_instruction = instruction_memory_map[pc_value]
        
        # Extract opcode
        opcode_value = current_instruction[-7:]
        
        if opcode_value not in instruction_definitions:
            raise ValueError("Invalid opcode in instruction")
            
        instruction_type = instruction_type_categories[opcode_value]
        
        if instruction_type == 'R':
            # R-type instruction
            funct7_value = current_instruction[:7]
            rs2_value = current_instruction[7:12]
            rs1_value = current_instruction[12:17]
            funct3_value = current_instruction[17:20]
            rd_value = current_instruction[20:25]
            
            if not validate_R_type_instruction(opcode_value, funct7_value, funct3_value):
                raise ValueError("Invalid R-type instruction")
                
            if rs1_value not in register_name_mapping:
                raise ValueError("Invalid source register 1")
                
            if rs2_value not in register_name_mapping:
                raise ValueError("Invalid source register 2")
                
            if rd_value not in register_name_mapping:
                raise ValueError("Invalid destination register")
                
            execute_R_type_instruction(opcode_value, funct7_value, rs2_value, rs1_value, funct3_value, rd_value)
            pc_value += 4

        elif instruction_type == 'I':
            # I-type instruction
            immediate_value = current_instruction[:12]
            rs1_value = current_instruction[12:17]
            funct3_value = current_instruction[17:20]
            rd_value = current_instruction[20:25]
            
            if not validate_I_type_instruction(opcode_value, funct3_value):
                raise ValueError("Invalid I-type instruction")
                
            if rs1_value not in register_name_mapping:
                raise ValueError("Invalid source register")
                
            pc_value = execute_I_type_instruction(immediate_value, rs1_value, funct3_value, rd_value, opcode_value, pc_value, current_instruction)

        elif instruction_type == 'S':
            # S-type instruction
            immediate_value = current_instruction[:7] + current_instruction[20:25]
            rs2_value = current_instruction[7:12]
            rs1_value = current_instruction[12:17]
            funct3_value = current_instruction[17:20]
            
            if not validate_S_type_instruction(opcode_value, funct3_value):
                raise ValueError("Invalid S-type instruction")
                
            if rs1_value not in register_name_mapping:
                raise ValueError("Invalid source register 1")
                
            if rs2_value not in register_name_mapping:
                raise ValueError("Invalid source register 2")
                
            pc_value = execute_S_type_instruction(opcode_value, immediate_value, rs1_value, rs2_value, funct3_value, pc_value)

        elif instruction_type == 'B':
            # B-type instruction
            immediate_value = current_instruction[0] + current_instruction[24] + current_instruction[1:7] + current_instruction[20:24]
            rs2_value = current_instruction[7:12]
            rs1_value = current_instruction[12:17]
            funct3_value = current_instruction[17:20]
            
            if not validate_B_type_instruction(opcode_value, funct3_value):
                raise ValueError("Invalid B-type instruction")
                
            if rs1_value not in register_name_mapping:
                raise ValueError("Invalid source register 1")
                
            if rs2_value not in register_name_mapping:
                raise ValueError("Invalid source register 2")
                
            old_pc_value = pc_value
            pc_value = execute_B_type_instruction(opcode_value, immediate_value, rs1_value, rs2_value, pc_value, funct3_value)
            
            if pc_value == "HALT":
                simulation_output += f"0b{format(previous_pc_value, '032b')} "
                for reg_code in register_current_values.keys():
                    simulation_output += f"0b{register_current_values[reg_code]} "
                simulation_output += "\n"
                break

        elif instruction_type == 'J':
            # J-type instruction
            immediate_value = current_instruction[0] + current_instruction[12:20] + current_instruction[11] + current_instruction[1:11] + '0'
            rd_value = current_instruction[20:25]
            
            if not validate_J_type_instruction(opcode_value):
                raise ValueError("Invalid J-type instruction")
                
            if rd_value not in register_name_mapping:
                raise ValueError("Invalid destination register")
                
            pc_value = execute_J_type_instruction(opcode_value, immediate_value, rd_value, pc_value)
        
        else:
            raise ValueError("Unknown instruction type")

        # Generate output line
        if pc_value == 'HALT':
            simulation_output += "0b" + format(int(previous_pc_value), "032b") + " "
        else:
            simulation_output += "0b" + format(int(pc_value), "032b") + " "
        
        # Ensure zero register stays zero
        register_current_values['00000'] = "0" * 32
        
        # Add register values to output
        for reg_code in register_current_values.keys():
            simulation_output += "0b" + register_current_values[reg_code] + " "
        
        simulation_output += "\n"

    # Add memory dump to output
    for mem_address in range(65536, 65660 + 1, 4):
        mem_address_hex = f"0x{mem_address:08X}"
        simulation_output += f"{mem_address_hex}:0b{format(memory_data_storage[mem_address_hex], '032b')}\n"

    # Write output to file
    with open(output_file_path, "w") as output_file:
        output_file.write(simulation_output.strip())

if __name__ == "__main__":
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    
    with open(input_file_path, "r") as input_file:
        instructions_to_execute = input_file.readlines()
    
    simulate_program(instructions_to_execute, output_file_path)