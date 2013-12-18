# Trie.py

class Trie:
    """Trie is the overall header of the data structure. 
    it contains the root node of the TST, from which all the data
    in the TST can be accessed."""
    def __init__(self, char=None):
        self.char = char
        self.left = self.right = self.child = None
        self.flag = False

    # Recursively inserts a single word into the tst. Each character of
    # the word is inserted as a single element in a sorted tree of characters.
    # Algorithmic complexity: O(log(k)), where k is the length of the word.
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

    # Looks for a word in the tst each character at a time. Once the 
    # end of the word is reached, the flag is checked. A string of characters
    # in a TST is only a word if the last character is flagged.
    # Algorithmic complexity: O(log(k)), where k is the length of the word.
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

    # Checks whether the word is a prefix of another word in the 
    # dictionary. 
    # Algorithmic complexity: O(log(k)), where k is the length of the prefix.
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

    # Inserts multiple words into the tst from a list dic. This is used 
    # to insert all the words of a dictionary into the TST in order to 
    # populate it in the beginning of the program. This function uses a 
    # binary insertion algorithm to create a balanced tree.
    # Contract: dic is sorted. By inserting the middle word of dic first
    # each time and recursively calling insertDic on the resulting left
    # and right dic lists, the resulting TST is quite balanced. Also, by 
    # passing in start and stop indices, the same dic list can be passed
    # through the recursive calls as opposed to creating a new smaller dic
    # list each time, saving memory. 
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

    #Functions to test my TST implementation
    def testLookup(self, word, ans):
        print "Testing lookup(", word, ") ==", str(ans)
        self.lookup(word) == ans
        print "Passed!"
    
    def testIsPrefix(self, word, ans):
        print "Testing isPrefix(", word, ") ==", str(ans)
        self.isPrefix(word) == ans
        print "Passed!"

def createDictionary(file, test=False):
    dic = [w.strip() for w in file]

    tst = Trie()
    tst.insertDict(dic, 0, len(dic))

    #Testing
    if test:
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


#Open dictionary text file and create TST dictionary.
f = open('dict.txt', 'r')
T = createDictionary(f)






        
        