# Sortable-Challenge
A solution to the matching problem presented by Sortable, as an option for job applicants.

### To Run This Program:
Clone this repository and run `python sortable.py`

### Output:
This program will return a file `results.txt` containing all the product names, with their corresponding matched listings, on separate lines. All products are present in the results file, so products with no matches are represented with an `[]` in their listings field.

### A Little Bit About My Solution:
I felt that a tree would make the most sense for housing all the product information, since the fields (manufacturer, family, model, product_name) were of a increasing specificity. The height of each node corresponds to which field it is in relation to. This means that all of the lines in `products.txt` only need to be processed once, as nodes are created when they are not already present in the tree.

For matching, I felt it would make sense to remove possible inconsistencies between different listings for the same product, so the field names and listings are all lower-case and only contain alphanumeric characters. I felt that the model field may have intentional special characters, so I left it as a list of strings. 

* Manufacturer of Product had to match Manufacturer of Listing 
* Family of Product had to be present in Listing Title (if Family was provided) 
* Model of Product had to be a consecutive subset of the Listing Title string 

Resulting matches were placed in a dictionary, where the key is a product_name, and the value is a list of listings, which were then formatted and placed in the output file.
