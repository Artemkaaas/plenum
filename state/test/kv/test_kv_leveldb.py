import os
import pytest
from state.kv.kv_store_leveldb import KeyValueStorageLeveldb

i = 0

@pytest.yield_fixture(scope="function")
def kv(tempdir) -> KeyValueStorageLeveldb:
    global i
    kv = KeyValueStorageLeveldb(os.path.join(tempdir, 'kv{}'.format(i)))
    i += 1
    yield kv
    kv.close()

def test_reopen(kv):
    kv.put('k1', 'v1')
    v1 = kv.get('k1')
    kv.close()

    kv.open()
    v2 = kv.get('k1')

    assert b'v1' == v1
    assert b'v1' == v2

def test_drop(kv):
    kv.put('k1', 'v1')
    hasKeyBeforeDrop = kv.has_key('k1')
    kv.close()
    kv.drop()

    kv.open()
    hasKeyAfterDrop = kv.has_key('k1')

    assert hasKeyBeforeDrop
    assert not hasKeyAfterDrop

def test_put_string(kv):
    kv.put('k1', 'v1')
    v1 = kv.get('k1')

    kv.put('k2', 'v2')
    v2 = kv.get('k2')

    kv.put('k1', 'v3')
    v3 = kv.get('k1')
    v4 = kv.get('k2')

    assert b'v1' == v1
    assert b'v2' == v2
    assert b'v3' == v3
    assert b'v2' == v4

def test_put_bytes(kv):
    kv.put(b'k1', b'v1')
    v1 = kv.get(b'k1')

    kv.put(b'k2', b'v2')
    v2 = kv.get(b'k2')

    kv.put(b'k1', b'v3')
    v3 = kv.get(b'k1')
    v4 = kv.get(b'k2')

    assert b'v1' == v1
    assert b'v2' == v2
    assert b'v3' == v3
    assert b'v2' == v4

def test_put_string_and_bytes(kv):
    kv.put(b'k1', 'v1')
    v1 = kv.get('k1')

    kv.put('k2', b'v2')
    v2 = kv.get(b'k2')

    kv.put('k1', b'v3')
    v3 = kv.get('k1')
    v4 = kv.get('k2')

    assert b'v1' == v1
    assert b'v2' == v2
    assert b'v3' == v3
    assert b'v2' == v4

def test_remove_string(kv):
    kv.put('k1', 'v1')
    hasKeyBeforeRemove = kv.has_key('k1')
    kv.remove('k1')
    hasKeyAfterRemove = kv.has_key('k1')

    assert hasKeyBeforeRemove
    assert not hasKeyAfterRemove

def test_remove_bytes(kv):
    kv.put(b'k1', b'v1')
    hasKeyBeforeRemove = kv.has_key(b'k1')
    kv.remove(b'k1')
    hasKeyAfterRemove = kv.has_key(b'k1')

    assert hasKeyBeforeRemove
    assert not hasKeyAfterRemove

def test_batch_string(kv):
    batch = [('k'.format(i), 'v'.format(i))
             for i in range(5)]
    kv.setBatch(batch)

    for i in range(5):
        assert 'v'.format(i).encode() == kv.get('k'.format(i))

def test_batch_bytes(kv):
    batch = [('k'.format(i).encode(), 'v'.format(i).encode())
             for i in range(5)]
    kv.setBatch(batch)

    for i in range(5):
        assert 'v'.format(i).encode() == kv.get('k'.format(i))