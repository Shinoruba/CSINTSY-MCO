% facts 1st gen
father(papa, ronnie).
father(papa, chito).
father(papa, litos).
father(papa, pete).
father(papa, menchu).
father(papa, maurine).
father(papa, melle).
% 2nd gen
father(ronnie, jego).
father(ronnie, gelo).
% 2nd gen
father(chito, marco).
father(chito, mikel).
father(chito, mico).
father(chito, lui).
father(chito, la).
% 2nd gen
father(litos, jio).
father(litos, carla).
father(litos, jack).
% 3rd gen
father(la, luca).
father(la, tali).
% 3rd gen
father(jio, alonso).
father(jio, tomas).
% 2nd gen
father(nick, nicole).
father(nick, anjoe).
mother(melle, anjoe).
mother(melle, nicole).
% 1st gen
mother(mama, ronnie).
mother(mama, chito).
mother(mama, litos).
mother(mama, pete).
mother(mama, menchu).
mother(mama, maurine).
mother(mama, melle).
% 2nd gen
mother(aprile, marco).
mother(aprile, mikel).
mother(aprile, mico).
mother(aprile, lui).
mother(aprile, la).
% 2nd gen
mother(corie, jio).
mother(corie, carla).
mother(corie, jack).
% 3rd gen
mother(erin, alonso).
mother(erin, tomas).
% 2nd gen
mother(lalang, gelo).
mother(lalang, jego).
% 3rd gen
mother(kristine, luca).
mother(kristine, tali).
% 
male(papa).
male(ronnie).
male(chito).
male(litos).
male(pete).
male(jego).
male(gelo).
male(marco).
male(mikel).
male(nick).
male(anjoe).
male(mico).
male(lui).
male(la).
male(litos).
male(jio).
male(jack).
male(alonso).
male(tomas).
male(luca).
female(menchu).
female(maurine).
female(melle).
female(nicole).
female(carla).
female(mama).
female(aprile).
female(corie).
female(erin).
female(lalang).
female(tali).
female(kristine).

% sibling(X, Y) :- sibling(Y, X). THIS CAUSES A LOOP

% define relative by emman edited by jack (does not include in-laws or great grand parents)
relative(X, Y) :-
    X \= Y,
    sibling(X, Y);          % They are siblings
    cousin(X, Y);           % They are cousins
    (is_aunt_of(X, Y); is_uncle_of(X, Y));    % One is an aunt or uncle
    parent(X, Y);           % One is a parent
    parent(Y, X);
    grandparent(X, Y);      % One is a grandparent
    grandparent(Y, X);
    married(X, Y).          % They are married

% define married
married(X, Y) :-
    parent(X, Z),
    parent(Y, Z).

% define sibling
sibling(X, Y) :-
    X \= Y,
    (father(Z, X), father(Z, Y)); % Z is the father of X, Z is the father of Y
    (mother(A, X), mother(A, Y)). % A is the mother of X, A is the mother of Y

% define parent
parent(X, Y) :- 
    % X is the parent of Y if they are the father or the mother of Y
    father(X, Y); mother(X, Y).

% define cousin
cousin(X, Y) :-
    parent(A, X), % A is the parent of X
    parent(B, Y), % B is the parent of Y
    sibling(A, B). % A and B are siblings

/* 
% define grandparent
grandparent(X, Y) :- % X is the grandparent of Y if
    parent(X, Y), % X is the parent of Y
    parent(Y, _Z). % Y is the parent of Z : Z is the grandchild

% Include the case where a sibling of a grandparent is also a grandparent
grandparent(X, Y) :- 
    sibling(X, S),  % X is a sibling of S
    parent(S, Z),   % S is the parent of Z
    parent(Z, Y).   % Z is the parent of Y : X is also considered a grandparent
*/

% define grandparent new by jack - considers couples but only immediate family
grandparent(Grandparent, Grandkid) :-
    (parent(Grandparent, Parent); 
    sibling(Grandparent, Parent)),
    parent(Parent, Grandkid).

% who are the siblings of _? fixed by jack
is_sibling_of(Input) :-
    sibling(Input, Y),
    Input \= Y,
    format('~w ~s sibling of ~w~n', [Input, "is the", Y]),
    nl.

% who are the sisters of _? fixed by jack
is_sister_of(Input) :-
    sibling(Input, Y), % X and Y are siblings
    female(Y), % Input is also female
    format('~w ~s sister of ~w~n', [Input, "is the", Y]),
    nl.

% is _ the sister of _? liana
is_sister_of(Sister, Person) :-
    sibling(Sister, Person), % Sister and Person are siblings
    female(Sister), % Sister is also female
    !,
    format('~w is the sister of ~w~n', [Sister, Person]),
    nl.

% who is the mother of _? fixed by jack
is_mother_of(Input) :- 
    mother(Y, Input),
    !,
    format('~w ~s mother of ~w~n', [Y, "is the", Input]),
    nl.

% is _ the mother of _ ? by jack
is_mother_of(Mother, Child) :- 
    mother(Mother, Child),
    female(Mother),
    format('~w is the mother of ~w~n', [Mother, Child]),
    nl.

/*
% _ is the grandmother of X
is_grandmother_of(Input) :- 
    parent(Input, Y),
    parent(Y, Z),
    format('~w ~s grandmother of ~w~n', [Input, "is the", Z]),
    nl.
*/

% is _ a grandmother of _? by jack (does not count siblings of the grandparent as grandparents)
is_grandmother_of(Grandmother, Grandkid) :-
    parent(Parent, Grandkid), % Grandkid is the child of Parent
    parent(Grandmother, Parent), % Parent is the child of Grandmother
    female(Grandmother),
    format('~w is the grandmother of ~w~n', [Grandmother, Grandkid]),
    nl.

% _ is the child of X
is_child_of(Input) :- 
    (father(Input, Y); mother(Input, Y)),
    format('~w ~s child of ~w~n', [Y, "is the", Input]).

% is _ the child of _? liana
is_child_of(Child, Parent) :- 
    (parent(Parent, Child)),
    !,
    format('~w is a child of ~w~n', [Child, Parent]).

% _ is a daughter of X
is_daughter_of(Input) :- 
    Input \= Y,
    (father(Input, Y); mother(Input, Y)),
    female(Y),
    format('~w ~s daughter of ~w~n', [Y, "is the", Input]),
    nl.

% is _ the daughter of _ ? by jack
is_daughter_of(Daughter, Parent) :- % daughter is the daughter of parent IF
    parent(Parent, Daughter), 
    female(Daughter),
    format('~w ~s daughter of ~w~n', [Daughter, "is the", Parent]),
    nl.

/* 
% _ is an uncle of X
is_uncle_of(Input) :- 
    sibling(Input, Parent),    % Input is a sibling of the parent
    parent(Parent, Child),     % Parent is a parent of Child
    male(Input),               % Input is male
    format('~w ~s uncle of ~w~n', [Input, "is the", Child]),
    nl.
*/ 

% is _ the uncle of _ ? by jack
is_uncle_of(Uncle, NieceNephew) :- 
    (sibling(Uncle, Parent); cousin(Uncle, Parent)), % uncle is the sibling or cousin of parent
    parent(Parent, NieceNephew), % parent is the parent of niece/nephew
    male(Uncle),
    format('~w ~s uncle of ~w~n', [Uncle, "is the", NieceNephew]),
    nl.

% who are the brothers of _ ? fixed liana
is_brother_of(Input) :-
    sibling(Input, Y),         % Input is a sibling of Y
    male(Y),               % Input is male
    format('~w ~s brother of ~w~n', [Input, "is the", Y]),
    nl.

% is _ a brother of _? liana
is_brother_of(Brother, Person) :-
    sibling(Brother, Person),    % Brother is a sibling of Person
    male(Brother),               % Brother is male
    !,
    format('~w is the brother of ~w~n', [Brother, Person]),
    nl.

% who is the father of _? fixed by jack
is_father_of(Input) :- 
    father(Y, Input),
    format('~w ~s father of ~w~n', [Y, "is the", Input]),
    nl. 

% is _ the father of _ ? by jack
is_father_of(Father, Child) :- 
    father(Father, Child),
    male(Father),
    format('~w is the father of ~w~n', [Father, Child]),
    nl.

% _ and _ are the parents of X
are_parents_of(Input) :- 
    parent(Father, Input), 
    father(Father, Input),
    parent(Mother, Input),
    mother(Mother, Input),
    format('~w ~s and ~w ~s parents of ~w~n', [Father, "and", Mother, "are the", Input]),
    nl.

/*
% _ is the grandfather of X
is_grandfather_of(Input) :- 
    parent(Input, Y),          % Input is a parent of Y
    parent(Y, Z),              % Y is a parent of Z
    male(Input),               % Input is male
    format('~w ~s grandfather of ~w~n', [Input, "is the", Z]),
    nl.
*/

% is _ a grandfather of _? by jack (does not count siblings of the grandparent as grandparents)
is_grandfather_of(Grandfather, Grandkid) :-
    parent(Parent, Grandkid), % Grandkid is the child of Parent
    parent(Grandfather, Parent), % Parent is the child of Grandfather
    male(Grandfather),
    format('~w is the grandfather of ~w~n', [Grandfather, Grandkid]),
    nl.

% _, _, and _ are the children of X
are_children_of(Input) :- 
    findall(Child, parent(Input, Child), Children), % Find all children of Input
    format('~w ~s children of ~w: ~w~n', [Children, "are the", Input, Children]),
    nl.

% is _ a son of 
is_son_of(Input) :- 
    (father(Input, Y); mother(Input, Y)),
    male(Y),
    format('~w ~s son of ~w~n', [Y, "is the", Input]),
    nl.

% _ is a son of _
is_son_of(Son, Parent) :- 
    (father(Parent, Son); mother(Parent, Son)),
    male(Son),
    !,
    format('~w is the son of ~w~n', [Son, Parent]),
    nl.



/* % _ is an aunt of X
is_aunt_of(Input) :- 
    sibling(Input, Parent),    % Input is a sibling of the parent
    parent(Parent, Child),     % Parent is a parent of Child
    female(Input),             % Input is female
    format('~w ~s aunt of ~w~n', [Input, "is the", Child]),
    nl.
*/

% is _ the aunt of _ ? by jack
% i cannot for the life of me make this accept people theyre married to
is_aunt_of(Aunt, NieceNephew) :- 
    (sibling(Aunt, Parent); cousin(Aunt, Parent)), % Aunt is the sibling or cousin of parent
    parent(Parent, NieceNephew), % parent is the parent of niece/nephew
    female(Aunt),
    format('~w ~s aunt of ~w~n', [Aunt, "is the", NieceNephew]),
    nl.

% get all the grandchildren of Y
is_grandparent_of(Input) :-
    % Input \= Y,
    parent(Input, X),
    parent(X, Y),
    format('~w ~s grandparent of ~w~n', [Input, "is the", Y]),
    nl.

:- dynamic father/2.
:- dynamic mother/2.
:- dynamic sibling/2.
:- dynamic brother/2.
:- dynamic sister/2.
:- dynamic child/2.
:- dynamic parent/2.
:- dynamic grandmother/2.
:- dynamic grandfather/2.
:- dynamic children/2.
:- dynamic daughter/2.
:- dynamic son/2.
:- dynamic uncle/2.
:- dynamic aunt/2.
:- dynamic male/1.
:- dynamic female/1.
% :- is if
% , is and
% ; is or
% nl is next line

% are _ and _ the parents of ? by jack
are_parents_of(Parent1, Parent2, Child) :- 
    Parent1 \= Parent2,
    parent(Parent1, Child), 
    parent(Parent2, Child),
    format('~w ~s ~w ~s parents of ~w~n', [Parent1, "and", Parent2, "are the", Child]),
    nl.

% are _, _, and _ the children of _? by jack - FOR 2 CHILDREN
are_children_of(Child1, Child2, Parent) :- 
    parent(Parent, Child1), 
    parent(Parent, Child2),
    format('~w ~s ~w ~s children of ~w~n', [Child1, "and", Child2, "are the", Parent]),
    nl.

% are _, _, and _ the children of _? by jack - FOR 3 CHILDREN
are_children_of(Child1, Child2, Child3, Parent) :-
    parent(Parent, Child1),
    parent(Parent, Child2),
    parent(Parent, Child3),
    format('~w ~s ~w ~s ~w ~s children of ~w~n', [Child1, "and", Child2, "and", Child3, "are the", Parent]),
    nl.

% who are the daughters of _?

% who are the sons of _?

% who are the children of _?