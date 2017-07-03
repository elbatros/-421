import json, re, time
from node import Node, Tree, FAMILY, OTHER, PROD_ID, MODEL, MANUFACTURER

#regex for non-alphanumeric characters
NON_ALPHA_NUM = '[^A-Za-z0-9]+'

def reformat(line):
    '''Accept a dictionary, line, and format it and return it so that
    it can be accepted by Tree Class'''
    #make family mandatory field by adding OTHER to dicts that don't have it
    if not (FAMILY in line):
        line[FAMILY] = OTHER;

    for attr in line.keys():
        #leave product_name with original formatting
        if attr != PROD_ID: 
            new_attr = reformatList(line[attr])
            #leave model as a list of strings
            if attr != MODEL:
                #otherwise, create a single string of lowercase
                #alphanumeric characters
                new_attr = ''.join(new_attr)
            line[attr] = new_attr
    return line

def reformatList(s):
    '''Accept a str, s, and return a list of str, split by alphanumeric
    characters, all lowercase'''
    split = re.split(NON_ALPHA_NUM, s)
    for i in range(len(split)):
        split[i] = split[i].lower()

    return split
if __name__ == '__main__':
    start_time = time.time()
    
    #create a Tree to hold all products, and a dict to hold
    #all matched results
    prod_tree = Tree()
    result_dict = dict()

    total_listings = 0
    matched_listings = 0
    matched_products = 0
    
    file = open('products.txt', 'r', encoding = 'utf-8')

    #add all lines from products.txt to the tree
    for line in file.readlines():
        line = json.loads(line)
        line = reformat(line)
        prod_tree.populate(line, prod_tree.getRoot())
        result_dict[line[PROD_ID]] = []

    file.close()

    file = open('listings.txt', 'r', encoding='utf-8')

    #match all lines from listings.txt to the tree
    for line in file.readlines():
        line = json.loads(line)
        split_title = reformatList(line['title'])
        manu = reformatList(line[MANUFACTURER])
        manu = ''.join(manu)
        match_id = prod_tree.search(split_title, manu)
        #if a product match exists for this listing
        if match_id:
            result_dict[match_id].append(line)
            matched_listings += 1
        total_listings += 1

    file.close()

    file = open('results.txt', 'w', encoding='utf-8')

    #create a separate dict for each match and write it to results file
    #on seperate lines
    for key in result_dict.keys():
        temp_dict = dict()
        temp_dict['product_name'] = key
        temp_dict['listings'] = result_dict[key]
        new_line = json.dumps(temp_dict)
        file.write(new_line + '\n')
        if result_dict[key] != []:
            matched_products += 1

    file.close()

    print('Sortable Challenge Report')
    print('Execution Run Time: %s seconds' % (time.time() - start_time))
    print('Matched %d of %d listings' % (matched_listings, total_listings))
    print('Matched to %d of %d products' % (matched_products, len(result_dict.keys())))
