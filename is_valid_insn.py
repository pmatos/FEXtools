import subprocess
import sys
import os


def assemble_instruction(instruction):
    # Template for a simple ARM assembly file
    asm_template = """
section .text
global _start

_start:
    %s
    mov r0, #0 // Use exit system call
    ldr r7, =1 // System call number for exit
    svc 0 // Invoke operating system call
"""

    asm_code = asm_template % instruction
    asm_filename = "temp.asm"
    obj_filename = "temp.o"
    executable_filename = "temp"

    try:
        # Write the assembly code to a file
        with open(asm_filename, "w") as f:
            f.write(asm_code)

        # Assemble the ASM file into an object file
        as_command = ["as", asm_filename, "-o", obj_filename]
        subprocess.run(as_command, check=True, stderr=subprocess.PIPE)

        # Link the object file to create an executable
        ld_command = ["ld", obj_filename, "-o", executable_filename]
        subprocess.run(ld_command, check=True)

        return "Success: The instruction assembled correctly."
    except subprocess.CalledProcessError as e:
        return f"Assembly Error: {e}"
    finally:
        # Cleanup: remove temporary files
        for filename in [asm_filename, obj_filename, executable_filename]:
            if os.path.exists(filename):
                os.remove(filename)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python is_valid_insn.py '<assembly_instruction>'")
        sys.exit(1)

    instruction = sys.argv[1]
    result = assemble_instruction(instruction)
    print(result)
