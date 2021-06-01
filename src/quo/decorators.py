#
#
#
import inspect
from functools import update_wrapper
from .core import Argument
from .core import Command
from .core import Tether
from .core import Option
from quo.context.current import currentcontext
from .utilities import echo
from quo.decorators import argument
from quo.decorators import autoconfirm
from quo.decorators import autopswd
from quo.decorators import autoversion
from quo.decorators import autohelp
from quo.decorators import command
from quo.decorators import option
from quo.decorators import tether

#Marks a callback as wanting to receive current context
def contextualize(f):
    """Marks a callback as wanting to receive the current context
    object as first argument.
    """

    def new_func(*args, **kwargs):
        return f(currentcontext(), *args, **kwargs)

    return update_wrapper(new_func, f)


def objectualize(f):
    """This function passes the object on the
    context onwards (:attr:`Context.obj`).  This is useful if that object
    represents the state of a nested system.
    """

    def new_func(*args, **kwargs):
        return f(currentcontext().obj, *args, **kwargs)

    return update_wrapper(new_func, f)


def make_pass_decorator(object_type, ensure=False):
    """Given an object type this creates a decorator that will work
    similar to :func:`objectualize` but instead of passing the object of the
    current context, it will find the innermost context of type
    :func:`object_type`.

    This generates a decorator that works roughly like this::

        from functools import update_wrapper

        def decorator(f):
            @contextualize
            def new_func(ctx, *args, **kwargs):
                obj = ctx.find_object(object_type)
                return ctx.invoke(f, obj, *args, **kwargs)
            return update_wrapper(new_func, f)
        return decorator

    :param object_type: the type of the object to pass.
    :param ensure: if set to `True`, a new object will be created and
                   remembered on the context if it's not there yet.
    """

    def decorator(f):
        def new_func(*args, **kwargs):
            ctx = currentcontext()
            if ensure:
                obj = ctx.ensure_object(object_type)
            else:
                obj = ctx.find_object(object_type)
            if obj is None:
                raise RuntimeError(
                    "Managed to invoke callback without a context"
                    f" object of type {object_type.__name__!r}"
                    " existing."
                )
            return ctx.invoke(f, obj, *args, **kwargs)

        return update_wrapper(new_func, f)

    return decorator


def _make_command(f, name, attrs, cls):
    if isinstance(f, Command):
        raise TypeError("Attempted to convert a callback into a command twice.")
    try:
        params = f.__quo_params__
        params.reverse()
        del f.__quo_params__
    except AttributeError:
        params = []
    help = attrs.get("help")
    if help is None:
        help = inspect.getdoc(f)
        if isinstance(help, bytes):
            help = help.decode("utf-8")
    else:
        help = inspect.cleandoc(help)
    attrs["help"] = help
    return cls(
        name=name or f.__name__.lower().replace("_", "-"),
        callback=f,
        params=params,
        **attrs,
    )


