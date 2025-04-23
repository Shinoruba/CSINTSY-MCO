% facts
father(carlitos, jack).
father(carlitos, carla).
father(carlitos, jio).
father(jio, alonso).
father(chito, marco).
father(nick, nicole).
mother(corie, jack).
mother(aprile, marco).
mother(melle, nicole).
mother(corie, jio).
sibling(carlitos, chito).
sibling(carlitos, melle).
sibling(X,Y) :- sibling(Y,X), X \= Y.

male(carlitos).
male(jack).
male(chito).
male(marco).
male(nick).
male(marco).
male(jio).
male(alonso).
female(carla).
female(nicole).
female(corie).
female(aprile).
female(melle).

parent(X, Y) :- 
    father(X, Y), mother(_Z, Y); father(_Z, Y), mother(X, Y).
cousin(X,Y) :- cousin(Y,X).
cousin(X, Y) :- 
    father(Z, X), father(W, Y), sibling(Z, W). 
cousin(X, Y) :- 
    mother(Z, X), mother(W, Y), sibling(Z, W).

get_grandchild(Z) :-
    parent(Z, X),
    parent(X, Y),
    write('Grandchild: '),
    write(Y), nl. 

get_mother(Y) :-
    mother(X, Y),
    write('Mother: '),
    write(X), nl.

get_father(Y) :-
    father(X, Y),
    write('Father: '),
    write(X), nl.

get_sibling(X) :-
    sibling(X, Y),
    write('Sibling of : '),
    write(Y), nl.
    
% :- is if
% , is and
% ; is or
% nl is next line