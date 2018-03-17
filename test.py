
N = int(input())

# Get the array
numArray1 = list(map(int, input().split()))
numArray2 = list(map(int, input().split()))

sumArray = [
    num1 + num2
    for i, num1 in enumerate(numArray1)
    for j, num2 in enumerate(numArray2)
    if i == j
]

# Write the logic here:


# Print the sumArray
for element in sumArray:
    print(element, end=" ")

print("")


