#
import os
import re
import contextlib
import ctypes
from ctypes.wintypes import (
    BOOL,
    CHAR,
    DWORD,
    HANDLE,
    LONG,
    LPWSTR,
    MAX_PATH,
    PDWORD,
    ULONG,
)


from .core import Arg
from .core import MultiCommand
from .core import App
from .core import ParameterSource
from .core import SHELL_NAMES
from .parser import split_arg_string
from quo.expediency.vitals import inscribe


def shell_complete(cli, ctx_args, prog_name, complete_var, instruction):
    #Perform shell completion for the given CLI program.

    #param cli: Command being called.
    #param ctx_args: Extra arguments to pass to``cli.make_context``.
    #param prog_name: Name of the executable in the shell.
    #param complete_var: Name of the environment variable that holds the completion instruction.
    #param instruction: Value of ``complete_var`` with the completion instruction and shell, in the form ``instruction_shell``.
    #return: Status code to exit with.
    
    shell, _, instruction = instruction.partition("_")
    comp_cls = get_completion_class(shell)

    if comp_cls is None:
        return 1

    comp = comp_cls(cli, ctx_args, prog_name, complete_var)

    if instruction == "source":
        echo(comp.source())
        return 0

    if instruction == "complete":
        echo(comp.complete())
        return 0

    return 1


class CompletionItem:
    """Represents a completion value and metadata about the value. The
    default metadata is ``type`` to indicate special shell handling,
    and ``help`` if a shell supports showing a help string next to the
    value.

    Arbitrary parameters can be passed when creating the object, and
    accessed using ``item.attr``. If an attribute wasn't passed,
    accessing it returns ``None``.

    :param value: The completion suggestion.
    :param type: Tells the shell script to provide special completion
        support for the type. quo uses ``"dir"`` and ``"file"``.
    :param help: String shown next to the value if supported.
    :param kwargs: Arbitrary metadata. The built-in implementations
        don't use this, but custom type completions paired with custom
        shell support could use it.
    """

    __slots__ = ("value", "type", "help", "_info")

    def __init__(self, value, type="plain", help=None, **kwargs):
        self.value = value
        self.type = type
        self.help = help
        self._info = kwargs

    def __getattr__(self, name):
        return self._info.get(name)


# Only Bash >= 4.4 has the nosort option.
_SOURCE_BASH = """\
%(complete_func)s() {
    local IFS=$'\\n'
    local response

    response=$(env COMP_WORDS="${COMP_WORDS[*]}" COMP_CWORD=$COMP_CWORD \
%(complete_var)s=bash_complete $1)

    for completion in $response; do
        IFS=',' read type value <<< "$completion"

        if [[ $type == 'dir' ]]; then
            COMREPLY=()
            compopt -o dirnames
        elif [[ $type == 'file' ]]; then
            COMREPLY=()
            compopt -o default
        elif [[ $type == 'plain' ]]; then
            COMPREPLY+=($value)
        fi
    done

    return 0
}

%(complete_func)s_setup() {
    complete -o nosort -F %(complete_func)s %(prog_name)s
}

%(complete_func)s_setup;
"""

_SOURCE_ZSH = """\
#compdef %(prog_name)s

%(complete_func)s() {
    local -a completions
    local -a completions_with_descriptions
    local -a response
    (( ! $+commands[%(prog_name)s] )) && return 1

    response=("${(@f)$(env COMP_WORDS="${words[*]}" COMP_CWORD=$((CURRENT-1)) \
%(complete_var)s=zsh_complete %(prog_name)s)}")

    for type key descr in ${response}; do
        if [[ "$type" == "plain" ]]; then
            if [[ "$descr" == "_" ]]; then
                completions+=("$key")
            else
                completions_with_descriptions+=("$key":"$descr")
            fi
        elif [[ "$type" == "dir" ]]; then
            _path_files -/
        elif [[ "$type" == "file" ]]; then
            _path_files -f
        fi
    done

    if [ -n "$completions_with_descriptions" ]; then
        _describe -V unsorted completions_with_descriptions -U
    fi

    if [ -n "$completions" ]; then
        compadd -U -V unsorted -a completions
    fi
}

compdef %(complete_func)s %(prog_name)s;
"""

_SOURCE_FISH = """\
function %(complete_func)s;
    set -l response;

    for value in (env %(complete_var)s=fish_complete COMP_WORDS=(commandline -cp) \
COMP_CWORD=(commandline -t) %(prog_name)s);
        set response $response $value;
    end;

    for completion in $response;
        set -l metadata (string split "," $completion);

        if test $metadata[1] = "dir";
            __fish_complete_directories $metadata[2];
        else if test $metadata[1] = "file";
            __fish_complete_path $metadata[2];
        else if test $metadata[1] = "plain";
            echo $metadata[2];
        end;
    end;
end;

complete --no-files --command %(prog_name)s --arguments \
"(%(complete_func)s)";
"""


class ShellComplete:
    """Base class for providing shell completion support. A subclass for
    a given shell will override attributes and methods to implement the
    completion instructions (``source`` and ``complete``).

    :param cli: Command being called.
    :param prog_name: Name of the executable in the shell.
    :param complete_var: Name of the environment variable that holds
        the completion instruction.

    """

    name = None
    """Name to register the shell as with :func:`add_completion_class`.
    This is used in completion instructions (``{name}_source`` and
    ``{name}_complete``).
    """
    source_template = None
    """Completion script template formatted by :meth:`source`. This must
    be provided by subclasses.
    """

    def __init__(self, cli, ctx_args, prog_name, complete_var):
        self.cli = cli
        self.ctx_args = ctx_args
        self.prog_name = prog_name
        self.complete_var = complete_var

    @property
    def func_name(self):
        """The name of the shell function defined by the completion
        script.
        """
        safe_name = re.sub(r"\W*", "", self.prog_name.replace("-", "_"), re.ASCII)
        return f"_{safe_name}_completion"

    def source_vars(self):
        """Vars for formatting :attr:`source_template`.

        By default this provides ``complete_func``, ``complete_var``,
        and ``prog_name``.
        """
        return {
            "complete_func": self.func_name,
            "complete_var": self.complete_var,
            "prog_name": self.prog_name,
        }

    def source(self):
        """Produce the shell script that defines the completion
        function. By default this ``%``-style formats
        :attr:`source_template` with the dict returned by
        :meth:`source_vars`.
        """
        return self.source_template % self.source_vars()

    def get_completion_args(self):
        """Use the env vars defined by the shell script to return a
        tuple of ``args, incomplete``. This must be implemented by
        subclasses.
        """
        raise NotImplementedError

    def get_completions(self, args, incomplete):
        """Determine the context and last complete command or parameter
        from the complete args. Call that object's ``shell_complete``
        method to get the completions for the incomplete value.

        :param args: List of complete args before the incomplete value.
        :param incomplete: Value being completed. May be empty.
        """
        ctx = _resolve_context(self.cli, self.ctx_args, self.prog_name, args)

        if ctx is None:
            return []

        obj, incomplete = _resolve_incomplete(ctx, args, incomplete)
        return obj.shell_complete(ctx, incomplete)

    def format_completion(self, item):
        """Format a completion item into the form recognized by the
        shell script. This must be implemented by subclasses.

        :param item: Completion item to format.
        """
        raise NotImplementedError

    def complete(self):
        """Produce the completion data to send back to the shell.

        By default this calls :meth:`get_completion_args`, gets the
        completions, then calls :meth:`format_completion` for each
        completion.
        """
        args, incomplete = self.get_completion_args()
        completions = self.get_completions(args, incomplete)
        out = [self.format_completion(item) for item in completions]
        return "\n".join(out)


class BashComplete(ShellComplete):
    """Shell completion for Bash."""

    name = "bash"
    source_template = _SOURCE_BASH

    def _check_version(self):
        import subprocess

        output = subprocess.run(["bash", "--version"], stdout=subprocess.PIPE)
        match = re.search(r"version (\d)\.(\d)\.\d", output.stdout.decode())

        if match is not None:
            major, minor = match.groups()

            if major < "4" or major == "4" and minor < "4":
                raise RuntimeError(
                    "Shell completion is not supported for Bash"
                    " versions older than 4.4."
                )
        else:
            raise RuntimeError(
                "Couldn't detect Bash version, shell completion is not supported."
            )

    def source(self):
        self._check_version()
        return super().source()

    def get_completion_args(self):
        cwords = split_arg_string(os.environ["COMP_WORDS"])
        cword = int(os.environ["COMP_CWORD"])
        args = cwords[1:cword]

        try:
            incomplete = cwords[cword]
        except IndexError:
            incomplete = ""

        return args, incomplete

    def format_completion(self, item: CompletionItem):
        return f"{item.type},{item.value}"


class ZshComplete(ShellComplete):
    """Shell completion for Zsh."""

    name = "zsh"
    source_template = _SOURCE_ZSH

    def get_completion_args(self):
        cwords = split_arg_string(os.environ["COMP_WORDS"])
        cword = int(os.environ["COMP_CWORD"])
        args = cwords[1:cword]

        try:
            incomplete = cwords[cword]
        except IndexError:
            incomplete = ""

        return args, incomplete

    def format_completion(self, item: CompletionItem):
        return f"{item.type}\n{item.value}\n{item.help if item.help else '_'}"


class FishComplete(ShellComplete):
    """Shell completion for Fish."""

    name = "fish"
    source_template = _SOURCE_FISH

    def get_completion_args(self):
        cwords = split_arg_string(os.environ["COMP_WORDS"])
        incomplete = os.environ["COMP_CWORD"]
        args = cwords[1:]

        # Fish stores the partial word in both COMP_WORDS and
        # COMP_CWORD, remove it from complete args.
        if incomplete and args and args[-1] == incomplete:
            args.pop()

        return args, incomplete

    def format_completion(self, item: CompletionItem):
        if item.help:
            return f"{item.type},{item.value}\t{item.help}"

        return f"{item.type},{item.value}"


_available_shells = {
    "bash": BashComplete,
    "fish": FishComplete,
    "zsh": ZshComplete,
}


def add_completion_class(cls, name=None):
    """Register a :class:`ShellComplete` subclass under the given name.
    The name will be provided by the completion instruction environment
    variable during completion.

    :param cls: The completion class that will handle completion for the
        shell.
    :param name: Name to register the class under. Defaults to the
        class's ``name`` attribute.
    """
    if name is None:
        name = cls.name

    _available_shells[name] = cls


def get_completion_class(shell):
    """Look up a registered :class:`ShellComplete` subclass by the name
    provided by the completion instruction environment variable. If the
    name isn't registered, returns ``None``.

    :param shell: Name the class is registered under.
    """
    return _available_shells.get(shell)


def _is_incomplete_argument(ctx, param):
    """Determine if the given parameter is an argument that can still
    accept values.

    :param ctx: Invocation context for the command represented by the
        parsed complete args.
    :param param: Argument object being checked.
    """
    if not isinstance(param, Argument):
        return False

    value = ctx.params[param.name]
    return (
        param.nargs == -1
        or ctx.get_parameter_source(param.name) is not ParameterSource.COMMANDLINE
        or (
            param.nargs > 1
            and isinstance(value, (tuple, list))
            and len(value) < param.nargs
        )
    )


def _start_of_option(value):
    """Check if the value looks like the start of an option."""
    return value and not value[0].isalnum()


def _is_incomplete_option(args, param):
    """Determine if the given parameter is an option that needs a value.

    :param args: List of complete args before the incomplete value.
    :param param: Option object being checked.
    """
    if not isinstance(param, Option):
        return False

    if param.is_flag:
        return False

    last_option = None

    for index, arg in enumerate(reversed(args)):
        if index + 1 > param.nargs:
            break

        if _start_of_option(arg):
            last_option = arg

    return last_option is not None and last_option in param.opts


def _resolve_context(cli, ctx_args, prog_name, args):
    """Produce the context hierarchy starting with the command and
    traversing the complete arguments. This only follows the commands,
    it doesn't trigger input prompts or callbacks.

    :param cli: Command being called.
    :param prog_name: Name of the executable in the shell.
    :param args: List of complete args before the incomplete value.
    """
    ctx_args["resilient_parsing"] = True
    ctx = cli.make_context(prog_name, args.copy(), **ctx_args)
    args = ctx.protected_args + ctx.args

    while args:
        if isinstance(ctx.command, MultiCommand):
            if not ctx.command.chain:
                name, cmd, args = ctx.command.resolve_command(ctx, args)

                if cmd is None:
                    return ctx

                ctx = cmd.make_context(name, args, parent=ctx, resilient_parsing=True)
                args = ctx.protected_args + ctx.args
            else:
                while args:
                    name, cmd, args = ctx.command.resolve_command(ctx, args)

                    if cmd is None:
                        return ctx

                    sub_ctx = cmd.make_context(
                        name,
                        args,
                        parent=ctx,
                        allow_extra_args=True,
                        allow_interspersed_args=False,
                        resilient_parsing=True,
                    )
                    args = sub_ctx.args

                ctx = sub_ctx
                args = sub_ctx.protected_args + sub_ctx.args
        else:
            break

    return ctx


def _resolve_incomplete(ctx, args, incomplete):
    """Find the quo object that will handle the completion of the
    incomplete value. Return the object and the incomplete value.

    :param ctx: Invocation context for the command represented by
        the parsed complete args.
    :param args: List of complete args before the incomplete value.
    :param incomplete: Value being completed. May be empty.
    """
    # Different shells treat an "=" between a long option name and
    # value differently. Might keep the value joined, return the "="
    # as a separate item, or return the split name and value. Always
    # split and discard the "=" to make completion easier.
    if incomplete == "=":
        incomplete = ""
    elif "=" in incomplete and _start_of_option(incomplete):
        name, _, incomplete = incomplete.partition("=")
        args.append(name)

    # The "--" marker tells quo to stop treating values as options
    # even if they start with the option character. If it hasn't been
    # given and the incomplete arg looks like an option, the current
    # command will provide option name completions.
    if "--" not in args and _start_of_option(incomplete):
        return ctx.command, incomplete

    params = ctx.command.get_params(ctx)

    # If the last complete arg is an option name with an incomplete
    # value, the option will provide value completions.
    for param in params:
        if _is_incomplete_option(args, param):
            return param, incomplete

    # It's not an option name or value. The first argument without a
    # parsed value will provide value completions.
    for param in params:
        if _is_incomplete_argument(ctx, param):
            return param, incomplete

    # There were no unparsed arguments, the command may be a group that
    # will provide command name completions.
    return ctx.command, incomplete




INVALID_HANDLE_VALUE = HANDLE(-1).value
ERROR_NO_MORE_FILES = 18
ERROR_INSUFFICIENT_BUFFER = 122
TH32CS_SNAPPROCESS = 2
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000


kernel32 = ctypes.windll.kernel32


def _check_handle(error_val=0):
    def check(ret, func, args):
        if ret == error_val:
            raise ctypes.WinError()
        return ret

    return check


def _check_expected(expected):
    def check(ret, func, args):
        if ret:
            return True
        code = ctypes.GetLastError()
        if code == expected:
            return False
        raise ctypes.WinError(code)

    return check


class ProcessEntry32(ctypes.Structure):
    _fields_ = (
        ("dwSize", DWORD),
        ("cntUsage", DWORD),
        ("th32ProcessID", DWORD),
        ("th32DefaultHeapID", ctypes.POINTER(ULONG)),
        ("th32ModuleID", DWORD),
        ("cntThreads", DWORD),
        ("th32ParentProcessID", DWORD),
        ("pcPriClassBase", LONG),
        ("dwFlags", DWORD),
        ("szExeFile", CHAR * MAX_PATH),
    )


kernel32.CloseHandle.argtypes = [HANDLE]
kernel32.CloseHandle.restype = BOOL

kernel32.CreateToolhelp32Snapshot.argtypes = [DWORD, DWORD]
kernel32.CreateToolhelp32Snapshot.restype = HANDLE
kernel32.CreateToolhelp32Snapshot.errcheck = _check_handle(  # type: ignore
    INVALID_HANDLE_VALUE,
)

kernel32.Process32First.argtypes = [HANDLE, ctypes.POINTER(ProcessEntry32)]
kernel32.Process32First.restype = BOOL
kernel32.Process32First.errcheck = _check_expected(  # type: ignore
    ERROR_NO_MORE_FILES,
)

kernel32.Process32Next.argtypes = [HANDLE, ctypes.POINTER(ProcessEntry32)]
kernel32.Process32Next.restype = BOOL
kernel32.Process32Next.errcheck = _check_expected(  # type: ignore
    ERROR_NO_MORE_FILES,
)

kernel32.GetCurrentProcessId.argtypes = []
kernel32.GetCurrentProcessId.restype = DWORD

kernel32.OpenProcess.argtypes = [DWORD, BOOL, DWORD]
kernel32.OpenProcess.restype = HANDLE
kernel32.OpenProcess.errcheck = _check_handle(  # type: ignore
    INVALID_HANDLE_VALUE,
)

kernel32.QueryFullProcessImageNameW.argtypes = [HANDLE, DWORD, LPWSTR, PDWORD]
kernel32.QueryFullProcessImageNameW.restype = BOOL
kernel32.QueryFullProcessImageNameW.errcheck = _check_expected(  # type: ignore
    ERROR_INSUFFICIENT_BUFFER,
)


@contextlib.contextmanager
def _handle(f, *args, **kwargs):
    handle = f(*args, **kwargs)
    try:
        yield handle
    finally:
        kernel32.CloseHandle(handle)


def _iter_processes():
    f = kernel32.CreateToolhelp32Snapshot
    with _handle(f, TH32CS_SNAPPROCESS, 0) as snap:
        entry = ProcessEntry32()
        entry.dwSize = ctypes.sizeof(entry)
        ret = kernel32.Process32First(snap, entry)
        while ret:
            yield entry
            ret = kernel32.Process32Next(snap, entry)


def _get_full_path(proch):
    size = DWORD(MAX_PATH)
    while True:
        path_buff = ctypes.create_unicode_buffer("", size.value)
        if kernel32.QueryFullProcessImageNameW(proch, 0, path_buff, size):
            return path_buff.value
        size.value *= 2


def get_shell(pid=None, max_depth=10):
    proc_map = {
        proc.th32ProcessID: (proc.th32ParentProcessID, proc.szExeFile)
        for proc in _iter_processes()
    }
    pid = pid or os.getpid()

    for _ in range(0, max_depth + 1):
        try:
            ppid, executable = proc_map[pid]
        except KeyError:  # No such process? Give up.
            break

        # The executable name would be encoded with the current code page if
        # we're in ANSI mode (usually). Try to decode it into str/unicode,
        # replacing invalid characters to be safe (not thoeratically necessary,
        # I think). Note that we need to use 'mbcs' instead of encoding
        # settings from sys because this is from the Windows API, not Python
        # internals (which those settings reflect). (pypa/pipenv#3382)
        if isinstance(executable, bytes):
            executable = executable.decode("mbcs", "replace")

        name = executable.rpartition(".")[0].lower()
        if name not in SHELL_NAMES:
            pid = ppid
            continue

        key = PROCESS_QUERY_LIMITED_INFORMATION
        with _handle(kernel32.OpenProcess, key, 0, pid) as proch:
            return (name, _get_full_path(proch))

    return None

def shelldetector(pid=None, max_depth=10):
    name = os.name
    try:
        impl = importlib.import_module(".{}".format(name), __name__)
    except ImportError:
        message = "Shell detection not implemented for {0!r}".format(name)
        raise RuntimeError(message)
    try:
        get_shell = impl.get_shell
    except AttributeError:
        raise RuntimeError("get_shell not implemented for {0!r}".format(name))
    shell = get_shell(pid, max_depth=max_depth)
    if shell:
        return shell
    raise ShellDetectionFailure() 
