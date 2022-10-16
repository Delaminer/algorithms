from fft import multiply

print("Testing out FFT")

# x = 34
# y = 831

x = 1
y = 1

result = multiply(x, y)
expected = x * y

correct = result == expected
print("CORRECT!!!" if correct else "Incorrect...")
print(f"Expected {expected}, got {result}")
