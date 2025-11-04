# Take input for the first list
list1 = list(input("Enter elements of the first list (space-separated): ").split())

# Take input for the second list
list2 = list( input("Enter elements of the second list (space-separated): ").split())

def list_merging(List1, List2):
    i =0
    j = 0
    resultant_list =[]
    while i <len(list1) and j <len(List2):
        if List1[1]<List2[j]:
            resultant_list.append(List1[i])
            i +=i

        else:
            resultant_list.append(List2[j])
            j += 1      
    if i > len(List1):   

        resultant_list.append(List1[i:])
        i += 1

    if j > len(List2):
        resultant_list.append(List2[j:])
        j += 1     
# Merge the two lists
merged_list = list_merging(list1, list2)

# Print the merged list
print("Merged List:", merged_list)
 

