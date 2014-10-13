// Tokens!
%fragment I: '(?i)';    // Case Insensitive

start: (section|NEWLINE)+;
section: SECTION NEWLINE (NEWLINE|host)*;
host: HOST NEWLINE;
NEWLINE: '\n+' (%newline) ;
LBRACK: '\[';
RBRACK: '\]';
COLON: ':';
COMMA: ',';
EXCLUDE: '!';
NUMBER: '\d+';

WS: '[\t \f]+' (%ignore);
COMMENT: '[\#;][^\n]*'(%ignore);


SECTION: '\[[^\[\]\n;]+\]'
{
    start: '\[' name ']'
         | '\[' name ':' group ']';
    group: name;
    name: '[^\[\]\n;]+';
};
HOST: I '[a-zA-Z0-9][a-zA-Z0-9\[\]\-:,\.!]+'
{
    start: fragment*;
    fragment: name
            | range;
    name: '[a-zA-Z0-9\.\-]';
    range: '\[' items '\]'
         | '\[' items '!' items '\]';
    @items: item ','?
          | item ',' items;
    item: '\d+'
        | '\d+' ':' '\d+';
};


/*
start: NL* section* NL*;
section: NL* LBRACK title RBRACK NL hosts?;
title: NAME COLON NAME
     | NAME;

@hosts: host*;
host: host_item* NL;
@host_item: NAME
          | range;

range: LBRACK items RBRACK
     | LBRACK items EXCLUDE items RBRACK;
@items: item COMMA?
      | item COMMA items;
item: NUMBER
    | NUMBER COLON NUMBER;

LBRACK: '\[';
RBRACK: '\]';
COLON: ':';
COMMA: ',';
EXCLUDE: '!';
NUMBER: '\d+';
NL: '(\r?\n[\t ]*)+'    // Don't count on the + to prevent multiple NLs. They can happen.
    (%newline);
LINE_CONT: '\[\t \f]*\r?\n' (%ignore) (%newline);
NAME: '[a-zA-Z_][a-zA-Z_0-9.]*(?!r?"|r?\')';
WS: '[ \t\f]+' (%ignore);
%newline_char: '\n';
*/
