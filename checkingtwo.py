# """def is_prime(n):
#     check if a number is prime
#     if n<=1:
#         return False
#     for i in range(2,int(n**0.5)+1):
#         if n%i==0:
#             return False
# for i in range(2,100):
#     if is_prime(i) and is_prime(i+2):
#         print(f"{i} and {i+2} are twin primes.")"""

# def is_prime(n):
#     if n<1:
#         return False
#     for i in range(2,int(n**0.5)+1):
#         if n%i==0:
#             return False
#         return True
    

# for i in range(2,100):
#     if is_prime(i) and is_prime(i+2):
#         print(f"({i},{i+2})")
    
def is_prime(n):
 if n<=1 :
   return False
 else:
   for i in range (2,int(n**0.5)+1):
    if n%i==0:
        return False
    else:
        return True
for i in range(2,100):
  if is_prime (i) and is_prime(i+2):
     print(f"({i} ,{i+2} )")
 
