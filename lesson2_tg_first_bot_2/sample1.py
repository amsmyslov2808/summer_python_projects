a = int(input("введите а: "))
print(f"a = {a}")

if a >= 0 and a <= 10:
    print("good")
elif a >= 11 and a <= 25:
    print("good on 75%")
elif a >= 26 and a <= 50:
    print("good on 50%")
else:
    print("bad")

print("programm is over")
