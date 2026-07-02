from typing_extensions import Optional


class ListNode:
    def __init__(self, val) -> None:
        self.val = val
        self.top: Optional[ListNode] = None
        self.bottom: Optional[ListNode] = None


class Link:
    def __init__(self) -> None:
        self.head: Optional[ListNode] = None
        self.tail: Optional[ListNode] = None
        self.idx = {}


link = Link()


def enqueue(val: int):
    newNode = ListNode(val)
    link.idx[val] = newNode
    if link.tail is None:
        link.tail = newNode
        link.head = newNode
        return

    newNode.top = link.tail
    link.tail.bottom = newNode
    link.tail = newNode


def dequeue() -> int:
    if link.head is None:
        return -1

    code = link.head.val

    if link.head == link.tail:
        del link.idx[link.head.val]
        link.head = None
        link.tail = None
        return code

    temp = link.head
    link.head = link.head.bottom
    link.head.top = None  # type: ignore
    temp.bottom = None
    del link.idx[temp.val]

    return code


def refresh(code: int):
    node = link.idx.get(code, None)

    if node == link.tail or node is None:
        return

    if node == link.head:
        dequeue()
        enqueue(code)
        return

    curr_top = node.top
    curr_btm = node.bottom

    curr_top.bottom = curr_btm
    curr_btm.top = curr_top

    node.top = None
    node.bottom = None
    enqueue(node.val)
