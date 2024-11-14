import heapq
from collections import defaultdict
from rodnmod.thunderstore import getMods

# Step 1: Build a frequency map from your JSON tree (mod list)
def build_frequency_map(mod_list):
    freq_map = defaultdict(int)
    for mod in mod_list:
        freq_map[mod] += 1
    return freq_map

# Step 2: Construct a Huffman Tree
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # For priority queue to compare nodes based on frequency
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_map):
    priority_queue = [Node(char, freq) for char, freq in freq_map.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(priority_queue, merged)

    return priority_queue[0]  # Root of the Huffman tree

# Step 3: Generate Huffman codes from the tree
def generate_huffman_codes(root, code='', huffman_codes=None):
    if huffman_codes is None:
        huffman_codes = {}

    if root:
        if root.char:
            huffman_codes[root.char] = code
        generate_huffman_codes(root.left, code + '0', huffman_codes)
        generate_huffman_codes(root.right, code + '1', huffman_codes)

    return huffman_codes

# Step 4: Encode the mod list using Huffman codes
def encode_mod_list(mod_list, huffman_codes):
    return ''.join(huffman_codes[mod] for mod in mod_list)

# Step 5: Decode the encoded mod list (if needed)
def decode_mod_list(encoded_data, huffman_tree):
    decoded_list = []
    node = huffman_tree
    for bit in encoded_data:
        node = node.left if bit == '0' else node.right
        if node.char:
            decoded_list.append(node.char)
            node = huffman_tree  # Reset to the root
    return decoded_list

# Example usage:
modList = [

]

for mod in getMods():
    modList.append(mod)


# Step 1: Build the frequency map
freq_map = build_frequency_map(modList)

# Step 2: Build the Huffman tree
huffman_tree = build_huffman_tree(freq_map)

# Step 3: Generate Huffman codes
huffman_codes = generate_huffman_codes(huffman_tree)

# Step 4: Encode the mod list
encoded_data = encode_mod_list(modList, huffman_codes)

# Output the Huffman codes and encoded data
print(f"Huffman Codes: {huffman_codes}")
print(f"Encoded Data: {encoded_data}")

# Step 5: Decode the mod list (for verification)
decoded_list = decode_mod_list(encoded_data, huffman_tree)
print(f"Decoded List: {decoded_list}")
