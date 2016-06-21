#Class for hotel objects
class hotel:
    #Class for each hotel's reservations
    class reservation:
        def __init__(self, name, checkindate, staydays,hname):
            self.name = name
            self.checkindate = checkindate
            self.staydays = staydays
            self.hotelname = hname
    def __init__(self, id, name, stars, noofrooms,rid):
        self.reservations = []
        self.id = int(id)
        self.name = name
        self.stars = stars
        self.nofrooms = noofrooms
        self.rescount = 0
        self.rid = int(rid)
    #Filling reservations for each hotel
    def fillres(self, name, date, days,hname):  # Function to fill the Reservations of the Hotel
        self.reservations.append(hotel.reservation(name, date, days,hname))

        self.rescount += 1
        return
    #Showing all reservations for the hotel
    def showres(self):
        for i in range(0, len(self.reservations)):
            print("Name : ", self.reservations[i].name, "\n")
            print("Checkin Date : ", self.reservations[i].checkindate, "\n")
            print("Days to stay : ", self.reservations[i].staydays, "\n")
    #returning the number of reservations for the hotel
    def numofres(self):
        return len(self.reservations)

#Red Black node class
class rbnode(object):
    def __init__(self, key):
        "Constructor."
        self._key =key
        self._red = False
        self._left = None
        self._right = None
        self._p = None

    #Binding properties into the variables for easier use
    key = property(fget=lambda self: self._key, doc="The node's key")
    red = property(fget=lambda self: self._red, doc="Is the node red?")
    left = property(fget=lambda self: self._left, doc="The node's left child")
    right = property(fget=lambda self: self._right, doc="The node's right child")
    p = property(fget=lambda self: self._p, doc="The node's parent")

    def __str__(self):
        return str(self.key)


    def __repr__(self):
        return str(self.key)

#Red Black tree class
class rbtree(object):

    def __init__(self, create_node=rbnode): #Contructor
        "Otan ftiaxnoume to dentro arxika dimiourgoume ena Nil node to opoio einai h riza tou dentrou"
        self._nil = create_node(key=None)
        self._root = self.nil
        self._create_node = create_node


    root = property(fget=lambda self: self._root, doc="The tree's root node")
    nil = property(fget=lambda self: self._nil, doc="The tree's nil node")

    def search(self, key,calcss, x=None):
        """Auti i sunartisi psaxnei to dentro gia to id pou exei dwthei kai epistrefei
        ena obj ama to vrei i to nill node ama den to vrei"""

        if None == x:
            calcss += 1
            x = self.root
        while x != self.nil and key != x.key:
            calcss += 1
            if key < x.key:
                x = x.left
            else:
                x = x.right


        return x,calcss
    def minimum(self, x=None):
        """Epistrofi tis elaxistis timis se ena dentro rizas x"""
        if None == x:
            x = self.root
        while x.left != self.nil:
            x = x.left
        return x
    def maximum(self, x=None):
        """Epistrofi tis megistis timis se ena dentro rizas x"""
        if None == x:
            x = self.root
        while x.right != self.nil:
            x = x.right

        return x
    def insert_key(self, key):
        "Eisagwgi kleidriou xrisimopoieitai apo tin insert node"
        self.insert_node(self._create_node(key=key))
    def insert_node(self, z):
        "Eisagogi node sto dentro"
        y = self.nil
        x = self.root
        while x != self.nil:
            y = x
            if z.key < x.key:
                x = x.left
            else:
                x = x.right
        z._p = y
        if y == self.nil:
            self._root = z
        elif z.key < y.key:
            y._left = z
        else:
            y._right = z
        z._left = self.nil
        z._right = self.nil
        z._red = True
        self._insert_fixup(z)

    def _insert_fixup(self, z):
        "Zugostathmisi meta tin eisagwgi enos node"
        while z.p.red:
            if z.p == z.p.p.left:
                y = z.p.p.right
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.right:
                        z = z.p
                        self._left_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._right_rotate(z.p.p)
            else:
                y = z.p.p.left
                if y.red:
                    z.p._red = False
                    y._red = False
                    z.p.p._red = True
                    z = z.p.p
                else:
                    if z == z.p.left:
                        z = z.p
                        self._right_rotate(z)
                    z.p._red = False
                    z.p.p._red = True
                    self._left_rotate(z.p.p)
        self.root._red = False

    def _left_rotate(self, x):
        "Aristeri peristrofi"
        y = x.right
        x._right = y.left
        if y.left != self.nil:
            y.left._p = x
        y._p = x.p
        if x.p == self.nil:
            self._root = y
        elif x == x.p.left:
            x.p._left = y
        else:
            x.p._right = y
        y._left = x
        x._p = y

    def _right_rotate(self, y):
        "deksia peristrofi"
        x = y.left
        y._left = x.right
        if x.right != self.nil:
            x.right._p = y
        x._p = y.p
        if y.p == self.nil:
            self._root = x
        elif y == y.p.right:
            y.p._right = x
        else:
            y.p._left = x
        x._right = y
        y._p = x

    def check_invariants(self):
        "Gurizei True ean to dentro einai ontos RB tree"

        def is_red_black_node(node):
            "Checking if a node has both left and right children. If False then it's not Rb"
            if (node.left and not node.right) or (node.right and not node.left):
                return 0, False

            #If it's a leaf and it's red then return False
            if not node.left and not node.right and node.red:
                return 0, False

            #If it's red. Check the children to be black. If they are not return False.
            if node.red and node.left and node.right:
                if node.left.red or node.right.red:
                    return 0, False

            #Check the whole tree if the black node count is balanced
            if node.left and node.right:

                #If the childrens parents are not correct return Falce
                if self.nil != node.left and node != node.left.p:
                    return 0, False
                if self.nil != node.right and node != node.right.p:
                    return 0, False

                #Run itself over the children to get the whole tree
                left_counts, left_ok = is_red_black_node(node.left)
                if not left_ok:
                    return 0, False
                right_counts, right_ok = is_red_black_node(node.right)
                if not right_ok:
                    return 0, False

                # Check if the children counts are ok
                if left_counts != right_counts:
                    return 0, False
                return left_counts, True
            else:
                return 0, True

        num_black, is_ok = is_red_black_node(self.root)
        return is_ok and not self.root._red

def test_tree(t, keys):
    "Eisagwgi stoixeiw sto dentro"
    for i, key in enumerate(keys):
        t.insert_key(key)





class TrieNode:
    #Arxikopoiisi metavlitwn
    def __init__(self):
        self.val = None
        self.pointers={}
        self.reservations = []

class Trie:

    def __init__(self):
        self.root = TrieNode()
        self.calcs = 0

    #Eisagwgi stoixeioy sto trie
    def insert(self, word,reservation):

        self.rec_insert(word, self.root,reservation)
        return

    #Anadromiki eisagwgh stoixeiou sto dentro
    def rec_insert(self, word, node,reservation):
        if word[:1] not in node.pointers:
            newNode=TrieNode()
            newNode.val=word[:1]
            node.pointers[word[:1]]=newNode
            self.rec_insert(word, node,reservation)
        else:
            nextNode = node.pointers[word[:1]]
            if len(word[1:])==0:
                nextNode.pointers[' ']='__END__'
                nextNode.reservations.append(reservation)
                return
            return self.rec_insert(word[1:], nextNode,reservation)


    #Anazhthsh stoixeiou sto dentro
    def search(self, word,prt):
        self.calcs = 0
        if len(word)==0:
            return False
        return self.rec_search(word,self.root,prt)

    #Anadromikh anazitisi kai upologismos kinisewn
    def rec_search(self, word, node,prt):

        if word[:1] not in node.pointers:
            self.calcs += 1
            return False
        else:
            nextNode = node.pointers[word[:1]]
            self.calcs += 1
            if len(word[1:])==0:

                if ' ' in nextNode.pointers:
                    self.calcs+=1
                    if prt:
                        self.printres(nextNode)
                    return True
                else:
                    return False
            return self.rec_search(word[1:],nextNode,prt)
    #Ektiposi kratisis gia TO TRIE
    def printres(self,tnode):
        print("=======Reservations Found:=======")
        print("     For Mr/Ms : " + tnode.reservations[0].name + " :\n\n")
        print("/===================================")
        for it in range(0,len(tnode.reservations)):
            print("|  Hotel : ",tnode.reservations[it].hotelname)
            print("|  Checkin Date : ",tnode.reservations[it].checkindate)
            print("|  Days to stay : ",tnode.reservations[it].staydays)
            print("|===================================" )

#Sunartisi dimiourgias tou trie tree
def make_trie(hotels):
    trie = Trie()

    for it in range(0,len(hotels)):
        for j in range(0,len(hotels[it].reservations)):
             reserv = hotels[it].reservations[j]
             name = hotels[it].reservations[j].name
             trie.insert(name,reserv)
    return trie