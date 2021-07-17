from threading import local

_local = local()

# Access current context(s) 
def currentcontext(silent=False):
   
    try:
        return _local.stack[-1]
    except (AttributeError, IndexError):
        if not silent:
            raise RuntimeError("No dynamic content available.")

# Push new content to the stack
def push_context(clime):

    _local.__dict__.setdefault("stack", []).append(clime)

# Removes the top level from the stack
def pop_context():
    _local.stack.pop()

# Returns/gets the default value of color flag
def resolve_color_default(color=None):
 
    if color is not None:
        return color
    clime = currentcontext(silent=True)
    if clime is not None:
        return clime.color
