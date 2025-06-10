def generate_masked_eicar():
    # Raw EICAR: X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*
    eicar_parts = [
        "X5O!P%", "@AP[4\\P", "ZX54(P^)", "7CC)7}$EICAR", "-STANDARD", "-ANTIVIRUS", "-TEST", "-FILE!$H+H*"
    ]
    masked = '" + "'.join(eicar_parts)
    script = f'code = "{masked}"\nwith open("eicar.txt", "w") as f:\n\tf.write(code)\nprint("[+] Masked EICAR file written.")'
    output_path = "output/eicar_generator.py"
    with open(output_path, "w") as f:
        f.write(script)
    print(f"[+] Masked EICAR payload saved to {output_path}")
