import pickle

if __name__ == "__main__":
    with open('tran_res.dat', 'rb') as f:
        dicts = pickle.load(f)
    print("input somethings u want search, CTRL + C to exit")
    
    while True:
        thing = input()
        res = []
        for each_page in dicts:
            lines = each_page['item_list']
            for each_line in range(len(lines)):
                content = lines[each_line]
                if content.find(thing) != -1:
                    res.append((each_page['page'], each_line))
        
        for each_res in res:
            print("occr in page %d line %d" % (each_res[0] + 1, each_res[1] + 1))
