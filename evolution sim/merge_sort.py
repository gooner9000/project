def merge_sort(lst, key = lambda x: x):
    if len(lst) <= 1:
        return lst
    left = lst[:len(lst)/2]
    right = lst[len(lst)/2:]
    left = merge_sort(left)
    right = merge_sort(right)

    return merge(left,right,key)

l=merge_sort([(1,2),(0,1)],lambda x: x[0])
l=l[::-1]
print(l)
def merge(left, right,key):
    l=r=0
    while l<len(left) and r<len(right):
        if key(left[l]) < key(right[r]):
