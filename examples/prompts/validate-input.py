import quo

session = quo.Prompt()


class NumberValidator(quo.validation.Validator):

    def validate(self, document):
        text = document.text

        if text and not text.isdigit():
            i = 0

            # Get index of first non numeric character.
            # We want to move the cursor here.

            for i, cursor in enumerate(text):
                if not cursor.isdigit():
                    break

                raise quo.errors.ValidationError(message='This input contains non-numeric characters', cursor_position=i)

number = int(session.prompt('Give a number: ', validator=NumberValidator()))

quo.echo('You said: %i' % number)
