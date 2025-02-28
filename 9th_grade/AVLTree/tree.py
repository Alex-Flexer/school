class Tree:
    def __init__(self, key) -> None:
        self.key = key
        self.right = None
        self.left = None

    def __str__(self) -> str:
        return ' '.join(map(str, self.get_preorder_traversal()))

    def add(self, key):
        if not self.left and not self.right:
            if key < self.key:
                self.left = Tree(key)
            elif key > self.key:
                self.right = Tree(key)
            else:
                raise KeyError(f"Node by key {key} is already in tree")
        else:
            if self.left and key < self.key:
                self.left.add(key)
            elif not self.left and key < self.key:
                self.left = Tree(key)
            elif self.right and key > self.key:
                self.right.add(key)
            elif not self.right and key > self.key:
                self.right = Tree(key)
            else:
                raise KeyError(f"Node by key {key} is already in tree")
        return self

    def pop(self, key):
        if key < self.key:
            self.left = self.left.pop(key)
        elif key > self.key:
            self.right = self.right.pop(key)
        else:
            if not self.left and not self.right:
                return None
            elif not self.left:
                self.key = self.right.key
                self.right = self.right.right
                self.left = self.right.left if self.right else None
            elif not self.right:
                self.key = self.left.key
                self.right = self.left.left
                self.left = self.left.right
            else:
                small_sub_tree = self.right
                while small_sub_tree.left:
                    small_sub_tree = small_sub_tree.left
                new_key = small_sub_tree.key
                small_sub_tree.right = self.pop(new_key)
                self.key = new_key
        return self

    def rotate_left(self, key=-1) -> None:
        if key < self.key and key != -1:
            self.left.rotate_right(key)
        elif key > self.key and key != -1:
            self.right.rotate_right(key)
        else:
            self.key, self.left.key = self.left.key, self.key
            self.right, self.left.left, self.left.right =\
                self.left.left, self.left.right, self.right
            # r -> l.l
            # l.l -> l.r
            # l.r -> r

            self.left, self.right = self.right, self.left

    def rotate_right(self, key=-1) -> None:
        if key < self.key and key != -1:
            self.left.rotate_right(key)
        elif key > self.key and key != -1:
            self.right.rotate_right(key)
        else:
            self.key, self.right.key = self.right.key, self.key
            self.left, self.right.right, self.right.left =\
                self.right.right, self.right.left, self.left
            # l -> r.r
            # r.r -> r.l
            # r.l -> l

            self.left, self.right = self.right, self.left

    def find_node(self, key: int):
        if key < self.key:
            return self.left.find_node(key)
        elif key > self.key:
            return self.right.find_node(key)
        elif key == self.key:
            return self
        else:
            return -1

    def get_high(self,  key=-1, start_node=None):
        if not start_node:
            if key == -1:
                start_node = self
            else:
                start_node = self.find_node(key)

        def find_max_distance_leaf(node: Tree):
            mx_dist = 0
            if node.left:
                mx_dist = max(mx_dist, find_max_distance_leaf(node.left) + 1)
            if node.right:
                mx_dist = max(mx_dist, find_max_distance_leaf(node.right) + 1)
            return mx_dist

        return find_max_distance_leaf(start_node)

    def balance_node(self, key=-1):
        if key == -1:
            node = self
        else:
            node = self.find_node(key)
        l_high = node.left.get_high(start_node=node.left) if node.left else -1
        r_high = node.right.get_high(start_node=node.right) if node.right else -1
        if abs(r_high - l_high) <= 1:
            return

        if l_high > r_high:
            l_r_high = node.left.right.get_high() if node.left and node.left.right else -1
            l_l_high = node.left.left.get_high() if node.left and node.left.left else -1
            if l_r_high > l_l_high:
                node.left.rotate_right()
            node.rotate_left()
        else:
            r_l_high = node.right.left.get_high() if node.right and node.right.left else -1
            r_r_high = node.right.right.get_high() if node.right and node.right.right else -1
            if r_l_high > r_r_high:
                node.right.rotate_left()
            node.rotate_right()
        node.full_tree_balance()

    def full_tree_balance(self):
        if not self.left and not self.right:
            return
        if self.left:
            self.left.full_tree_balance()
        if self.right:
            self.right.full_tree_balance()
        self.balance_node()

    def get_preorder_traversal(self) -> list:
        res = []
        if self.left:
            res += self.left.get_preorder_traversal()
        res.append(self.key)
        if self.right:
            res += self.right.get_preorder_traversal()
        return res
