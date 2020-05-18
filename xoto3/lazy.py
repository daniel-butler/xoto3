"""Primarily for singleton resources that you want to lazily load on usage."""
import typing as ty
from typing import TypeVar, Generic
from threading import local

import boto3

L = TypeVar("L")


class Lazy(Generic[L]):
    """A Lazy resource pattern.

    Encapsulates a single instance of the resource that can be accessed
    with (), and can also have more than one copy made of it as desired.
    """

    def __init__(self, loader_func: ty.Callable[..., L], storage=None):  # must have a __dict__
        """The loader func can encapsulate everything necessary to create the
        resource, or it can take additional arguments via the call.

        """
        self.loader_func = loader_func
        self.storage = storage if storage else lambda: 0

    def __call__(self, *args, **kwargs) -> L:
        """Access to the internal instance.

        The first call will create an internal instance, and
        subsequent calls will return it.
        """
        try:
            return self.storage.value
        except AttributeError:
            self.storage.value = self.instance(*args, **kwargs)
            return self.storage.value

    def copy(self) -> "Lazy[L]":
        """Each Lazy object is a self-contained singleton

        but other Lazy-loading resource copies can easily be derived
        from the first.

        """
        return Lazy(self.loader_func)

    def instance(self, *args, **kwargs) -> L:
        """If you want your own personal instance instead of the internal one,
        you may create it.

        """
        return self.loader_func(*args, **kwargs)


class ThreadLocalLazy(Lazy[L]):
    def __init__(self, loader_func: ty.Callable[..., L]):
        # local() creates a brand new instance every time it is called,
        # so this does not cause issues with storage being shared across multiple TTLazies
        super().__init__(loader_func, local())


class SessionedBoto3:
    """Apparently there are thread-safety issues conditions if you don't
    first create a session.

    https://github.com/boto/boto3/issues/1592
    """

    def __init__(self, method_name: str, *args, **kwargs):
        self.method_name = method_name
        assert self.method_name in {"resource", "client"}
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        session = boto3.session.Session()
        method = getattr(session, self.method_name)
        return method(*self.args, **self.kwargs)


def tlls(method_name: str, *args, **kwargs):
    """Thread Local Lazy SessionedBoto3"""
    return ThreadLocalLazy(SessionedBoto3(method_name, *args, **kwargs))
