from collections import namedtuple
### APRIORI #####
# to check improvement uncomment lines 20-26
#Improvement implemented is transaction reduction
import pandas as pd
def frequent_itemsets(database, min_supp):
    database = pd.read_csv(database, sep=", ", header=None)
    L1= gen_freq1set(database.values.tolist(),min_supp)
    Itemset_List=[]
    Itemset_List.append(L1)
    set_num=1
    RowList= database.values.tolist()
    for li in Itemset_List:
        rowCount = 0
        Candidate_k= Apriori_Gen(li,set_num)
        set_num=set_num+1
        Candidate_count={}
        for rows in RowList:#RowList:
            #candidate k is a list of k-itemsets
            T_Candidates=Transaction_candidate(Candidate_k,rows)
            #Improvement : Transaction reduction
            # if  len(T_Candidates)==0:
            #
            #     RowList.pop(rowCount)
            #
            # rowCount = rowCount + 1


            for candidate in T_Candidates:
                Contains, val= tupleSet_contains(Candidate_count,candidate)
                if Contains:

                    increase = val
                    Candidate_count.update({tuple(candidate):increase+1})

                else:
                    Candidate_count.update({tuple(candidate): 1})
        L_itemset= {}
        for key,value in Candidate_count.items():
            if value >= min_supp:
                L_itemset.update({key:value})
        if not len(L_itemset)== 0:
            Itemset_List.append(L_itemset)
        print(L_itemset)
        Candidate_count.clear()
    return Itemset_List

#checks equal tuples

def tupleSet_contains(Tuple_set,candidate):
    for tuples in Tuple_set.keys():
        check = True
        tuple_list= list(tuples)
        for item in candidate:
            if not tuple_list.__contains__(item):
                check = False
        if check:
            return True, Tuple_set[tuples]
    return False,None


#choose the candidates in the transaction
#candidate(list of k-itemsets) and transaction(a list) are both list
def Transaction_candidate(candidate,transaction):
    t_candidates=[]

    for itemset in candidate:
        in_transaction = False
        for item in itemset:
            if not item in transaction:
                in_transaction=False

                break
            in_transaction=True
        if in_transaction:
            t_candidates.append(itemset)
    return t_candidates

def gen_freq1set(data,min_supp):
    Itemset={}

    #Going over each row/ transaction
    for row in data:

        #Going over each item in the row
        for i in row:

            #checking if the item is part of the itemset dictionary
            if not Itemset.keys().__contains__((i,)):
                tuple_i= (i,)
                Itemset[tuple_i]=1
            else:
                tuple_i2= (i,)
                Itemset[tuple_i2]=Itemset[tuple_i2]+1
    L_itemset={}
    for key, value in Itemset.items():
        if value >= min_supp:
            L_itemset.update({key: value})
    return L_itemset
#is given a set of k-1 itemset
#itemset is dictionary with tuples of items as the key, and its frequency as values
def Apriori_Gen(Freq_set,set_num):
    print(set_num)
    count=0
    SetComparison = []
    #keys are tuples
    for keys in Freq_set:
        SetComparison.append(list(keys))
    CandidateList=[]
    for itemsets in SetComparison:
        count=count+1
        #iterationg over the comparison itemsets; ommiting the main itemset and the ones before
        for i in SetComparison: #range(count,len(SetComparison)-1):
#Problem: there is a high run time to iterate over the whole Data
#It selects one of the Itemset and then iterates over the rest of the itemset to join candidates to form k+1 candidate sets
           # iteration over the elements of the itemset
           # x is each item/element
             union= set(itemsets) | set(i)
             if len(union)== set_num+1 and set(itemsets) != set(i):
                 if set_num<=1:
                     CandidateList.append(list(union))
                     continue
                 #if not CandidateList.__contains__(union) and \
                 if not has_infrequent_subsets(list(union),SetComparison) and not contains(CandidateList,list(union)):
                     CandidateList.append(list(union))

    return CandidateList
#finds the k-1 sized subsets
def Subset (Itemset):
    #will contain each subset in teh form of a list
    Subset_list=[]
    for i in range(len(Itemset)-1,0,-1):
        new_subset = []
        for count in range(0,i):
            new_subset.append(Itemset[count])
        for rest_count in range(i+1,len(Itemset)):
            new_subset.append(Itemset[rest_count])
        Subset_list.append(new_subset.copy())
        del new_subset[:]
    new_subset_last = []
    for x in range(1,len(Itemset)):
        new_subset_last.append(Itemset[x])
    Subset_list.append(new_subset_last)
    return Subset_list

#contains will determine if a list is present in the List of lists
def contains(Mega_List,list):
    if Mega_List == None:
        return False
    for li in Mega_List:
        In_it= True
        for ele in list:
            if not li.__contains__(ele):
                In_it=False
                break
        if In_it:
            return True
    return False

def has_infrequent_subsets(Candidate_set,LkItemset):
    Candidate_subset= Subset(Candidate_set)
    #print(Candidate_subset)
    contain = False
    for sub in Candidate_subset:
        if not contains(LkItemset,sub):
            #will send true
            contain= True
            break
    return contain



###### FP- GROWTH #########

class Node (object):
    def __init__(self,tree,item,count=1):
        self.tree=tree
        self.item=item
        self.children={}
        self.count=count
        self.parent=None
        self.neighbour=None

    def add_child(self,object):
        if not object.item in self.children:
            self.children[object.item]= object
            object.parent=self

    def find_Node (self,P):
        try:
            return self.children[P]
        except KeyError:
            return None



    def increase(self):
        self.count+=1
    def children(self):
        return tuple(self.children.itervalues())

    def root(self):
        return self.item is None and self.count is None
    def neighbor(self):
        return self.neighbour
    def neighbor(self,value):
        self.neighbour=value
class Tree(object):

    Route= namedtuple('Route','head tail')
    def __init__(self):
        self.root= Node(self,None,None)
        self.routes= {}
    def root(self):
        return self.root

    def insert(self,Plist):
        top = self.root
        for ele in Plist:
            Node_insert= top.find_Node(ele)
            if Node_insert:
                Node_insert.increase()
            else:
                Node_insert=Node(self,ele)
                top.add_child(Node_insert)
                self.update_route(Node_insert)

            top=Node_insert

    def items(self):
        for item in iter(self.routes.keys()):
            yield (self.nodes(item),item)

    def nodes (self,item):
        try:
            node= self.routes[item][0]
        except KeyError:
            return
        while node:
            yield node
            node =node.neighbour

    def update_route(self,object):

        try:
            route = self.routes[object.item]
            route[1].neighbour = object
            self.routes[object.item]=self.Route(route[0],object)
        except KeyError:
            self.routes[object.item]= self.Route(object,object)

    def prefix_route(self,item):
        def collect_route(FPnode):
            route_path=[]

            while FPnode and not FPnode.root():
                route_path.append(FPnode)
                FPnode=FPnode.parent
            route_path.reverse()
            return route_path
        return (collect_route(FPnode)for FPnode in self.nodes(item))



#sorts the freqset in order of their frequencies
def sort (L1_Dict):
    SortedList=[]
    hKey,Hvalue= None,0
    while len(L1_Dict)>0:
        for key,value in L1_Dict.items():
            if value > Hvalue:
                hKey,Hvalue=key,value
        SortedList.append(hKey)
        del L1_Dict[hKey]
        Hvalue=0
    return SortedList
#Checks if the 1 itemset is in a given row


def InTransaction(L1_Dict, row):
    In_transaction={}
    for key,values in L1_Dict.items():
        list(key)
        if row.__contains__(key[0]):
            In_transaction[key[0]]=values
    return In_transaction
#another tree that keeps track of the conditional pattern base
def conditional_tree(path):

    C_tree= Tree()
    items= []
    condition_item=None
    for a_path in path:
        if condition_item is None:
            condition_item=a_path[-1].item
        top_Node=C_tree.root

        for FP_node in a_path:
            new_node=top_Node.find_Node(FP_node.item)
            #to add a new node if the node does not exist in this tree
            if not new_node:
                items.append(FP_node.item)
                count = FP_node.count if FP_node.item==condition_item else 0
                new_node= Node(top_Node,FP_node.item,count)
                top_Node.add_child(new_node)
                C_tree.update_route(new_node)
            top=new_node

    for path_1 in C_tree.prefix_route(condition_item):
        count= path_1[-1].count
        for FP_node1 in reversed(path_1[:-1]):
            FP_node1.count+=count

    return C_tree


# Forming the tree
def Form_Growth_Tree(database,min_supp):
    df = pd.read_csv(database, sep=", ", header=None)
    L1 = gen_freq1set(df.values.tolist(), min_supp)
    MasterTree= Tree()
    for rows in df.values.tolist():
        Candidates_Inrows= InTransaction(L1,rows)
        Sorted_Itemset= sort(Candidates_Inrows)
        MasterTree.insert(Sorted_Itemset)

    def Path_with_suffix(tree, suffix):
        for node, item in tree.items():
            supp= sum(FPnode.count for FPnode in node)
            if supp>= min_supp and item not in suffix:

                Chosen_List= [item]+ suffix
                yield (Chosen_List,supp)
                condition_tree= conditional_tree(tree.prefix_route(item))
                for suf in Path_with_suffix(condition_tree, Chosen_List):
                    yield suf


    for itemset in Path_with_suffix(MasterTree,[]):
        yield itemset

def Partioning (Dataset, n,min_sup ):
    df = pd.read_csv(Dataset, sep=", ", header=None)
    df_splited= pd.np.array_split(df,n)
    for d in df_splited:
        frequent_itemsets(d,min_sup)


#Partioning("UCI_Dataset.txt",10)
#Uncomment to check Apriori
print(frequent_itemsets("UCI_Dataset.txt",0.4*32561))




#Uncomment to check FP_growth
# result = []
# for itemset,support in Form_Growth_Tree("UCI_Dataset.txt",0.2*32561):
#      result.append((itemset,support))
#
# for itemset, support in result:
#     print( str(itemset)+ ' '+ str(support))







