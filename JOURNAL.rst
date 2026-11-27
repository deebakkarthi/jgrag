2026-11-27 12:55 PM
===================

Convert ``simp.html`` to a plain text file.

* ``html2text`` with its default settings doesn't give satisfactory results.
  It outputs things in markdown which is not what I want. Since, these
  documents won't be fed into the LLMs as such, I don't have to care about
  preserving *italicizing* or **bold text**. The output format I want is
  a simple text file with a single line containing lower cased letters.

        .. code-block:: python
        IGNORE_EMPHASIS = True
        IGNORE_IMAGES = True
        IGNORE_LINKS = True
        BYPASS_TABLES = True
        IGNORE_TABLES = True

  Accomplishes what I want. Now the result is just a plain text file with no
  markdown except for headings and ``inline code blocks``

2026-11-27 01:52 PM
===================

The next step is to normalize this. The regular NLP pipeline is
``"[a-z0-9+]".findall(str.lower())``. Which basically splits on
*non-alphanumerics* and discards them.

Though that is tempting to do, I want to preserve inline code and code blocks.
They have to be tokenized just on whitespace. I want to instruct the queries
to be structured in such a way too.

Example
-------

To search for `[ERROR VERILOG-69]` the query would be "`ERROR VERILOG-69`" with
the backquotes. Backquotes  would be used to indicate an roughly exact match.
That is why we want BM25 instead of any of these deep search methods.

Some preproc considerations
===========================

        .. code:: html
        <code>
        some_code
        </code>

becomes ` some_code`. There is a dangling space in the front. I don't want that.
Though it is the correct conversion. HTML actually does insert a space in
monopspace if there are newlines in ``<code>`` that are not inside a ``<pre>``.
Strip every code block to avoid this.

Tokenizer
=========

Lowercase and remove non-alphanumerics except for ``\`inline code blocks\```
and actual code blocks. I want to only split on whitespace inside those.

Example
-------
``\`check_cov -clock clk\``` becomes `["check_cov", "-clock", "clk"]`.

So I would need to first split non code blocks and code blocks.

Tokenizer vs Preprocessing
==========================

How to design this phase? Do I actually need the documents? The result of
this process is just an index. I don't need to store the preprocessed documents
right? 

So if I have a document as::
        
        I continue cooking, you and I both forget about Pinkman. We forget this
        ever happened. We consider this a lone hiccup in an otherwise long and
        fruitful business arrangement. I prefer Option B. 

        ```
        #include "aldor"
        #include "aldorio"
        #pile

        sumlist(R: ArithmeticType, l: List R): R == 
            s: R := 0;
            for x in l repeat s := s + x
            s

        import from List Integer, Integer, List SingleFloat, SingleFloat
        stdout << sumlist(Integer, [2,3,4,5]) << newline
        stdout << sumlist(SingleFloat, [2.0, 2.1, 2.2, 2.4]) << newline
        ```

Then I want to convert this into::

        
        i continue cooking you and i both forget about pinkman we forget this
        ever happened we consider this a lone hiccup in an otherwise long and
        fruitful business arrangement i prefer option b. #include "aldor"
        #include "aldorio" #pile sumlist(R: ArithmeticType, l: List R): R == s:
        R := 0; for x in l repeat s := s + x s import from List Integer,
        Integer, List SingleFloat, SingleFloat stdout << sumlist(Integer,
        [2,3,4,5]) << newline stdout << sumlist(SingleFloat, [2.0, 2.1, 2.2,
        2.4]) << newline

This would all be in one line. But the key thing is that the non-code block
text would all be exclusively lowercased alphanumerics but the code blocks
will preserve all of their content.

Do I really want this? If I applied the same tokenizer to the code blocks
then I won't really be missing any documents, right? I will simply get a super
set which would be better.

For instance if ``check -cov`` is converted to ``["check", "cov"]`` then any query
with ``check -cov`` will surely retrieve this document plus other that might
match. The retrieved document id will be used to get the ``html`` which would
fill in the appropriate context.

The case of the simpler tokenizer is that the index would be compact. I won't
have an entry for say ``clock,`` taking up space.

But a CEX for this is ``#include`` vs ``include```. These mean very different
things.

Hybrid approach
---------------

* Preserve capitalization of code blocks
* Remove trailing ``,``, ``;``
* Preserve hyphens, hashtags, etc.


Rationale
---------

``-coverage``, a flag one might search for, is very distinct from just
``coverage``. Hence it is important to preserve that ``-``. But all other
non-alphanumerics don't seem to be too important to preserve and their
removal won't hinder the search.

TODO(dbk)
---------

* Tokenizer
* Preprocessing

        * Separate code vs non-code blocks
        * lowercase, remove non-alphanumerics for the non-code block
        * code-blocks might need more logic

