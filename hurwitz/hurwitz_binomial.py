from hurwitz import HurwitzQuaternion

# Predefined labeled half and whole quaternions
labeled_halfs = {
    "α": HurwitzQuaternion(-1, 1, 1, -1, True),
    "β": HurwitzQuaternion(-1, 1, -1, 1, True),
    "γ": HurwitzQuaternion(1, -1, 1, -1, True),
    "δ": HurwitzQuaternion(1, -1, -1, 1, True),
    "ε": HurwitzQuaternion(1, 1, -1, -1, True),
    "ζ": HurwitzQuaternion(1, 1, 1, -1, True),
    "η": HurwitzQuaternion(1, 1, 1, 1, True),
    "θ": HurwitzQuaternion(-1, -1, -1, -1, True),
    "i": HurwitzQuaternion(-1, 1, 1, 1, True),
    "κ": HurwitzQuaternion(1, -1, 1, 1, True),
    "λ": HurwitzQuaternion(1, 1, -1, 1, True),
    "μ": HurwitzQuaternion(1, 1, 1, -1, True),
    "ν": HurwitzQuaternion(-1, -1, -1, 1, True),
    "ξ": HurwitzQuaternion(-1, -1, 1, -1, True),
    "ο": HurwitzQuaternion(-1, 1, -1, -1, True),
    "π": HurwitzQuaternion(1, -1, -1, -1, True)
}

labeled_wholes = {
    "א": HurwitzQuaternion(1, 0, 0, 0, False),
    "-א": HurwitzQuaternion(-1, 0, 0, 0, False),
    "V": HurwitzQuaternion(0, 1, 0, 0, False),
    "-V": HurwitzQuaternion(0, -1, 0, 0, False),
    "L": HurwitzQuaternion(0, 0, 1, 0, False),
    "-L": HurwitzQuaternion(0, 0, -1, 0, False),
    "E": HurwitzQuaternion(0, 0, 0, 1, False),
    "-E": HurwitzQuaternion(0, 0, 0, -1, False)
}

negative_labeled_wholes = {
    "-א": HurwitzQuaternion(-1, 0, 0, 0, False),
    "-V": HurwitzQuaternion(0, -1, 0, 0, False),
    "-L": HurwitzQuaternion(0, 0, -1, 0, False),
    "-E": HurwitzQuaternion(0, 0, 0, -1, False)
}

positive_labeled_wholes = {
    "א": HurwitzQuaternion(1, 0, 0, 0, False),
    "V": HurwitzQuaternion(0, 1, 0, 0, False),
    "L": HurwitzQuaternion(0, 0, 1, 0, False),
    "E": HurwitzQuaternion(0, 0, 0, 1, False),
}

def check_decompose_binomial(hq):
    """
    Decomposes a quaternion into its whole and half parts and checks against the labeled quaternions.
    """
    binomial = hq.decompose_binomial()
    whole = binomial[0]
    half = binomial[1]
    whole_key = None
    half_key = None

    # Check if whole part is in labeled_wholes
    for key, value in labeled_wholes.items():
        if whole == value:
            whole_key = key
            break

    # Check if half part is in labeled_halfs
    for key, value in labeled_halfs.items():
        if half == value:
            half_key = key
            break

    # Return result based on what parts matched
    if whole_key and half_key:
        return f"{whole_key} ⦻ {half_key}"
    elif half_key and not whole_key:
        return half_key
    elif whole_key and not half_key:
        return whole_key
    else:
        return "η"  # Default class if no match found

def find_equivalence_classes():
    """
    Iterates through combinations of half and whole quaternions, checking for equivalence classes.
    """
    classes = {}

    # Iterate over all half and whole quaternion combinations
    for half_key, half in labeled_halfs.items():
        for whole_key, whole in labeled_wholes.items():
            result = check_decompose_binomial(half + whole)
            print(f"{whole_key} ⦻ {half_key}: {result}")

            # Check if the result is already a known class
            if result in classes:
                classes[result].append((whole_key, half_key))
            else:
                # Check if it exists in any other class' value set
                found = False
                for class_name, class_members in classes.items():
                    if result in class_members:
                        class_members.append((whole_key, half_key))
                        found = True
                        break

                # If not found, create a new class
                if not found:
                    classes[result] = [(whole_key, half_key)]

    return classes

# Run the class detection and print the results
classes = find_equivalence_classes()


# Output the class groupings
print("\nEquivalence Classes:")
for class_name, class_members in classes.items():
    print(f"{class_name}: {class_members}")



print(len(classes.keys()))

def find_half_unit_classes():
    """
    Finds and prints all classes where only half units are involved (i.e., no whole quaternion components).
    """
    half_unit_classes = {}
    binary_classes = classes.copy()

    for class_name, class_value in classes.items():
        if class_name in labeled_halfs.keys():
            half_unit_classes[class_name] = class_value
            binary_classes.pop(class_name)


    return half_unit_classes, binary_classes

# Run the function to find and print the half unit classes
half_unit_classes = find_half_unit_classes()[0]
binary_classes = find_half_unit_classes()[1]

print("\nHalf Unit Classes:")
for class_name, class_members in half_unit_classes.items():
    print(f"{class_name}: {class_members}")
print(len(half_unit_classes.keys()))


def find_single_half_unit_classes():
    single_classes = {}

    for single_class_name, class_value in classes.items():
        # Ensure the class has exactly one element
        if len(class_value) == 1:
           
            single_classes[single_class_name] = class_value
            

    return single_classes

print("\n binary Classes:")
for class_name, class_members in binary_classes.items():
    print(f"{class_name}: {class_members}")

print(len(binary_classes.keys()))

binary_classes_aleph = binary_classes.copy()
# remove all classes with aleph
for key in list(binary_classes.keys()):
    if 'א' in key:
        del binary_classes_aleph[key]

print("\n binary Classes without א:")
for class_name, class_members in binary_classes_aleph.items():
    print(f"{class_name}: {class_members}")

print(len(binary_classes_aleph.keys()))

print("Specials: ")
print(classes['η'])
print(classes["π"])

combo_mode = binary_classes_aleph.copy()
combo_mode['η'] = classes['η']
combo_mode['π'] = classes['π']

print(len(combo_mode.keys()))

print("\n Combo Class items with V in the items:")

V_subclasses = []
for key, value in combo_mode.items():
    valid = False
    for item in value:
        if 'V' in item:
            #print(item)
            valid = True
    if valid:
        print("Adding class: ", key, " - ", value)
        V_subclasses.append(value)

print(len(V_subclasses))

E_subclasses = []
print("\n Combo Class items with E in the items:")
for key, value in combo_mode.items():
    valid = False
    for item in value:
        if 'E' in item:
            #print(item)
            valid = True
    if valid:
        print("Adding class: ", key, " - ", value)
        E_subclasses.append(value)

print(len(E_subclasses))


L_subclasses = []
print("\n Combo Class items with L in the items:")
for key, value in combo_mode.items():
    valid = False
    for item in value:
        if 'L' in item:
            #print(item)
            valid = True
    if valid:
        print("Adding class: ", key, " - ", value)
        L_subclasses.append(value)

print(len(L_subclasses))

whole_to_binary = {
    'א' : (0,0),
    'V' : (0,1),
    'L' : (1,0),
    'E' : (1,1)
}

half_to_binary = {
    'α' : (0,1,1,0),
    'β' : (0,1,0,1),
    'γ' : (1,0,1,0),
    'δ' : (1,0,0,1),
    'ε' : (1,1,0,0),
    'ζ' : (0,0,1,1),
    'η' : (1,1,1,1),
    'θ' : (0,0,0,0),
    'i' : (0,1,1,1),
    'κ' : (1,0,1,1),
    'λ' : (1,1,0,1),
    'μ' : (1,1,1,0),
    'ν' : (0,0,0,1),
    'ξ' : (0,0,1,0),
    'ο' : (0,1,0,0),
    'π' : (1,0,0,0)
}

def binary_to_qubit(binary_tuple):
    whole, half = binary_tuple
    hq_whole = whole_to_binary[whole] if whole else (0,0)
    hq_half = half_to_binary[half] if half else (0,0,0,0)
    return (hq_whole, hq_half)

print("V Subclass Qubits:")
vquibi = []
for subclass in V_subclasses:
    print("Subclass: ", subclass)
    for binary in subclass:
        if 'V' in binary:
            quibit = binary_to_qubit(binary)
            vquibi.append(quibit)
            print(quibit)

print(len(vquibi))

equibi = []
print("E Subclass Qubits:")
for subclass in E_subclasses:
    print("Subclass: ", subclass)
    for binary in subclass:
        if 'E' in binary:
            quibit = binary_to_qubit(binary)
            equibi.append(quibit)
            print(quibit)

print(len(equibi))

lquibi = []
print("L Subclass Qubits:")
for subclass in L_subclasses:
    print("Subclass: ", subclass)
    for binary in subclass:
        if 'L' in binary:
            quibit = binary_to_qubit(binary)
            lquibi.append(quibit)
            print(quibit)

print(len(lquibi))

for class_name, class_members in combo_mode.items():
    if len(class_members) == 1 and class_name != 'π':
        print(class_name) 
    else:
        pstring = ""
        for member in class_members:
            pstring += str(member[0])+ " ⦻ " + str(member[1]) + ", "
        if len(class_members) != 2:
            print(f"{class_name},", pstring)
        else:
            print(pstring)


a="""
V ⦻ α - ((0, 1), (0, 1, 1, 0))
L ⦻ α - ((1, 0), (0, 1, 1, 0))
V ⦻ β - ((0, 1), (0, 1, 0, 1))
E ⦻ β - ((1, 1), (0, 1, 0, 1))
L ⦻ γ - ((1, 0), (1, 0, 1, 0))
E ⦻ δ - ((1, 1), (1, 0, 0, 1))
V ⦻ ε - ((0, 1), (1, 1, 0, 0))
V ⦻ ζ, V ⦻ μ, - i
L ⦻ ζ, L ⦻ μ, - j 
V ⦻ η - ((0, 1), (1, 1, 1, 1))
L ⦻ η - ((1, 0), (1, 1, 1, 1))
E ⦻ η - ((1, 1), (1, 1, 1, 1))
V ⦻ i - ((0, 1), (0, 1, 1, 1))
L ⦻ i - ((1, 0), (0, 1, 1, 1))
E ⦻ i - ((1, 1), (0, 1, 1, 1))
L ⦻ κ - ((1, 0), (1, 0, 1, 1))
E ⦻ κ - ((1, 1), (1, 0, 1, 1))
V ⦻ λ - ((0, 1), (1, 1, 0, 1))
E ⦻ λ - ((1, 1), (1, 1, 0, 1))
E ⦻ ν - ((1, 1), (0, 0, 0, 1)) - [k - 1/2(1+i+j-k)]
L ⦻ ξ - ((1, 0), (0, 0, 1, 0)) - [j - 1/2(1+i-j+k)]
V ⦻ ο - ((0, 1), (0, 1, 0, 0)) - [i - 1/2(1-i+j+k)]
η, E ⦻ ζ, א ⦻ i, V ⦻ κ, L ⦻ λ, E ⦻ μ, L ⦻ ν, E ⦻ ξ, - 1/2(1+i+j+k)
π, א ⦻ θ,  - e - 1/2(1-i-j-k)
"""

gen_i = HurwitzQuaternion(1, 1, 1, -1, True) + HurwitzQuaternion(0, 1, 0, 0, False)
gen_j = HurwitzQuaternion(1, 1, 1, -1, True) + HurwitzQuaternion(0, 0, 1, 0, False)
gen_half = HurwitzQuaternion(1, 1, 1, -1, True) + HurwitzQuaternion(0, 0, 0, 1, False)
gen_e = HurwitzQuaternion(1, -1, -1, -1, True)

print(repr(gen_i))
print(repr(gen_j))
print(repr(gen_half))
print(repr(gen_e))

print(repr(gen_i + gen_e))
print(repr(gen_e + gen_i))


# (i + 1/2(-1+i+j-k))(1/2(1-i-j-k)) = V x α * pi =  1/2(i+1-k+j) + j = L x mu = j
# V x nu = 1/2(1+i+j+k) + i
# (1/2(1+i+j+k) + i) x 1/2(1+i+j+k) = 1/2(i-1+k-j) + 2 * (1/2(-1+i+j+k))

print(repr(HurwitzQuaternion(1, 1, 1, 1, True)**2)) #= 2 * (1/2(-1+i+j+k))


print((HurwitzQuaternion(1, 1, 1, 1, True)**3)) #= 2 * (1/2(-1+i+j+k))

print(repr(HurwitzQuaternion(1, 1, 1, 1, True)**4)) #= 2 * (1/2(-1+i+j+k))