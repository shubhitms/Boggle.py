# Trie.py

class Trie:
    """Trie is the overall header of the data structure. 
    it contains the root node of the TST, from which all the data
    in the TST can be accessed."""
    def __init__(self, char=None):
        self.char = char
        self.left = self.right = self.child = None
        self.flag = False

    @classmethod
    def insert_helper(this, tst, word):
        if word == "": return tst
        char = word[0]
        if tst == None:
            tst = Trie(char)
        elif tst.char == None:
            tst.char = char
        if char == tst.char:
            word = word[1:]
            if word != "": 
                tst.child = this.insert_helper(tst.child, word)
            else: 
                tst.flag = True
        elif char < tst.char:
            tst.left = this.insert_helper(tst.left, word)
        else:
            tst.right = this.insert_helper(tst.right, word)
        return tst

    def insert(self, word):
        return self.insert_helper(self, word)

    def lookup(self, word):
        tst = self
        while tst != None:
            char = word[0]
            if char == tst.char:
                word = word[1:]
                if word == "":
                    if tst.flag:
                        return True
                    break;
                tst = tst.child
            elif char < tst.char:
                tst = tst.left
            else:
                tst = tst.right
        return False

    def isPrefix(self, word):
        tst = self
        while tst != None:
            char = word[0]
            if char == tst.char:
                word = word[1:]
                if word == "":
                    return True
                tst = tst.child
            elif char < tst.char:
                tst = tst.left
            else:
                tst = tst.right
        return False

    def insertDict(self, dic, start=0, stop=None):
        if stop == None:
            stop = len(dic)
        diff = stop - start
        if diff == 1:
            self.insert(dic[start])
        elif diff == 2:
            self.insert(dic[start])
            self.insert(dic[start+1])
        else:
            mid = start + (diff / 2)
            self.insert(dic[mid])
            self.insertDict(dic, mid+1, stop)
            self.insertDict(dic, start, mid)

    def testLookup(self, word, ans):
        print "Testing lookup(", word, ") ==", str(ans)
        self.lookup(word) == ans
        print "Passed!"

    def testLookup(self, word, ans):
        print "Testing lookup(", word, ") ==", str(ans)
        self.lookup(word) == ans
        print "Passed!"
    
    def testIsPrefix(self, word, ans):
        print "Testing isPrefix(", word, ") ==", str(ans)
        self.isPrefix(word) == ans
        print "Passed!"

def createDictionary(file):
    dic = [w.strip() for w in file]

    tst = Trie()
    tst.insertDict(dic, 0, len(dic))

    #Testing
    print "Testing tst.lookup!"
    tst.testLookup("hello", True)
    tst.testLookup("there", True)
    tst.testLookup("abandonments", True)
    tst.testLookup("skjvnskfjv", False)
    tst.testLookup("zzz", True)

    print "Testing tst.prefix"
    tst.testIsPrefix("abando", True)
    tst.testIsPrefix("initi", True)
    tst.testIsPrefix("hi", True)
    tst.testIsPrefix("zyz", False)

    return tst


f = open('dict.txt', 'r')
T = createDictionary(f)






        
        