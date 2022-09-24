def print_simulated_donors(donors, show_n_betas: int = 5):
    print("donor\t\tsignal\t\t" + "\t\t".join([f'beta_{i+1}' for i in range(show_n_betas - 1)]) + "\t\t...")
    for index, donor in enumerate(donors):
        print(f"donor_{number_to_str(index+1, 2)}\t\t{int(donor[0])}\t\t\t" + "\t\t\t".join([number_to_str(round(val, 3), 4) for val in donor[1:show_n_betas]]))


def number_to_str(num, expected_len):
    if len(str(num)) < expected_len:
        return str(num) + "".join([' ' for _ in range(expected_len - len(str(num)))])
    else:
        return str(num)
