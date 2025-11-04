
st = str(input("Enter a string "))
result = ""
for i in range(len(st)):
    if i % 2 == 0:
        result += st[i]
                  


print("result after removing  characters at odd palces")        
print(result)         