import abc
import typing

# Decoy to avoid circular imports

from quo.document import Document
from quo.text.core import StyleAndTextTuples, Textual


class Completion:
    """
    NOTE: Decoy class to avoid circular imports
    """

    def __init__(
        self,
        text: str,
        start_position: int = 0,
        display: typing.Optional[Textual] = None,
        display_meta: typing.Optional[Textual] = None,
        style: str = "",
        selected_style: str = "",
    ) -> None:

        from quo.text import to_formatted_text

        self.text = text
        self.start_position = start_position
        self._display_meta = display_meta

        if display is None:
            display = text

        self.display = to_formatted_text(display)

        self.style = style
        self.selected_style = selected_style

        assert self.start_position <= 0

    def __repr__(self) -> str:
        if isinstance(self.display, str) and self.display == self.text:
            return "%s(text=%r, start_position=%r)" % (
                self.__class__.__name__,
                self.text,
                self.start_position,
            )
        else:
            return "%s(text=%r, start_position=%r, display=%r)" % (
                self.__class__.__name__,
                self.text,
                self.start_position,
                self.display,
            )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Completion):
            return False
        return (
            self.text == other.text
            and self.start_position == other.start_position
            and self.display == other.display
            and self._display_meta == other._display_meta
        )

    def __hash__(self) -> int:
        return hash((self.text, self.start_position, self.display, self._display_meta))

    @property
    def display_text(self) -> str:
        "The 'display' field as plain text."
        from quo.text import fragment_list_to_text

        return fragment_list_to_text(self.display)
    @property
    def display_meta(self) -> StyleAndTextTuples:
        "Return meta-text. (This is lazy when using a callable)."
        from quo.text import to_formatted_text

        return to_formatted_text(self._display_meta or "")

    @property
    def display_meta_text(self) -> str:
        "The 'meta' field as plain text."
        from quo.text import fragment_list_to_text

        return fragment_list_to_text(self.display_meta)

    def new_completion_from_position(self, position: int) -> "Completion":
        """
        (Only for internal use!)
        Get a new completion by splitting this one. Used by `Application` when
        it needs to have a list of new completions after inserting the common
        prefix.
        """
        assert position - self.start_position >= 0

        return Completion(
            text=self.text[position - self.start_position :],
            display=self.display,
            display_meta=self._display_meta,
        )


class CompleteEvent:
    """
    Event that called the completer.

    :param text_inserted: When True, it means that completions are requested
        because of a text insert. (`Buffer.complete_while_typing`.)
    :param completion_requested: When True, it means that the user explicitly
        pressed the `Tab` key in order to view the completions.

    These two flags can be used for instance to implement a completer that
    shows some completions when ``Tab`` has been pressed, but not
    automatically when the user presses a space. (Because of
    `complete_while_typing`.)
    """

    def __init__(
        self, text_inserted: bool = False, completion_requested: bool = False
    ) -> None:
        assert not (text_inserted and completion_requested)

        #: Automatic completion while typing.
        self.text_inserted = text_inserted

        #: Used explicitly requested completion by pressing 'tab'.
        self.completion_requested = completion_requested

    def __repr__(self) -> str:
        return "%s(text_inserted=%r, completion_requested=%r)" % (
            self.__class__.__name__,
            self.text_inserted,
            self.completion_requested,
        )


class Completer(metaclass=abc.ABCMeta):
    """
    A decoy Base class for completer implementations to avoid circular imports
    """

    @abc.abstractmethod
    def get_completions(
        self, document: Document, complete_event: CompleteEvent
    ) -> typing.Iterable[Completion]:
        """
        This should be a generator that yields :class:`.Completion` instances.

        If the generation of completions is something expensive (that takes a
        lot of time), consider wrapping this `Completer` class in a
        `ThreadedCompleter`. In that case, the completer algorithm runs in a
        background thread and completions will be displayed as soon as they
        arrive.

        :param document: :class:`~prompt_toolkit.document.Document` instance.
        :param complete_event: :class:`.CompleteEvent` instance.
        """
        while False:
            yield

    async def get_completions_async(
        self, document: Document, complete_event: CompleteEvent
    ) -> typing.AsyncGenerator[Completion, None]:
        """
        Asynchronous generator for completions. (Probably, you won't have to
        override this.)

        Asynchronous generator of :class:`.Completion` objects.
        """
        for item in self.get_completions(document, complete_event):
            yield item


def get_common_complete_suffix(
    document: Document, completions: typing.Sequence[Completion]
) -> str:
    """
    Return the common prefix for all completions.
    """
    # Take only completions that don't change the text before the cursor.
    def doesnt_change_before_cursor(completion: Completion) -> bool:
        end = completion.text[: -completion.start_position]
        return document.text_before_cursor.endswith(end)

    completions2 = [c for c in completions if doesnt_change_before_cursor(c)]

    # When there is at least one completion that changes the text before the
    # cursor, don't return any common part.
    if len(completions2) != len(completions):
        return ""

    # Return the common prefix.
    def get_suffix(completion: Completion) -> str:
        return completion.text[-completion.start_position :]

    return _commonprefix([get_suffix(c) for c in completions2])

