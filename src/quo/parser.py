# This code uses parts of optparse written by Gregory P. Ward and
# maintained by the Python Software Foundation.
from collections import deque

from quo.outliers import BadArgUsage, BadAppUsage, NoSuchApp, UsageError

# Sentinel value that indicates an app was passed as a flag without a
# value but is not a flag app. App.consume_value uses this to
# prompt or use the flag_value.
_flag_needs_value = object()

# This returns a Tuple with the unpacked arguments
#at the first index and the remaining arguments as the second 
def _unpack_args(args, nargs_spec):
    """Given an iterable of arguments and an iterable of nargs specifications,
    it returns a tuple with all the unpacked arguments at the first index
    and all remaining arguments as the second.

    The nargs specification is the number of arguments that should be consumed
    or `-1` to indicate that this position should eat up all the remainders.

    Missing items are filled with `None`.
    """
    #Missing items are filled with 'None' 
    args = deque(args)
    nargs_spec = deque(nargs_spec)
    rv = []
    spos = None

    def _fetch(c):
        try:
            if spos is None:
                return c.popleft()
            else:
                return c.pop()
        except IndexError:
            return None

    while nargs_spec:
        nargs = _fetch(nargs_spec)
        if nargs == 1:
            rv.append(_fetch(args))
        elif nargs > 1:
            x = [_fetch(args) for _ in range(nargs)]
            # If we're reversed, we're pulling in the arguments in reverse,
            # so we need to turn them around.
            if spos is not None:
                x.reverse()
            rv.append(tuple(x))
        elif nargs < 0:
            if spos is not None:
                raise TypeError("Cannot have two nargs < 0")
            spos = len(rv)
            rv.append(None)

    # spos is the position of the wildcard (star).  If it's not `None`,
    # we fill it with the remainder.
    if spos is not None:
        rv[spos] = tuple(args)
        args = []
        rv[spos + 1 :] = reversed(rv[spos + 1 :])

    return tuple(rv), list(args)


def split_opt(opt):
    first = opt[:1]
    if first.isalnum():
        return "", opt
    if opt[1:2] == first:
        return opt[:2], opt[2:]
    return first, opt[1:]


def normalize_opt(opt, clime):
    if clime is None or clime.token_normalize_func is None:
        return opt
    prefix, opt = split_opt(opt)
    return f"{prefix}{clime.token_normalize_func(opt)}"


def split_arg_string(string):
    """Split an argument string as with :func:`shlex.split`, but don't
    fail if the string is incomplete. Ignores a missing closing quote or
    incomplete escape sequence and uses the partial token as-is.

    .. code-block:: python

        split_arg_string("example 'my file")
        ["example", "my file"]

        split_arg_string("example my\\")
        ["example", "my"]

    :param string: String to split.
    """
    #splits an argument using :func :'shlex.split'
    import shlex

    lex = shlex.shlex(string, posix=True)
    lex.whitespace_split = True
    lex.commenters = ""
    out = []

    try:
        for token in lex:
            out.append(token)
    except ValueError:
        # Raised when end-of-string is reached in an invalid state. Use
        # the partial token as-is. The quote or escape character is in
        # lex.state, not lex.token.
        out.append(lex.token)

    return out


class App:
    def __init__(self, opts, dest, action=None, nargs=1, const=None, obj=None):
        self._short_opts = []
        self._long_opts = []
        self.prefixes = set()

        for opt in opts:
            prefix, value = split_opt(opt)
            if not prefix:
                raise ValueError(f"Invalid start character for app ({opt})")
            self.prefixes.add(prefix[0])
            if len(prefix) == 1 and len(value) == 1:
                self._short_opts.append(opt)
            else:
                self._long_opts.append(opt)
                self.prefixes.add(prefix)

        if action is None:
            action = "store"

        self.dest = dest
        self.action = action
        self.nargs = nargs
        self.const = const
        self.obj = obj

    @property
    def takes_value(self):
        return self.action in ("store", "append")

    def process(self, value, state):
        if self.action == "store":
            state.opts[self.dest] = value
        elif self.action == "store_const":
            state.opts[self.dest] = self.const
        elif self.action == "append":
            state.opts.setdefault(self.dest, []).append(value)
        elif self.action == "append_const":
            state.opts.setdefault(self.dest, []).append(self.const)
        elif self.action == "count":
            state.opts[self.dest] = state.opts.get(self.dest, 0) + 1
        else:
            raise ValueError(f"unknown action '{self.action}'")
        state.order.append(self.obj)


class Arg:
    def __init__(self, dest, nargs=1, obj=None):
        self.dest = dest
        self.nargs = nargs
        self.obj = obj

    def process(self, value, state):
        if self.nargs > 1:
            holes = sum(1 for x in value if x is None)
            if holes == len(value):
                value = None
            elif holes != 0:
                raise BadArgUsage(
                    f"argument {self.dest} takes {self.nargs} values"
                )

        if self.nargs == -1 and self.obj.envvar is not None:
            value = None

        state.opts[self.dest] = value
        state.order.append(self.obj)


class ParsingState:
    def __init__(self, rargs):
        self.opts = {}
        self.largs = []
        self.rargs = rargs
        self.order = []


class AppParser:
    """The app parser is an internal class that is ultimately used to
    parse apps and arguments.  It's modelled after optparse and brings
    a similar but vastly simplified API.  It should generally not be used
    directly as the high level quo classes wrap it for you.

    It's not nearly as extensible as optparse or argparse as it does not
    implement features that are implemented on a higher level (such as
    types or defaults).

    :param clime: optionally the :class:`~quo.Context` where this parser
                should go with.
    """

    def __init__(self, clime=None):
        #: The :class:`~quo.Context` for this parser.  This might be
        #: `None` for some advanced use cases.
        self.clime = clime
        #: This controls how the parser deals with interspersed arguments.
        #: If this is set to `False`, the parser will stop on the first
        #: non-app.  quo uses this to implement nested subcommands
        #: safely.
        self.allow_interspersed_args = True
        #: This tells the parser how to deal with unknown apps.  By
        #: default it will error out (which is sensible), but there is a
        #: second mode where it will ignore it and continue processing
        #: after shifting all the unknown apps into the resulting args.
        self.ignore_unknown_apps = False
        if clime is not None:
            self.allow_interspersed_args = clime.allow_interspersed_args
            self.ignore_unknown_apps = clime.ignore_unknown_apps
        self._short_opt = {}
        self._long_opt = {}
        self._opt_prefixes = {"-", "--"}
        self._args = []

    def add_app(self, opts, dest, action=None, nargs=1, const=None, obj=None):
        """Adds a new app named `dest` to the parser.  The destination
        is not inferred (unlike with optparse) and needs to be explicitly
        provided.  Action can be any of ``store``, ``store_const``,
        ``append``, ``appnd_const`` or ``count``.

        The `obj` can be used to identify the app in the order list
        that is returned from the parser.
        """
        if obj is None:
            obj = dest
        opts = [normalize_opt(opt, self.clime) for opt in opts]
        app = App(opts, dest, action=action, nargs=nargs, const=const, obj=obj)
        self._opt_prefixes.update(app.prefixes)
        for opt in app._short_opts:
            self._short_opt[opt] = app
        for opt in app._long_opts:
            self._long_opt[opt] = app

    def add_arg(self, dest, nargs=1, obj=None):
        """Adds a positional arg named `dest` to the parser.

        The `obj` can be used to identify the app in the order list
        that is returned from the parser.
        """
        if obj is None:
            obj = dest
        self._args.append(Arg(dest=dest, nargs=nargs, obj=obj))

    def parse_args(self, args):
        """Parses positional arguments and returns ``(values, args, order)``
        for the parsed apps and arguments as well as the leftover
        arguments if there are any.  The order is a list of objects as they
        appear on the command line.  If arguments appear multiple times they
        will be memorized multiple times as well.
        """
        state = ParsingState(args)
        try:
            self._process_args_for_apps(state)
            self._process_args_for_args(state)
        except UsageError:
            if self.clime is None or not self.clime.resilient_parsing:
                raise
        return state.opts, state.largs, state.order

    def _process_args_for_args(self, state):
        pargs, args = _unpack_args(
            state.largs + state.rargs, [x.nargs for x in self._args]
        )

        for idx, arg in enumerate(self._args):
            arg.process(pargs[idx], state)

        state.largs = args
        state.rargs = []

    def _process_args_for_apps(self, state):
        while state.rargs:
            arg = state.rargs.pop(0)
            arglen = len(arg)
            # Double dashes always handled explicitly regardless of what
            # prefixes are valid.
            if arg == "--":
                return
            elif arg[:1] in self._opt_prefixes and arglen > 1:
                self._process_opts(arg, state)
            elif self.allow_interspersed_args:
                state.largs.append(arg)
            else:
                state.rargs.insert(0, arg)
                return

        # 
        # not a very interesting subset!

    def _match_long_opt(self, opt, explicit_value, state):
        if opt not in self._long_opt:
            from difflib import get_close_matches

            possibilities = get_close_matches(opt, self._long_opt)
            raise NoSuchApp(opt, possibilities=possibilities, clime=self.clime)

        app = self._long_opt[opt]
        if app.takes_value:
            # 
            #
            #
            # 
            if explicit_value is not None:
                state.rargs.insert(0, explicit_value)

            value = self._get_value_from_state(opt, app, state)

        elif explicit_value is not None:
            raise BadAppUsage(opt, f"{opt} app does not take a value")

        else:
            value = None

        app.process(value, state)

    def _match_short_opt(self, arg, state):
        stop = False
        i = 1
        prefix = arg[0]
        unknown_apps = []

        for ch in arg[1:]:
            opt = normalize_opt(f"{prefix}{ch}", self.clime)
            app = self._short_opt.get(opt)
            i += 1

            if not app:
                if self.ignore_unknown_apps:
                    unknown_apps.append(ch)
                    continue
                raise NoSuchApp(opt, clime=self.clime)
            if app.takes_value:
                # Any characters left in arg?  Pretend they're the
                # next arg, and stop consuming characters of arg.
                if i < len(arg):
                    state.rargs.insert(0, arg[i:])
                    stop = True

                value = self._get_value_from_state(opt, app, state)

            else:
                value = None

            app.process(value, state)

            if stop:
                break

        # If we got any unknown apps we re-combinate the string of the
        # remaining apps and re-attach the prefix, then report that
        # to the state as new larg.  This way there is basic combinatorics
        # that can be achieved while still ignoring unknown arguments.
        if self.ignore_unknown_apps and unknown_apps:
            state.largs.append(f"{prefix}{''.join(unknown_apps)}")

    def _get_value_from_state(self, app_name, app, state):
        nargs = app.nargs

        if len(state.rargs) < nargs:
            if app.obj._flag_needs_value:
                # App allows omitting the value.
                value = _flag_needs_value
            else:
                n_str = "an argument" if nargs == 1 else f"{nargs} arguments"
                raise BadAppUsage(
                    app_name, f"{app_name} app requires {n_str}."
                )
        elif nargs == 1:
            next_rarg = state.rargs[0]

            if (
                app.obj._flag_needs_value
                and isinstance(next_rarg, str)
                and next_rarg[:1] in self._opt_prefixes
                and len(next_rarg) > 1
            ):
                # The next arg looks like the start of an app, don't
                # use it as the value if omitting the value is allowed.
                value = _flag_needs_value
            else:
                value = state.rargs.pop(0)
        else:
            value = tuple(state.rargs[:nargs])
            del state.rargs[:nargs]

        return value

    def _process_opts(self, arg, state):
        explicit_value = None
        # Long app handling happens in two parts.  The first part is
        # supporting explicitly attached values.  In any case, we will try
        # to long match the app first.
        if "=" in arg:
            long_opt, explicit_value = arg.split("=", 1)
        else:
            long_opt = arg
        norm_long_opt = normalize_opt(long_opt, self.clime)

        # At this point we will match the (assumed) long app through
        # the long app matching code.  Note that this allows apps
        # like "-foo" to be matched as long apps.
        try:
            self._match_long_opt(norm_long_opt, explicit_value, state)
        except NoSuchApp:
            # At this point the long app matching failed, and we need
            # to try with short apps.  However there is a special rule
            # which says, that if we have a two character apps prefix
            # (applies to "--foo" for instance), we do not dispatch to the
            # short app code and will instead raise the no app
            # error.
            if arg[:2] not in self._opt_prefixes:
                return self._match_short_opt(arg, state)
            if not self.ignore_unknown_apps:
                raise
            state.largs.append(arg)
