'''
Dictionary with auto-expiring values for caching purposes.

Expiration happens on any access, object is locked during cleanup from expired
values. Can not store more than max_len elements - the oldest will be deleted.

>>> ExpiringDict(max_len=100, max_age_seconds=10)

The values stored in the following way:
{
    key1: (value1, created_time1),
    key2: (value2, created_time2)
}

NOTE: iteration over dict and also keys() do not remove expired values!
'''

import time
from threading import RLock
import sys

try:
    from collections import OrderedDict
except ImportError:
    # Python < 2.7
    from ordereddict import OrderedDict


class ExpiringDict(OrderedDict):
    def __init__(self, max_len, max_age_seconds, default=None):
        assert max_age_seconds >= 0
        assert max_len >= 1
        if default is not None:
            assert isinstance(default, dict)

        OrderedDict.__init__(self)
        self.max_len = max_len
        self.max_age = max_age_seconds
        self.default = default
        self.lock = RLock()

        if sys.version_info >= (3, 5):
            self._safe_keys = lambda: list(self.keys())
        else:
            self._safe_keys = self.keys

    def __contains__(self, key):
        """ Return True if the dict has a key, else return False. """
        try:
            with self.lock:
                item = OrderedDict.__getitem__(self, key)
                if time.time() - item[1] < self.max_age:
                    return True
                else:
                    del self[key]
        except KeyError:
            pass

        _has, _value, _age = self._try_get_from_default(key)
        if _has:
            return True

        return False

    def _try_get_from_default(self, key):
        if self.default and key in self.default:
            return True, self.default[key], 999
        return False, None, 0

    def __getitem__(self, key, with_age=False):
        """ Return the item of the dict.

        Raises a KeyError if key is not in the map.
        """
        with self.lock:
            item = OrderedDict.__getitem__(self, key)
            item_age = time.time() - item[1]
            if item_age < self.max_age:
                if with_age:
                    return item[0], item_age
                else:
                    return item[0]
            else:
                _has, _value, _age = self._try_get_from_default(key)
                if _has:
                    return _value

                del self[key]
                raise KeyError(key)

    def __setitem__(self, key, value):
        """ Set d[key] to value. """
        with self.lock:
            if len(self) == self.max_len:
                try:
                    self.popitem(last=False)
                except KeyError:
                    pass
            OrderedDict.__setitem__(self, key, (value, time.time()))

    def pop(self, key, default=None):
        """ Get item from the dict and remove it.

        Return default if expired or does not exist. Never raise KeyError.
        """
        with self.lock:
            try:
                item = OrderedDict.__getitem__(self, key)
                del self[key]
                return item[0]
            except KeyError:
                _has, _value, _age = self._try_get_from_default(key)
                if _has:
                    return _value

                return default

    def ttl(self, key):
        """ Return TTL of the `key` (in seconds).

        Returns None for non-existent or expired keys.
        """
        key_value, key_age = self.get(key, with_age=True)
        if key_age:
            key_ttl = self.max_age - key_age
            if key_ttl > 0:
                return key_ttl

        _has, _value, _age = self._try_get_from_default(key)
        if _has:
            return _age

        return None

    def get(self, key, default=None, with_age=False):
        " Return the value for key if key is in the dictionary, else default. "
        try:
            return self.__getitem__(key, with_age)
        except KeyError:
            if with_age:
                return default, None
            else:
                return default

    def items(self):
        """ Return a copy of the dictionary's list of (key, value) pairs. """
        r = []
        for key in self._safe_keys():
            try:
                r.append((key, self[key]))
            except KeyError:
                pass
        return r

    def values(self):
        """ Return a copy of the dictionary's list of values.
        See the note for dict.items(). """
        r = []
        for key in self._safe_keys():
            try:
                r.append(self[key])
            except KeyError:
                pass
        return r

    def fromkeys(self):
        " Create a new dictionary with keys from seq and values set to value. "
        raise NotImplementedError()

    def iteritems(self):
        """ Return an iterator over the dictionary's (key, value) pairs. """
        raise NotImplementedError()

    def itervalues(self):
        """ Return an iterator over the dictionary's values. """
        raise NotImplementedError()

    def viewitems(self):
        " Return a new view of the dictionary's items ((key, value) pairs). "
        raise NotImplementedError()

    def viewkeys(self):
        """ Return a new view of the dictionary's keys. """
        raise NotImplementedError()

    def viewvalues(self):
        """ Return a new view of the dictionary's values. """
        raise NotImplementedError()
