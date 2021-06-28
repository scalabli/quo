#
#
#
import inspect
import asyncio
from functools import update_wrapper
from quo.core import Argument
from quo.core import Command
from quo.core import Tether
from quo.core import App
from quo.context.current import currentcontext
from quo.expediency.utilities import echo
from quo.decorators import autoconfirm
from quo.decorators import autopswd
from quo.decorators import autoversion
from quo.decorators import autohelp

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
            def new_func(clime, *args, **kwargs):
                obj = clime.find_object(object_type)
                return clime.invoke(f, obj, *args, **kwargs)
            return update_wrapper(new_func, f)
        return decorator

    :param object_type: the type of the object to pass.
    :param ensure: if set to `True`, a new object will be created and
                   remembered on the context if it's not there yet.
    """

    def decorator(f):
        def new_func(*args, **kwargs):
            clime = currentcontext()
            if ensure:
                obj = clime.ensure_object(object_type)
            else:
                obj = clime.find_object(object_type)
            if obj is None:
                raise RuntimeError(
                    "Managed to invoke callback without a context"
                    f" object of type {object_type.__name__!r}"
                    " existing."
                )
            return clime.invoke(f, obj, *args, **kwargs)

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


def command(name=None, cls=None, **attrs):
    r"""Creates a new :class:`Command` and uses the decorated function as
    callback.  This will also automatically attach all decorated
    :func:`app`\s and :func:`argument`\s as parameters to the command.

    The name of the command defaults to the name of the function with
    underscores replaced by dashes.  If you want to change that, you can
    pass the intended name as the first argument.

    All keyword arguments are forwarded to the underlying command class.

    Once decorated the function turns into a :class:`Command` instance
    that can be invoked as a command line utility or be attached to a
    command :class:`Tether`.

    :param name: the name of the command.  This defaults to the function
                 name with underscores replaced by dashes.
    :param cls: the command class to instantiate.  This defaults to
                :class:`Command`.
    """
    if cls is None:
        cls = Command

    def decorator(f):
        cmd = _make_command(f, name, attrs, cls)
        cmd.__doc__ = f.__doc__
        return cmd

    return decorator




def _param_memo(f, param):
    if isinstance(f, Command):
        f.params.append(param)
    else:
        if not hasattr(f, "__quo_params__"):
            f.__quo_params__ = []
        f.__quo_params__.append(param)





def app(*param_decls, **attrs):
    """Attaches an app to the command.  All positional arguments are
    passed as parameter declarations to :class:`App`; all keyword
    arguments are forwarded unchanged (except ``cls``).
    This is equivalent to creating an :class:`App` instance manually
    and attaching it to the :attr:`Command.params` list.

    :param cls: the option class to instantiate.  This defaults to
                :class:`App`.
    """

    def decorator(f):
        # Issue 926, copy attrs, so pre-defined options can re-use the same cls=
        option_attrs = attrs.copy()

        if "help" in option_attrs:
            option_attrs["help"] = inspect.cleandoc(option_attrs["help"])
        OptionClass = option_attrs.pop("cls", App)
        _param_memo(f, OptionClass(param_decls, **option_attrs))
        return f

    return decorator


def argument(*param_decls, **attrs):
    """Attaches an argument to the command.  All positional arguments are
    passed as parameter declarations to :class:`Argument`; all keyword
    arguments are forwarded unchanged (except ``cls``).
    This is equivalent to creating an :class:`Argument` instance manually
    and attaching it to the :attr:`Command.params` list.

    :param cls: the argument class to instantiate.  This defaults to
                :class:`Argument`.
    """

    def decorator(f):
        ArgumentClass = attrs.pop("cls", Argument)
        _param_memo(f, ArgumentClass(param_decls, **attrs))
        return f

    return decorator

def tether(name=None, **attrs):
    """Creates a new :class:`Tether` with a function as callback.  This
    works otherwise the same as :func:`command` just that the `cls`
    parameter is set to :class:`Tether`.
    """
    attrs.setdefault("cls", Tether)
    return command(name, **attrs)
