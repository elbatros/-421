ROOT = 'root'
MANUFACTURER = 'manufacturer'
FAMILY = 'family'
MODEL = 'model'
PROD_ID = 'product_name'
OTHER = 'other'

class Node(object):

    def __init__(self, name, level):
        '''Initialize Node Object'''
        #can be of type str or [str]
        self.name = name
        self.children = []
        #the dictionary field that this node relates to
        self.level = level
    
    def getChildren(self):
        '''Return list of children Nodes'''
        return self.children

    def setChild(self, child):
        '''Add child to list of children Nodes'''
        self.children.append(child)

    def getLevel(self):
        '''Return dictionary field this node relates to'''
        return self.level

    def getName(self):
        '''Return name of this node'''
        return self.name

    def inChildren(self, s):
        '''Return node if str, s, matches any of the names
        of the child nodes, or, the first item in the name of
        a child node, return None otherwise'''
        for n in self.children:
            if n.getLevel() != MODEL:
                if n.getName() == s:
                    return n
            else:
                if n.getName()[0] == s:
                    return n
                
        return None
        
    def nextLevel(self, d):
        '''Return the level that is one below, this nodes
        current level'''
        level_dict = {
            ROOT: MANUFACTURER,
            MANUFACTURER: FAMILY,
            FAMILY: MODEL,
            MODEL: PROD_ID,
            PROD_ID: None,
        }

        return level_dict[self.level]

class Tree(object):

    def __init__(self):
        '''Initialize Tree Object'''
        self.root = Node('root', ROOT)

    def getRoot(self):
        '''Return the root node of this Tree'''
        return self.root

    def populate(self, d, n):
        '''Accept a product dictionary and populate the
        tree with nodes'''
        if n.nextLevel(d) != None:
            cur_node = n.inChildren(d[n.nextLevel(d)])
            #if node is already present, traverse further into tree
            if cur_node:
                self.populate(d, cur_node)
            #if node is not present, create node and traverse further
            else: 
                cur_node = Node(d[n.nextLevel(d)], n.nextLevel(d))
                n.setChild(cur_node)
                self.populate(d, cur_node)

    def search(self, title_list, manu):
        '''Return product_name if the title_list and manu match a
        path in the tree'''
        #check if manu matches manufacturer
        search_node = self.root.inChildren(manu)
        if search_node:
            #check if family matches any str in title_list
            search_node = self.searchFamily(search_node, title_list)
            if search_node:
                #check if model matches any subset in title_list
                search_node = self.searchModel(search_node, title_list)
                if search_node:
                    #return the singular product_name for this path
                    return search_node.getChildren()[0].getName()

        return None

    def searchFamily(self, node, title_list):
        '''Return family level node, if family name is present in node's
        children'''
        for word in title_list:
            new_node = node.inChildren(word)
            if new_node:
                return new_node

        #check if this manufacturer node has an 'other' family node
        new_node = node.inChildren(OTHER)
        return new_node

    def searchModel(self, node, title_list):
        '''Return model level node, if model name is present as a subset
        of title_list, return None otherwise'''
        for i in range(len(title_list)):
            #check if first element of every name matches any item
            new_node = node.inChildren(title_list[i])
            if new_node:
                tally = 0
                #if name is found, check if the following items in node
                #name match the following items in title_list
                if len(title_list) > i + len(new_node.getName()) - 1:
                    for j in range(len(new_node.getName())):
                        if title_list[i + j] == new_node.getName()[j]:
                            tally += 1
                    #all elements in node are matched
                    if tally == len(new_node.getName()):
                        return new_node

        return None
