% allows these predicates to be modified during runtime
% also lets facts not exist yet (without it may error)
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

% PARENT-CHILD RULES / RELATIONSHIPS


father_of(X, Y) :- father(X, Y).
parent_of(X, Y) :- father(X, Y); mother(X, Y).  

son_of(X, Y) :- father(Y, X), male(X). 
daughter_of(X, Y) :- (father(Y, X); mother(Y, X)), female(X).  


% SIBLING RULES / RELATIONSHIPS

sibling(X, Y) :- 
    (father(Z, X), father(Z, Y));         % X and Y share a father
    (mother(Z, X), mother(Z, Y)).         % X and Y share a mother


brother(X, Y) :- sibling(X, Y), male(X), X \= Y.  % X and Y are brothers
sister(X, Y) :- sibling(X, Y), female(X), X \= Y.  % X and Y are sisters

% GENDER RULES 

male(X) :- father(X, _); son(X, _).  
female(X) :- mother(X, _); daughter(X, _).  

