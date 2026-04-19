from mftool import Mftool

mf = Mftool()
codes = mf.get_scheme_codes()
print(f"Total schemes: {len(codes)}")

# Save all scheme codes and names to a text file
with open('mutual_fund_codes.txt', 'w') as f:
    f.write("Scheme Code\tScheme Name\n")  # Header
    for code, name in codes.items():
        if code != 'Scheme Code':  # Skip the header entry
            f.write(f"{code}\t{name}\n")

print("Mutual fund codes and names saved to mutual_fund_codes.txt")