#!/usr/bin/env python
"""
Example of printing colored text to the output.
"""
import time
import asyncio
import concurrent.futures
import multiprocessing
from quo import print
from quo.text import FormattedText
from quo.style import Style

async def main():
    style = Style.add(
        {
            "hello": "#ff0066",
            "world": "#44ff44 italic",
        }
    )

    # Print using a a list of text fragments.
    text_fragments = FormattedText(
        [
            ("class:hello", "Hello "),
            ("class:world", "World"),
            ("", "\n"),
        ]
    )
    async def ok(text_fragments, style):
        async with text_framents as txt:
            print(txt,  style=style)

    async def oks(dits):
        tasks = []
        task = asyncio.ensure_future(ok(text_fragments,style))
        tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)

def asyc_tasks(dits):
    asyncio.get_event_loop().run_until_complete(ok(dits))



       # with multiprocessing.Pool() as pool:
         #   pool.map(ok, dits)
    #print(text_fragments, style=style)

    # Print using an HTML object.
    print("<hello>hello</hello> <world>world</world>\n", style=style)

    # Print using an HTML object with inline styling.
    print('<style fg="#ff0066">hello</style> '
            '<style fg="#44ff44"><i>world</i></style>\n'
        )

if __name__ == "__main__":
    start = time.time()
    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as ex:
        futures = [ex.submit(asyc_tasks)]
        for future in concurrent.futures.as_completed(futures):
            pass
    duration = time.time() - start
    print(f"Duration {duration}")
