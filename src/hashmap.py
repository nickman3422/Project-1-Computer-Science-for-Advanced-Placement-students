"""
description: chained Hash Map with resizing
file: hashtable_open.py
language: python3
author: sps@cs.rit.edu Sean Strout
author: anh@cs.rit.edu Arthur Nunes-Harwitt
author: jsb@cs.rit.edu Jeremy Brown
author: as@cs.rit.edu Amar Saric
author: jeh@cs.rit.edu James Heliotis
"""

from typing import Any, Hashable, Sequence

class HashMap:
    """
    This hash map storage is a list of linked lists. Each node
    in each linked list contains an entry in the map.
    So as the storage fills up more and more, a linear component to the
    search becomes more significant. This HashMap rehashes to twice its
    count when the number of entries exceeds the length of the storage.
    """
    __slots__ = 'size', 'storage', 'capacity', 'collisions'

    def __init__( self, capacity = 100 ):
        self.size = 0
        self.storage = capacity * [None]
        self.capacity = 2 if capacity < 2 else capacity
        self.collisions = 0

    def __str__( self ):
        result = ""
        for i in range( len( self.storage ) ):
            e = self.storage[ i ]
            if e is not None:
                result += str( i ) + ": "
                result += str( e ) + "\n"
        return result

    class ChainNode:
        """
        A key-value entry plus a link to make it a node in a linked list
        """

        __slots__ = 'key', 'value', 'chain'

        def __init__( self,
                      key, value = None,
                      chain = None
                      ):
            self.key = key
            self.value = value
            self.chain = chain

        def __str__( self ):
            return "(" + str( self.key ) + ", " + str( self.value ) + ")"

def keys( hmap ):
    result = [ ]
    for entry_list in hmap.storage:
        entry = entry_list # Start at front
        while entry is not None:
            result.append( entry.key )
            entry = entry.chain
    return result

def contains( hmap, key ):
    index = hash_function( key ) % len( hmap.storage )
    entry = hmap.storage[ index ]
    while entry is not None:
        if entry.key == key:
            return True
        entry = entry.chain
    return False

def put( hmap, key, value ):

    index = hash_function( key ) % len( hmap.storage )

    # bookkeeping
    if hmap.storage[ index ] is not None and \
            hmap.storage[ index ].key != key:
        hmap.collisions += 1

    if hmap.size == hmap.capacity: # It should really check for a lower value!
        _rehash( hmap )
        index = hash_function( key ) % len( hmap.storage )
    front = hmap.storage[ index ]
    entry = front
    while entry is not None:
        if entry.key == key:
            entry.value = value
            return
        entry = entry.chain
    hmap.storage[ index ] = HashMap.ChainNode( key, value, front )
    hmap.size += 1

def delete( hmap, key ):

    index = hash_function( key ) % len( hmap.storage )
    front = hmap.storage[ index ]
    if front is None:
        raise Exception( "Element to delete does not exist" )
    if front.key == key:
        hmap.storage[ index ] = front.chain
        hmap.size -= 1
        return
    entry = front.chain
    prev = front
    while entry is not None:
        if entry.key == key:
            prev.chain = entry.chain
            hmap.size -= 1
            return
        prev = entry
        entry = entry.chain
    raise Exception( "Element to delete does not exist." )

def get( hmap, key ):
    index = hash_function( key ) % len( hmap.storage )
    entry = hmap.storage[ index ]
    while entry is not None:
        if entry.key == key:
            return entry.value
        entry = entry.chain
    raise Exception( "Element to get does not exist." )

def _rehash( hmap ):
    """
    Rebuild the map in a larger storage. The current map is not changed
    in any way that can be seen by its clients, but internally its storage is
    grown.
    :return: None
    """
    new_cap = 2 * hmap.capacity
    new_map = HashMap( new_cap )
    for key in keys( hmap ):
        put( new_map, key, get( hmap, key ) )
    hmap.capacity = new_map.capacity
    hmap.storage = new_map.storage
    # (Don't copy collisions. Collisions in rehashing don't count for us.)

def hash_function( value ):
    hashcode = hash( value )
    # hashcode = 0
    # hashcode = len( value )
    return hashcode