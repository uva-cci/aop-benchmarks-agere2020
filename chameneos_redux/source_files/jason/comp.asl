complement(blue,   red,    yellow).
complement(blue,   yellow, red).
complement(red,    blue,   yellow).
complement(red,    yellow, blue).
complement(yellow, blue,   red).
complement(yellow, red,    blue).
complement(C, C, C).

/* // alternative implementation
comb(blue,   red,    yellow).
comb(blue,   yellow, red).
comb(red,    yellow, blue).

complement(C1,C2,C) :- comb(C1,C2,C).
complement(C1,C2,C) :- comb(C2,C1,C).
complement(C, C, C).
*/

+!spell(N,L) : N < 10 <- .nth(N,[" zero", " one", " two", " three", " four", " five", " six", " seven", " eight", " nine"],L).
+!spell(N,L) <- !spell(N div 10,L1); !spell(N mod 10,L2); .concat(L1,L2,L).
