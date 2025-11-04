#like faf tit etc
name = input("Enter your name:")
name= name.strip()

low = 0
high = len(name) -1
while low < high:
    if name[low]==name[high]:
        low+=1
        high-=1
    else:
        print("It is not anagram")
        break
if low>=high:
    print("IT is anagram")
