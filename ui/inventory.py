from ppi.pySingleton import Singleton


class IntelligentInventory(Singleton):
    _slots: []

    def __init__(self, size: int = 9 * 4, max_window_percentages: (float, float) = (.5, .5)):
        self._slots = []

        self.reszize(size)

    def reszize(self, new_size: int):
        def shrink():
            if None in self._slots:
                del self._slots[self._get_index(None)]
            else:
                if len(self._slots) % 2 == 0:
                    del self._slots[len(self._slots) - 1]
                else:
                    del self._slots[0]

        def grow():
            """ Grows the Inventory by one and moves the items into the middle"""
            if len(self._slots) % 2 == 0:
                self._slots.append((None, 0))
            else:
                self._slots.insert(0, (None, 0))

        while len(self._slots) > new_size:
            try:
                shrink()
            except Exception as ex:
                print(ex)
        while len(self._slots) < new_size:
            try:
                grow()
            except Exception as ex:
                print(ex)

    @property
    def items(self):
        return ((i, j) for i, j in enumerate(self._slots))

    def _slot_is_occupied(self, index):
        return not (self._slots[index][0] is None)

    def _get_index(self, value):
        cntr = 0
        for i in self._slots:
            print(type(i[0]), type(value))
            if type(i[0]) == type(value):
                return cntr
            cntr += 1
        return None

    def add_item(self, item: object, amount: int = 1, index: int = -1, auto_index_on_error: bool = True):
        if index == -1:
            index = self._get_index(None)

        while self._slot_is_occupied(index) and auto_index_on_error:
            index += 1
            if index >= len(self._slots):
                index = 0

        self._slots[index] = (item, amount)

    def get_item(self, index) -> (object, int):
        return self._slots[index]

    def remove_item(self, index: int, amount: int, find_items: bool = False):
        def remove(wamount: int, windex: int):
            if self._slot_is_occupied(windex):
                if self._slots[windex][1] > wamount:
                    self._slots[windex] = (self._slots[windex][0], self._slots[windex][1] - wamount)
                    return True
                elif self._slots[windex][1] == wamount:
                    self._slots[windex] = (None, 0)
                    return True
                else:
                    raise Exception(
                        f'Not enought items in slot {windex} missing {wamount - self._slots[windex][1]} items!')
            else:
                raise Exception(f'Slot {windex} empty, cannot remove!')

        if not find_items:
            remove(amount, index)
        else:
            # TODO Check if this really works all the time!

            amount -= 1
            item_to_remove = self.get_item(index)[0]
            while self._get_index(item_to_remove) is not None and amount >= 0:
                p = self._get_index(item_to_remove)
                remove(1, self._get_index(item_to_remove))
                amount -= 1
            if amount > 0:
                raise Exception(f'Not enough items of type {item_to_remove}, missing {amount} items')


class Hotbar:
    selector: int
    size: int
    inventory: IntelligentInventory

    def __init__(self, size: int = 9, inventory: IntelligentInventory = IntelligentInventory()):
        self.inner_inventory = inventory
        self.size = size
        self.selector = 0
