The Parser
----------

Taken from learning zil.pdf 
https://archive.org/details/Learning_ZIL_Steven_Eric_Meretzky_1995

and 
Benjamin Fan 
https://groups.google.com/g/rec.arts.int-fiction/c/VpsWZdWRnlA?pli=1

If the parser succeeds in digesting the input, it passes three pieces of
information on to the rest of the program: the verb, the direct object, and the
indirect object

>HIT UNCLE OTTO WITH THE HAMMER

You knock some sense back into Uncle Otto, and he stops
insisting that he's Napoleon Bonaparte.


Verb: Hit
Object: Uncle Otto
Indirect Object: Hammer

Not every input has an Indirect object.

In such a case,
when there is no Indirect object, the parser sets the value of Indirect object to false

not every input has a direct object. Some examples of inputs where both direct and indirect object
are false:
>YELL  
>PANIC  
>INVENTORY  
<p>Note that you cannot have an indirect object without also having a direct object. Also note that
every valid input starts with a verb/action.</p>


Theory of Parser Construction
-----------------------------

For our purposes, "parsing" is defined as taking some input and
converting it into some output.  In Interactive Fiction (IF), the
input is what the player types onto the command line ("drop the
lantern"), and the output is some representation that is usable by the
underlying game system.

Unfortunately, much of what has been written about parsers is in
the context of reading computer programs (such as C and Java) and
translating them into a runnable form (an executable file or Java
bytecode).  Because these computer languages are more complex than IF
input, these parser texts tend to be overly complex.

### Traditionally, there are three steps in parsing:

1. **Lexical Analysis:**  This involves reading the source and breaking
them down into "tokens".  Tokens are sequences of characters which
represent a logical unit with some underlying meaning.  There are
programs available (LEX and FLEX) which can be used to construct a
lexical analyzer program.

     Here are some examples.  In the Java program line "if (counter ==
99)", the six tokens would be "if", "(", "counter", "==", "99", and
")".  For example, in the sentence "drop the lantern" the tokens would
be the three individual words "drop", "the", and "lantern".

2. **Syntactical Analysis:**.  This involves taking the sequence of tokens
and seeing whether the sequence matches certain patterns known to be a
correct sentence in some particular language.  This set of patterns or
rules of a language is known as a "grammar".  Syntactical analysis
usually involves taking the input tokens, the dictionary of all
possible tokens, and a grammar of the language and parsing them into a
data structure known as a "parse tree".  There are several techniques
which can be used to do this.  There are also programs available (YACC
and Bison) which can be used to construct a syntactical analyzer
program.

3. **Translation:**.  This involves taking the parse tree and translating
its contents into a form usable by the machine or interpreter.  In
terms of IF, the translator might be used convert the parse tree into
a canonical command.  For example, the commands "hang the cloak",
"drop cloak", "put the cloak on the hook" might all get translated
into a canonical "PUT CLOAK" command that the IF program can use.

Grammar Rules
-------------

Rule 0: The dictionary of all possible verbs, adjectives, direct
        objects, and indirect objects is *not* known.
Rule 1: The first word of the input is always a verb.
Rule 2: Indirect object phrases are always preceded by a preposition.
Rule 3: Direct object phrases are always positioned before indirect
        object phrases.
Rule 4: The dictionary of all possible prepositions is known.
Rule 5: The dictionary of all possible articles is known.


-----------------------------------------------------------------------------------

Here are some design notes for a proposed IF parser, possibly for
use with JIGSAW.  They might be helpful for people who are thinking of
writing their own parser.  
     Currently, the existing JIGSAW parser handles one- and two-word
input only.  The proposed parser handles commands as complex as "put
the velvet cloak on the brass hook".  The proposed parser is still not
very complex, but it should be sufficiently complex enough for IF
purposes.  The main "feature" of the parser is that it can be compiled
and used to parse commands without pre-knowledge of all the words in
the game's dictionary.  I'm not sure whether this is a worthwhile
goal.

     Because this type of parser may not be easily adaptable for
globalization into other languages, I am not sure whether it is worth
implementing.  Is a two-word parser good enough?

     The text in this posting is an excerpt-- the full text of the
notes is included but the text of the GNU FDL license is omitted.

Ben


JIGSAW Parser Notes
   or
Construction of a Generic Interactive Fiction Parser Which Works Even
When the Dictionary of All Words Is Not Known Beforehand

Copyright (c) 2002 Benjamin Fan

Permission is granted to copy, distribute and/or modify this document
under the terms of the GNU Free Documentation License, Version 1.2;
with no Invariant Sections, with no Front-Cover Texts, and with no
Back-Cover Texts. A copy of the license is included in the section
entitled "GNU Free Documentation License".
   
For excerpts which omit the full text of the GNU Free Documentation
License, the license text can be found at
http://www.gnu.org/licenses/fdl.html
 
Theory of Parser Construction
-----------------------------

     For our purposes, "parsing" is defined as taking some input and
converting it into some output.  In Interactive Fiction (IF), the
input is what the player types onto the command line ("drop the
lantern"), and the output is some representation that is usable by the
underlying game system.

     Unfortunately, much of what has been written about parsers is in
the context of reading computer programs (such as C and Java) and
translating them into a runnable form (an executable file or Java
bytecode).  Because these computer languages are more complex than IF
input, these parser texts tend to be overly complex.

     Traditionally, there are three steps in parsing:

1. Lexical Analysis.  This involves reading the source and breaking
them down into "tokens".  Tokens are sequences of characters which
represent a logical unit with some underlying meaning.  There are
programs available (LEX and FLEX) which can be used to construct a
lexical analyzer program.

     Here are some examples.  In the Java program line "if (counter ==
99)", the six tokens would be "if", "(", "counter", "==", "99", and
")".  For example, in an sentence "drop the lantern" the tokens would
be the three individual words "drop", "the", and "lantern".

2. Syntactical Analysis.  This involves taking the sequence of tokens
and seeing whether the sequence matches certain patterns known to be a
correct sentence in some particular language.  This set of patterns or
rules of a language is known as a "grammar".  Syntactical analysis
usually involves taking the input tokens, the dictionary of all
possible tokens, and a grammar of the language and parsing them into a
data structure known as a "parse tree".  There are several techniques
which can be used to do this.  There are also programs available (YACC
and Bison) which can be used to construct a syntactical analyzer
program.

3. Translation.  This involves taking the parse tree and translating
its contents into a form usable by the machine or interpreter.  In
terms of IF, the translator might be used convert the parse tree into
a canonical command.  For example, the commands "hang the cloak",
"drop cloak", "put the cloak on the hook" might all get translated
into a canonical "PUT CLOAK" command that the IF program can use.


IF Parsing Without Knowing the Dictionary
-----------------------------------------

     Fortunately, IF input is similar to written language so lexical
analysis is simple.  The tokens are the words separated by whitespace
(or possibly punctuation).  Because of these rules, it is not
necessary to know the dictionary of all possible tokens beforehand.

     Because IF input is limited to only a few patterns, it may be
possible to parse the input by simply looking at the word position of
the input.  More importantly, this would allow a generic parser to be
written without first knowing the dictionary of all possible words.
We will refer to this method of parsing as "Word Positional Parsing".

     It is acknowledged that this type of parser may work for certain
languages only (such as English).  For other languages (such as
Spanish), the sentence grammar will be different.  For each language,
a different parser will need to be written to accommodate the
different word orders and sentence constructions.  As an example, in
Spanish, "velvet cloak" translates to "capote del terciopelo".

     (Is it possible for a traditional parser produced by Bison to
parse our Interactive Fiction Grammar?  The tricky part is that the
dictionary of the language is not known by the parser.)


Grammar Rules
-------------

Rule 0: The dictionary of all possible verbs, adjectives, direct
        objects, and indirect objects is *not* known.
Rule 1: The first word of the input is always a verb.
Rule 2: Indirect object phrases are always preceded by a preposition.
Rule 3: Direct object phrases are always positioned before indirect
        object phrases.
Rule 4: The dictionary of all possible prepositions is known.
Rule 5: The dictionary of all possible articles is known.


Interactive Fiction Grammar
---------------------------

IFG := VERB_PHRASE DIRECT_OBJECT_PHRASE? INDIRECT_OBJECT_PHRASE?
   or
IFG := S0 | S1 | S2 | S3

Words

WORD := [:alpha:]+

Sentences

S0. verb
    (look, quit)
    S0 := V0

S1. verb (any direct object phrase)
    (hang the cloak, examine message)
    S1 := V0 ( D0 | D1 | D2 | D3 )

S2. verb (any indirect object phrase)
    (look under the table)
    S2 := V0 ( I0 | I1 | I2 | I3 )

S3. verb (any direct object phrase) (any indirect object phrase)
    (put the velvet cloak on the brass hook)
    S3 := V0 ( D0 | D1 | D2 | D3 ) ( I0 | I1 | I2 | I3 )

Verb Phrases

VERB_PHRASE := V0

V0. "verb" 
    (north, n, look, quit) 
    V0 := WORD

Direct Object Phrases

DIRECT_OBJECT_PHRASE :=  ARTICLE? WORD? WORD
   or
DIRECT_OBJECT_PHRASE := D0 | D1 | D2 | D3

D0. "direct_object"
    (message, cloak, lantern)
    D0 := WORD

D1. "article direct_object"
    (the message, the cloak, a lantern)
    ARTICLE := a | an | the
    D1 := ARTICLE WORD

D2. "adjective direct_object"
    (scrawled message, velvet cloak, brass lantern)
    D2 := WORD WORD

D3. "article adjective direct_object"
    (the scrawled message, the velvet cloak)
    D3 := ARTICLE WORD WORD

Indirect Object Phrases

INDIRECT_OBJECT_PHRASE :=  PREPOSITION ARTICLE? WORD? WORD
   or
INDIRECT_OBJECT_PHRASE := I0 | I1 | I2 | I3

I0. "preposition indirect_object"
    (under table, on hook, in box)
    PREPOSITION = on | under | in | to | around | inside | outside |
                  underneath | through | into 
    I0 := PREPOSITION WORD

I1. "preposition article indirect_object"
    (under the table, on the hook, in the box)
    I1 := PREPOSITION ARTICLE WORD

I2. "preposition adjective indirect_object"
    (under wooden table, on brass hook, in blue box)
    I2 := PREPOSITION WORD WORD

I3. "preposition article adjective indirect_object" 
    (under the wooden table, on the brass hook, in the blue box)
    I3 := PREPOSITION ARTICLE WORD WORD


English Sentences Specifically Not in Our IF Grammar

X0. "verb preposition"
    (go around, look under)

X1. "verb conjunction verb"
    (look and wait)

X2. "verb adverb"
    (look quickly)

X3. "verb direct object, direct object, direct object"
    (drop keys, lantern, food)

Notes on the Interactive Fiction Grammar

     More properly, modifiers should be specified as "any word except
for known articles or prepositions".  That is, "a cat" should be
parsed as D1, and it should not be parsed as D2.  I'm not sure how to
specify this in BNF or a regular expression.

     The grammar could be expanded to include prepositional phrases
such as "on top of".


Interactive Fiction Parser Algorithm
------------------------------------

X. Assuming that words are separated by whitespace and that all
   punctuation has been stripped from the input...

0. The first word is a verb.  Remove it and parse the rest of the
   input.

1. Scan for a preposition.  If one is found, remove it.  Parse the
   input preceding the preposition as a direct object phrase.  Parse
   the input following the preposition as an indirect object phrase.

Both direct and indirect object phrases are parsed using the same
algorithm:

2. Scan for an article.  If one is found, remove it and parse the rest
   of the input.

3. The last word in the input is the object.  Remove it and parse the
   rest of the input.

4. If any input remains, they are adjectives which modify the object.
   According to our grammar there can be only one adjective per
   object, so there should be only one word left in the input.
   However, this algorithm can be expanded easily to accommodate
   multiple adjectives.