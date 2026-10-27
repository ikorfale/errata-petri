# Prediction before running: why children of dividing 0 mod 3 deletion variants are sterile
Written 2026-10-27 ~21:00Z before delete_kids.py was run.
Guess (posts/petri-delete-e3-1028.md): the copy is cut in the wrong place, so the child gets a wrong length again.
For the 25 dividing single-deletion variants, mutation OFF, first division:
- in >= 20 of 25 the clean child is NOT an exact copy of its parent (length != 111 or letters differ);
- in >= 20 of 25 the clean child (mutation off) never divides within 3000 steps.
Falsified if most clean children are exact copies: then the sterility comes from mutation (or world state), not from the cut.
