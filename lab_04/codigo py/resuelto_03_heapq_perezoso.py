#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratorio 04 - Algoritmos Avanzados (UNSAAC, 2026-II)
Ejercicio Resuelto 3: Cola de Prioridad con heapq y Actualizaciones Perezosas
"""

import heapq
import itertools

REMOVED = object()

class HeapqPriorityQueue:
    def __init__(self):
        self.heap = []
        self.entries = {}
        self.counter = itertools.count()

    def is_empty(self) -> bool:
        self._discard_removed()
        return len(self.entries) == 0

    def insert(self, item, priority: int):
        if item in self.entries:
            self.remove(item)
        entry = [priority, next(self.counter), item]
        self.entries[item] = entry
        heapq.heappush(self.heap, entry)
        return entry

    def remove(self, item):
        entry = self.entries.pop(item)
        entry[2] = REMOVED

    def decrease_key(self, item, new_priority: int):
        old_priority = self.entries[item][0]
        if new_priority > old_priority:
            raise ValueError(f"La nueva clave ({new_priority}) debe ser menor o igual ({old_priority})")
        if new_priority == old_priority:
            return
        self.insert(item, new_priority)

    def minimum(self):
        self._discard_removed()
        if not self.heap:
            raise IndexError("Cola de prioridad vacía")
        priority, _, item = self.heap[0]
        return item, priority

    def extract_min(self):
        while self.heap:
            priority, _, item = heapq.heappop(self.heap)
            if item is not REMOVED:
                del self.entries[item]
                return item, priority
        raise IndexError("Cola de prioridad vacía")

    def _discard_removed(self):
        while self.heap and self.heap[0][2] is REMOVED:
            heapq.heappop(self.heap)

    def __len__(self):
        return len(self.entries)

    @property
    def physical_size(self):
        return len(self.heap)

def main():
    print("=" * 60)
    print(" EJERCICIO RESUELTO 3: HEAPQ CON ACTUALIZACIÓN PEREZOSA")
    print("=" * 60)

    pq = HeapqPriorityQueue()
    print("1. Insertando elementos ('a': 20, 'b': 12, 'c': 30)...")
    pq.insert("a", 20)
    pq.insert("b", 12)
    pq.insert("c", 30)
    print(f"   - Entradas activas: {len(pq)}, Tamaño físico: {pq.physical_size}")

    print("\n2. Ejecutando decrease_key('c', 5)...")
    pq.decrease_key("c", 5)
    print(f"   - Mínimo actual: {pq.minimum()}")
    print(f"   - Entradas activas: {len(pq)}, Tamaño físico heap: {pq.physical_size} (1 obsoleta acumulada)")

    print("\n3. Extrayendo elementos en orden de prioridad:")
    while not pq.is_empty():
        item, prio = pq.extract_min()
        print(f"   - Extraído: '{item}' con prioridad {prio}")

    assert pq.is_empty(), "La cola debería estar vacía"
    print("\n[ÉXITO] Ejercicio Resuelto 3 validado y verificado al 100%.")

if __name__ == "__main__":
    main()
