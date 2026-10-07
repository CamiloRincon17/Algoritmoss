"""Implementaciones educativas para estudiar algoritmos.

Ejecutar con: python algoritmos_parcial.py
Solo utiliza la biblioteca estándar de Python.
"""

from collections import deque
from statistics import median
from time import perf_counter


# Cambia estos valores para probar los algoritmos de ordenamiento y búsqueda.
VALUES_TO_TEST = [8, 3, 5, 1, 5, 0]


def bubble_sort(values):
    result = list(values)
    n = len(result)
    for end in range(n - 1, 0, -1):
        swapped = False
        for index in range(end):
            if result[index] > result[index + 1]:
                result[index], result[index + 1] = result[index + 1], result[index]
                swapped = True
        if not swapped:
            break
    return result


def selection_sort(values):
    result = list(values)
    for start in range(len(result) - 1):
        smallest = start
        for index in range(start + 1, len(result)):
            if result[index] < result[smallest]:
                smallest = index
        result[start], result[smallest] = result[smallest], result[start]
    return result


def insertion_sort(values):
    result = list(values)
    for index in range(1, len(result)):
        current = result[index]
        position = index - 1
        while position >= 0 and result[position] > current:
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = current
    return result


def merge_sort(values):
    items = list(values)
    if len(items) <= 1:
        return items

    middle = len(items) // 2
    left = merge_sort(items[:middle])
    right = merge_sort(items[middle:])
    merged = []
    left_index = right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            merged.append(left[left_index])
            left_index += 1
        else:
            merged.append(right[right_index])
            right_index += 1

    merged.extend(left[left_index:])
    merged.extend(right[right_index:])
    return merged


def quick_sort(values):
    result = list(values)

    def partition(low, high):
        pivot = result[high]
        boundary = low
        for index in range(low, high):
            if result[index] <= pivot:
                result[boundary], result[index] = result[index], result[boundary]
                boundary += 1
        result[boundary], result[high] = result[high], result[boundary]
        return boundary

    def sort_range(low, high):
        if low < high:
            pivot_index = partition(low, high)
            sort_range(low, pivot_index - 1)
            sort_range(pivot_index + 1, high)

    sort_range(0, len(result) - 1)
    return result


def radix_sort(values):
    result = list(values)
    if any(not isinstance(value, int) or value < 0 for value in result):
        raise ValueError("radix_sort acepta únicamente enteros no negativos")
    if not result:
        return result

    place = 1
    largest = max(result)
    while largest // place > 0:
        counts = [0] * 10
        output = [0] * len(result)

        for value in result:
            digit = (value // place) % 10
            counts[digit] += 1

        for digit in range(1, 10):
            counts[digit] += counts[digit - 1]

        for value in reversed(result):
            digit = (value // place) % 10
            counts[digit] -= 1
            output[counts[digit]] = value

        result = output
        place *= 10
    return result


class HashTable:
    """Tabla hash educativa con encadenamiento separado para colisiones."""

    def __init__(self, capacity=8):
        if capacity <= 0:
            raise ValueError("capacity debe ser positivo")
        self._buckets = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key):
        return self._buckets[hash(key) % len(self._buckets)]

    def _resize(self):
        old_buckets = self._buckets
        self._buckets = [[] for _ in range(len(old_buckets) * 2)]
        for bucket in old_buckets:
            for key, value in bucket:
                self._bucket(key).append((key, value))

    def put(self, key, value):
        bucket = self._bucket(key)
        for index, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                bucket[index] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._size / len(self._buckets) > 0.75:
            self._resize()

    def get(self, key, default=None):
        for stored_key, value in self._bucket(key):
            if stored_key == key:
                return value
        return default

    def delete(self, key):
        bucket = self._bucket(key)
        for index, (stored_key, _) in enumerate(bucket):
            if stored_key == key:
                del bucket[index]
                self._size -= 1
                return True
        return False

    def __len__(self):
        return self._size


class _SinglyNode:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, value):
        node = _SinglyNode(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1

    def find(self, value):
        current = self.head
        while current is not None:
            if current.value == value:
                return current
            current = current.next
        return None

    def delete(self, value):
        previous = None
        current = self.head
        while current is not None:
            if current.value == value:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                if current is self.tail:
                    self.tail = previous
                self._size -= 1
                return True
            previous, current = current, current.next
        return False

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def __len__(self):
        return self._size


class _DoublyNode:
    def __init__(self, value):
        self.value = value
        self.previous = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, value):
        node = _DoublyNode(value)
        if self.tail is None:
            self.head = self.tail = node
        else:
            node.previous = self.tail
            self.tail.next = node
            self.tail = node
        self._size += 1
        return node

    def find(self, value):
        current = self.head
        while current is not None:
            if current.value == value:
                return current
            current = current.next
        return None

    def delete_node(self, node):
        if node is None:
            return False
        if node.previous is None and node is not self.head:
            return False
        if node.previous is not None and node.previous.next is not node:
            return False
        if node.next is None and node is not self.tail:
            return False
        if node.next is not None and node.next.previous is not node:
            return False
        if node.previous is None:
            self.head = node.next
        else:
            node.previous.next = node.next
        if node.next is None:
            self.tail = node.previous
        else:
            node.next.previous = node.previous
        self._size -= 1
        return True

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.value)
            current = current.next
        return result

    def __len__(self):
        return self._size


class Stack:
    def __init__(self):
        self._items = []

    def push(self, value):
        self._items.append(value)

    def pop(self):
        if not self._items:
            raise IndexError("pop de una pila vacía")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek de una pila vacía")
        return self._items[-1]

    def is_empty(self):
        return not self._items

    def __len__(self):
        return len(self._items)


class Deque:
    """Adaptador mínimo de collections.deque para enseñar ambos extremos."""

    def __init__(self, values=()):
        self._items = deque(values)

    def add_front(self, value):
        self._items.appendleft(value)

    def add_rear(self, value):
        self._items.append(value)

    def remove_front(self):
        if not self._items:
            raise IndexError("remove_front de un deque vacío")
        return self._items.popleft()

    def remove_rear(self):
        if not self._items:
            raise IndexError("remove_rear de un deque vacío")
        return self._items.pop()

    def to_list(self):
        return list(self._items)

    def __len__(self):
        return len(self._items)


class _BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        if self.root is None:
            self.root = _BSTNode(key)
            return
        current = self.root
        while True:
            if key == current.key:
                return
            if key < current.key:
                if current.left is None:
                    current.left = _BSTNode(key)
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = _BSTNode(key)
                    return
                current = current.right

    def search(self, key):
        current = self.root
        while current is not None:
            if key == current.key:
                return current
            current = current.left if key < current.key else current.right
        return None

    def inorder(self):
        result = []

        def visit(node):
            if node is not None:
                visit(node.left)
                result.append(node.key)
                visit(node.right)

        visit(self.root)
        return result


class _AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """Árbol AVL con inserción balanceada, búsqueda y recorrido in-order."""

    @staticmethod
    def _height(node):
        return node.height if node else 0

    @classmethod
    def _update(cls, node):
        node.height = 1 + max(cls._height(node.left), cls._height(node.right))

    @classmethod
    def _rotate_right(cls, root):
        new_root = root.left
        middle = new_root.right
        new_root.right = root
        root.left = middle
        cls._update(root)
        cls._update(new_root)
        return new_root

    @classmethod
    def _rotate_left(cls, root):
        new_root = root.right
        middle = new_root.left
        new_root.left = root
        root.right = middle
        cls._update(root)
        cls._update(new_root)
        return new_root

    @classmethod
    def _insert(cls, node, key):
        if node is None:
            return _AVLNode(key)
        if key < node.key:
            node.left = cls._insert(node.left, key)
        elif key > node.key:
            node.right = cls._insert(node.right, key)
        else:
            return node

        cls._update(node)
        balance = cls._height(node.left) - cls._height(node.right)

        if balance > 1:
            if key > node.left.key:
                node.left = cls._rotate_left(node.left)
            return cls._rotate_right(node)
        if balance < -1:
            if key < node.right.key:
                node.right = cls._rotate_right(node.right)
            return cls._rotate_left(node)
        return node

    def __init__(self):
        self.root = None

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def search(self, key):
        current = self.root
        while current is not None:
            if key == current.key:
                return current
            current = current.left if key < current.key else current.right
        return None

    def inorder(self):
        result = []

        def visit(node):
            if node is not None:
                visit(node.left)
                result.append(node.key)
                visit(node.right)

        visit(self.root)
        return result


def heap_sort(values):
    result = list(values)
    size = len(result)

    def sift_down(root, end):
        while 2 * root + 1 < end:
            child = 2 * root + 1
            if child + 1 < end and result[child] < result[child + 1]:
                child += 1
            if result[root] >= result[child]:
                return
            result[root], result[child] = result[child], result[root]
            root = child

    for root in range(size // 2 - 1, -1, -1):
        sift_down(root, size)

    for end in range(size - 1, 0, -1):
        result[0], result[end] = result[end], result[0]
        sift_down(0, end)
    return result


class MaxHeap:
    def __init__(self):
        self._items = []

    def push(self, value):
        self._items.append(value)
        child = len(self._items) - 1
        while child > 0:
            parent = (child - 1) // 2
            if self._items[parent] >= self._items[child]:
                break
            self._items[parent], self._items[child] = (
                self._items[child],
                self._items[parent],
            )
            child = parent

    def peek_max(self):
        if not self._items:
            raise IndexError("peek_max de un heap vacío")
        return self._items[0]

    def pop_max(self):
        if not self._items:
            raise IndexError("pop_max de un heap vacío")
        maximum = self._items[0]
        last = self._items.pop()
        if self._items:
            self._items[0] = last
            parent = 0
            while True:
                left = 2 * parent + 1
                right = left + 1
                largest = parent
                if left < len(self._items) and self._items[left] > self._items[largest]:
                    largest = left
                if right < len(self._items) and self._items[right] > self._items[largest]:
                    largest = right
                if largest == parent:
                    break
                self._items[parent], self._items[largest] = (
                    self._items[largest],
                    self._items[parent],
                )
                parent = largest
        return maximum

    def __len__(self):
        return len(self._items)


def BFS(graph, start):
    visited = {start}
    order = []
    pending = deque([start])
    while pending:
        vertex = pending.popleft()
        order.append(vertex)
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                visited.add(neighbor)
                pending.append(neighbor)
    return order


def DFS(graph, start):
    visited = {start}
    order = []
    pending = [start]
    while pending:
        vertex = pending.pop()
        order.append(vertex)
        for neighbor in reversed(graph.get(vertex, [])):
            if neighbor not in visited:
                visited.add(neighbor)
                pending.append(neighbor)
    return order


def linear_search(values, target):
    for index, value in enumerate(values):
        if value == target:
            return index
    return -1


def binary_search(sorted_values, target):
    low, high = 0, len(sorted_values) - 1
    while low <= high:
        middle = (low + high) // 2
        if sorted_values[middle] == target:
            return middle
        if sorted_values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1


def set_status(record, status):
    """Asignar dos veces el mismo estado deja el mismo estado final."""
    record["status"] = status
    return record


SORTS = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
    "radix": radix_sort,
    "heap": heap_sort,
}


def run_checks():
    sample = [8, 3, 5, 1, 5, 0]
    expected = sorted(sample)
    for name, sort_function in SORTS.items():
        assert sort_function(sample) == expected, name
    assert quick_sort([]) == []
    assert radix_sort([]) == []
    try:
        radix_sort([2, -1])
    except ValueError:
        pass
    else:
        raise AssertionError("radix_sort debe rechazar enteros negativos")

    table = HashTable(2)
    table.put("ana", 42)
    table.put("ana", 43)
    assert table.get("ana") == 43 and len(table) == 1
    assert table.delete("ana") and table.get("ana") is None
    for value in range(20):
        table.put(f"clave-{value}", value)
    assert all(table.get(f"clave-{value}") == value for value in range(20))

    linked = LinkedList()
    for value in (1, 2, 3):
        linked.append(value)
    assert linked.delete(1) and linked.delete(3)
    assert linked.to_list() == [2] and len(linked) == 1

    doubly = DoublyLinkedList()
    first = doubly.append(1)
    doubly.append(2)
    last = doubly.append(3)
    assert doubly.delete_node(first) and doubly.delete_node(last)
    assert doubly.to_list() == [2] and len(doubly) == 1
    detached = _DoublyNode(9)
    assert not doubly.delete_node(detached) and doubly.to_list() == [2]

    stack = Stack()
    stack.push("primero")
    stack.push("último")
    assert stack.peek() == "último" and stack.pop() == "último"

    double_ended = Deque([2])
    double_ended.add_front(1)
    double_ended.add_rear(3)
    assert double_ended.remove_front() == 1
    assert double_ended.remove_rear() == 3
    assert double_ended.to_list() == [2]

    tree = BST()
    avl = AVLTree()
    for value in (3, 1, 4, 2):
        tree.insert(value)
        avl.insert(value)
    assert tree.inorder() == [1, 2, 3, 4]
    assert tree.search(4) is not None and tree.search(8) is None
    assert avl.inorder() == [1, 2, 3, 4]
    assert avl.search(2) is not None and avl.search(8) is None

    heap = MaxHeap()
    for value in (3, 1, 5, 2):
        heap.push(value)
    assert heap.peek_max() == 5
    assert [heap.pop_max() for _ in range(4)] == [5, 3, 2, 1]

    graph = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
    assert BFS(graph, "A") == ["A", "B", "C", "D"]
    assert DFS(graph, "A") == ["A", "B", "D", "C"]
    assert linear_search([4, 7, 9], 7) == 1
    assert linear_search([4, 7, 9], 8) == -1
    assert binary_search([1, 3, 5, 8, 9], 8) == 3
    assert binary_search([1, 3, 5, 8, 9], 4) == -1

    record = {"status": "inactivo"}
    set_status(record, "activo")
    once = dict(record)
    set_status(record, "activo")
    assert record == once


def show_trace():
    print("\nTraza corta de ordenamientos:")
    print(f"Valores de prueba: {VALUES_TO_TEST}")
    print("bubble_sort          ->", bubble_sort(VALUES_TO_TEST))
    print("selection_sort       ->", selection_sort(VALUES_TO_TEST))
    print("insertion_sort       ->", insertion_sort(VALUES_TO_TEST))
    print("merge_sort           ->", merge_sort(VALUES_TO_TEST))
    print("quick_sort           ->", quick_sort(VALUES_TO_TEST))
    print("radix_sort([21,13,11]) ->", radix_sort([21, 13, 11]))
    graph = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
    print("BFS desde A             ->", BFS(graph, "A"))
    print("DFS desde A             ->", DFS(graph, "A"))


def benchmark(values=VALUES_TO_TEST, repetitions=5):
    sort_functions = {
        "bubble": bubble_sort,
        "selection": selection_sort,
        "insertion": insertion_sort,
        "merge": merge_sort,
        "quick": quick_sort,
        "radix": radix_sort,
        "heap": heap_sort,
        "sorted (Python)": sorted,
    }

    print("\nBenchmark (mediana de segundos; cada algoritmo recibe los mismos datos):")
    print(f"{'n':>6}  {'algoritmo':<18} {'mediana (s)':>14}")
    data = list(values)
    expected = sorted(data)
    timings = {}
    for name, sort_function in sort_functions.items():
        observations = []
        for _ in range(repetitions):
            start = perf_counter()
            result = sort_function(data)
            observations.append(perf_counter() - start)
            if result != expected:
                raise AssertionError(f"{name} produjo un orden incorrecto")
        timings[name] = median(observations)

    for name, elapsed in sorted(timings.items(), key=lambda entry: entry[1]):
        print(f"{len(data):6}  {name:<18} {elapsed:14.8f}")
    winner = min(timings, key=timings.get)
    print(f"  Menor tiempo observado para n={len(data)}: {winner}\n")


def benchmark_search_and_graph(values=VALUES_TO_TEST, repetitions=5):
    search_functions = {
        "linear search": linear_search,
        "binary search": binary_search,
    }

    print("\nTiempos de búsqueda y recorridos (mediana de segundos):")
    print(f"{'n':>6}  {'algoritmo':<18} {'mediana (s)':>14}")
    data = list(values)
    sorted_values = sorted(data)
    target = sorted_values[-1] if sorted_values else -1
    expected_index = data.index(target) if target in data else -1
    search_cases = [
        (
            name,
            search_function,
            (data if name == "linear search" else sorted_values, target),
            expected_index if name == "linear search" else (
                sorted_values.index(target) if target in sorted_values else -1
            ),
        )
        for name, search_function in search_functions.items()
    ]

    for name, algorithm, arguments, expected in search_cases:
        observations = []
        for _ in range(repetitions):
            start = perf_counter()
            result = algorithm(*arguments)
            observations.append(perf_counter() - start)
            if result != expected:
                raise AssertionError(f"{name} produjo un resultado incorrecto")
        print(f"{len(data):6}  {name:<18} {median(observations):14.8f}")

    graph_size = len(data)
    graph = {
        vertex: [vertex + 1] if vertex + 1 < graph_size else []
        for vertex in range(graph_size)
    }
    expected_traversal = list(range(graph_size)) if graph_size else [0]
    for name, algorithm in (("BFS", BFS), ("DFS", DFS)):
        observations = []
        for _ in range(repetitions):
            start = perf_counter()
            result = algorithm(graph, 0)
            observations.append(perf_counter() - start)
            if result != expected_traversal:
                raise AssertionError(f"{name} produjo un resultado incorrecto")
        print(f"{graph_size:6}  {name:<18} {median(observations):14.8f}")


if __name__ == "__main__":
    run_checks()
    print("Comprobaciones: todas pasaron.")
    show_trace()
    benchmark()
    benchmark_search_and_graph()
