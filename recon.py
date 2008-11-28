#!/usr/bin/env python
# Regular expression test console
# By Brent Burley, 2001, erburley@ix.netcom.com
# This software is placed into the public domain
# Revision date: June 6, 2001

from Tkinter import *
import re

class Recon(Frame):
    def __init__(self, parent=None):
	# main frame
	Frame.__init__(self, parent)
	font = ('Courier', 14)
	f = Frame(self)
	f.pack(expand=YES, fill=BOTH)
	Label(f, text="Result:").grid(row=0, column=0, sticky=NE)
	Label(f, text="Text:").grid(row=1, column=0, sticky=NE)
	Label(f, text="Regex:").grid(row=2, column=0, sticky=E)
	self.result = Text(f, height=10, width=60, font=font)
	self.result.grid(row=0, column=1, sticky=NSEW)
	self.result.tag_configure('bold', foreground='blue', 
				  font=('Courier bold', 14))
	self.textEntry = Text(f, height=10, width=60, font=font)
	self.textEntry.grid(row=1, column=1, sticky=NSEW)
	self.reEntry = Entry(f, width=60, font=font)
	self.reEntry.grid(row=2, column=1, sticky=EW)
	f.grid_rowconfigure(0, weight=1)
	f.grid_rowconfigure(1, weight=1)
	f.grid_columnconfigure(1, weight=1)

	# option frame
	fo = Frame(f)
	fo.grid(row=3, column=1, sticky=W)
	self.opts = {}
	for o in ('IGNORECASE', 'LOCALE', 'MULTILINE', 'DOTALL', 'VERBOSE'):
	    var = IntVar()
	    Checkbutton(fo, text=o, variable=var).pack(side=LEFT)
	    self.opts[o] = (var, eval('re.'+o))
	self.findall = IntVar()
	Checkbutton(fo, text='Find All', variable=self.findall).pack(side=LEFT)

	# button frame
	fb = Frame(f)
	fb.grid(row=4, column=1, sticky=W)
	Button(fb, text="Evaluate", command=self.evaluate).pack(side=LEFT)
	Button(fb, text="Syntax Help", command=self.syntaxHelp).pack(side=LEFT)
	Button(fb, text="Flags Help", command=self.flagsHelp).pack(side=LEFT)
	Button(fb, text="Quit", command=self.quit).pack(side=LEFT)

	self.syntaxHelpWin = None
	self.flagsHelpWin = None
	self.result.insert(END, HelloText)

    def getFlags(self):
	flags = 0
	for o in self.opts.values():
	    if o[0].get(): flags = flags | o[1]
	return flags
	
    def evaluate(self):
	self.result.delete('0.0', END)
	text = self.textEntry.get('0.0', END)
	if len(text) and text[-1] == '\n': text = text[:len(text)-1]
	expr = self.reEntry.get()
	try:
	    r = re.compile(expr, self.getFlags())
	    m = r.search(text)
	except re.error, e:
	    self.result.insert(END, 'Error: ' + e[0])
	    return
	if not m:
	    self.result.insert(END, '(No match)')
	    return
	start = self.reportResult(m, text, 0)
	if self.findall.get():
	    while start < len(text):
		m = r.search(text, start)
		if not m: break
		start = self.reportResult(m, text, start)
	self.result.insert(END, text[start:])

    def reportResult(self, m, text, start):
	boundchars = "()"
	bounds = []
	for i in range(0, len(m.groups())+1):
	    s,e = m.start(i), m.end(i)
	    if s == -1 or e == -1: continue
	    bounds.append((s, 0))
	    bounds.append((e, 1))
	bounds.sort(lambda s1, s2: s1[0] - s2[0])
	index = start
	for b in bounds:
	    bindex = b[0]
	    self.result.insert(END, text[index:bindex])
	    self.result.insert(END, boundchars[b[1]], 'bold')
	    index = bindex
	if m.start() == m.end():
	    if index < len(text):
		self.result.insert(END, text[index])
	    index = index + 1
	return index

    def syntaxHelp(self):
	if not self.syntaxHelpWin:
	    self.syntaxHelpWin = HelpWindow(self, text=SyntaxHelpText)
	    self.syntaxHelpWin.title('Regular Expression Syntax')
	self.syntaxHelpWin.deiconify()
	self.syntaxHelpWin.tkraise()

    def flagsHelp(self):
	if not self.flagsHelpWin:
	    self.flagsHelpWin = HelpWindow(self, text=FlagsHelpText)
	    self.flagsHelpWin.title('Regular Expression Flags')
	self.flagsHelpWin.deiconify()
	self.flagsHelpWin.tkraise()

class HelpWindow(Toplevel):
    def __init__(self, parent=None, text='you need help'):
	Toplevel.__init__(self, parent)
	t = Text(self)
	t.insert(END, text)
	t.pack(side=LEFT, expand=YES, fill=BOTH)
	s = Scrollbar(self,command=t.yview)
	s.pack(expand=YES, fill=Y)
	t['yscrollcommand']=s.set
	self.protocol('WM_DELETE_WINDOW', self.withdraw)

HelloText = \
'''Welcome to Recon.

Type some text in the 'Text:' area below, then 
type a regular expression in the 'Regex:'
entry field and click on 'Evaluate'.  The
result of the match will appear here.
'''


SyntaxHelpText = \
r'''Regular expressions can contain both special and ordinary
characters. Most ordinary characters, like "A", "a", or "0", are the
simplest regular expressions; they simply match themselves. You can
concatenate ordinary characters, so last matches the string
'last'. (In the rest of this section, we'll write RE's in this special
style, usually without quotes, and strings to be matched 'in single
quotes'.)

Some characters, like "|" or "(", are special. Special characters
either stand for classes of ordinary characters, or affect how the
regular expressions around them are interpreted.

The special characters are: 

.	(Dot.) In the default mode, this matches any character except
	a newline. If the DOTALL flag has been specified, this matches
	any character including a newline.

^	(Caret.) Matches the start of the string, and in MULTILINE
	mode also matches immediately after each newline.

$ 	Matches the end of the string, and in MULTILINE mode also
	matches before a newline. foo matches both 'foo' and 'foobar',
	while the regular expression foo$ matches only 'foo'.

*	Causes the resulting RE to match 0 or more repetitions of the
	preceding RE, as many repetitions as are possible. ab* will
	match 'a', 'ab', or 'a' followed by any number of 'b's.

+	Causes the resulting RE to match 1 or more repetitions of the
	preceding RE. ab+ will match 'a' followed by any non-zero
	number of 'b's; it will not match just 'a'.

?	Causes the resulting RE to match 0 or 1 repetitions of the
	preceding RE. ab? will match either 'a' or 'ab'.

*?, +?, ??
	The "*", "+", and "?" qualifiers are all greedy; they match as
	much text as possible. Sometimes this behaviour isn't desired;
	if the RE <.*> is matched against '<H1>title</H1>', it will
	match the entire string, and not just '<H1>'. Adding "?" after
	the qualifier makes it perform the match in non-greedy or
	minimal fashion; as few characters as possible will be
	matched. Using .*? in the previous expression will match only
	'<H1>'.

{m,n}	Causes the resulting RE to match from m to n repetitions of
	the preceding RE, attempting to match as many repetitions as
	possible.  For example, a{3,5} will match from 3 to 5 "a"
	characters. Omitting n specifies an infinite upper bound; you
	can't omit m.

{m,n}?	Causes the resulting RE to match from m to n repetitions of
	the preceding RE, attempting to match as few repetitions as
	possible.  This is the non-greedy version of the previous
	qualifier. For example, on the 6-character string 'aaaaaa',
	a{3,5} will match 5 "a" characters, while a{3,5}? will only
	match 3 characters.

\	Either escapes special characters (permitting you to match
	characters like "*", "?", and so forth), or signals a special
	sequence; special sequences are discussed below.

	If you're not using a raw string to express the pattern,
	remember that Python also uses the backslash as an escape
	sequence in string literals; if the escape sequence isn't
	recognized by Python's parser, the backslash and subsequent
	character are included in the resulting string. However, if
	Python would recognize the resulting sequence, the backslash
	should be repeated twice. This is complicated and hard to
	understand, so it's highly recommended that you use raw
	strings for all but the simplest expressions.

[]	Used to indicate a set of characters. Characters can be listed
	individually, or a range of characters can be indicated by
	giving two characters and separating them by a "-". Special
	characters are not active inside sets. For example, [akm$]
	will match any of the characters "a", "k", "m", or "$"; [a-z]
	will match any lowercase letter, and [a-zA-Z0-9] matches any
	letter or digit. Character classes such as \w or \S(defined
	below) are also acceptable inside a range. If you want to
	include a "]" or a "-" inside a set, precede it with a
	backslash, or place it as the first character. The pattern []]
	will match ']', for example.

	You can match the characters not within a range by
	complementing the set. This is indicated by including a "^" as
	the first character of the set; "^" elsewhere will simply
	match the "^" character. For example, [^5] will match any
	character except "5".

|	A|B, where A and B can be arbitrary REs, creates a regular
	expression that will match either A or B. This can be used
	inside groups (see below) as well. To match a literal "|", use
	\|, or enclose it inside a character class, as in [|].

(...)	Matches whatever regular expression is inside the parentheses,
	and indicates the start and end of a group; the contents of a
	group can be retrieved after a match has been performed, and
	can be matched later in the string with the \number special
	sequence, described below. To match the literals "(" or "')",
	use \( or \), or enclose them inside a character class: [(]
	[)].

(?...)	This is an extension notation (a "?" following a "(" is not
	meaningful otherwise). The first character after the "?"
	determines what the meaning and further syntax of the
	construct is. Extensions usually do not create a new group;
	(?P<name>...) is the only exception to this rule. Following
	are the currently supported extensions.

(?iLmsx)
	(One or more letters from the set "i", "L", "m", "s", "x".)
	The group matches the empty string; the letters set the
	corresponding flags (re.I, re.L, re.M, re.S, re.X) for the
	entire regular expression. This is useful if you wish to
	include the flags as part of the regular expression, instead
	of passing a flag argument to the compile() function.

(?:...)	A non-grouping version of regular parentheses. Matches
	whatever regular expression is inside the parentheses, but the
	substring matched by the group cannot be retrieved after
	performing a match or referenced later in the pattern.

(?P<name>...)
	Similar to regular parentheses, but the substring matched by
	the group is accessible via the symbolic group name
	name. Group names must be valid Python identifiers. A symbolic
	group is also a numbered group, just as if the group were not
	named. So the group named 'id' in the example above can also
	be referenced as the numbered group 1.

	For example, if the pattern is (?P<id>[a-zA-Z_]\w*), the group
	can be referenced by its name in arguments to methods of match
	objects, such as m.group('id')or m.end('id'), and also by name
	in pattern text (e.g. (?P=id)) and replacement text (e.g.
	\g<id>).

(?P=name)
	Matches whatever text was matched by the earlier group named
	name.

(?#...)	A comment; the contents of the parentheses are simply ignored.

(?=...)	Matches if ... matches next, but doesn't consume any of the
	string. This is called a lookahead assertion. For example,
	Isaac (?=Asimov) will match 'Isaac ' only if it's followed by
	'Asimov'.

(?!...)	Matches if ... doesn't match next. This is a negative
	lookahead assertion. For example, Isaac (?!Asimov) will match
	'Isaac ' only if it's not followed by 'Asimov'.

The special sequences consist of "\" and a character from the list
below. If the ordinary character is not on the list, then the
resulting RE will match the second character. For example, \$ matches
the character "$".

\number	Matches the contents of the group of the same number. Groups
	are numbered starting from 1. For example, (.+) \1 matches
	'the the' or '55 55', but not 'the end' (note the space after
	the group). This special sequence can only be used to match
	one of the first 99 groups. If the first digit of number is 0,
	or number is 3 octal digits long, it will not be interpreted
	as a group match, but as the character with octal value
	number. Inside the "[" and "]" of a character class, all
	numeric escapes are treated as characters.

\A	Matches only at the start of the string.

\b	Matches the empty string, but only at the beginning or end of
	a word. A word is defined as a sequence of alphanumeric
	characters, so the end of a word is indicated by whitespace or
	a non-alphanumeric character. Inside a character range, \b
	represents the backspace character, for compatibility with
	Python's string literals.

\B	Matches the empty string, but only when it is not at the
	beginning or end of a word.

\d	Matches any decimal digit; this is equivalent to the set
	[0-9].

\D	Matches any non-digit character; this is equivalent to the set
	[^0-9].

\s	Matches any whitespace character; this is equivalent to the
	set [ \t\n\r\f\v].

\S	Matches any non-whitespace character; this is equivalent to
	the set [^ \t\n\r\f\v].

\w	When the LOCALE flag is not specified, matches any
	alphanumeric character; this is equivalent to the set
	[a-zA-Z0-9_]. With LOCALE, it will match the set [0-9_] plus
	whatever characters are defined as letters for the current
	locale.

\W	When the LOCALE flag is not specified, matches any
	non-alphanumeric character; this is equivalent to the set
	[^a-zA-Z0-9_].  With LOCALE, it will match any character not
	in the set [0-9_], and not defined as a letter for the current
	locale.

\Z	Matches only at the end of the string.


\\	Matches a literal backslash.
'''

FlagsHelpText = \
r'''Flags:

IGNORECASE
	Perform case-insensitive matching; expressions like [A-Z] will
	match lowercase letters, too. This is not affected by the
	current locale.

LOCALE
	Make \w, \W, \b, \B, dependent on the current locale. 

MULTILINE
	When specified, the pattern character "^" matches at the
	beginning of the string and at the beginning of each line
	(immediately following each newline); and the pattern
	character "$" matches at the end of the string and at the end
	of each line (immediately preceding each newline). By default,
	"^" matches only at the beginning of the string, and "$" only
	at the end of the string and immediately before the newline
	(if any) at the end of the string.

DOTALL
	Make the "." special character match any character at all,
	including a newline; without this flag, "." will match
	anything except a newline.

VERBOSE 
	This flag allows you to write regular expressions that look
	nicer. Whitespace within the pattern is ignored, except when
	in a character class or preceded by an unescaped backslash,
	and, when a line contains a "#" neither in a character class
	or preceded by an unescaped backslash, all characters from the
	leftmost such "#" through the end of the line are ignored.

Find All
	Find list of all non-overlapping matches of pattern in string.
	This isn't really a flag; it corresponds roughly to the 
	re.findall(pattern, string) function.
'''

if __name__ == '__main__':
    r = Recon()
    r.master.title('Recon - Regular Expression Test Console')
    r.pack(expand=YES, fill=BOTH)
    mainloop()

