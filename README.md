# Second Price  Sealed-Bid Auction

## Solution

This type of auction system can be solved in two different ways: state based transition and global
solution style. In the state based transition we can condisier that in each round there is a potential
winner W and a potential winning price WP and we can make a transit from state to state comparing our 
result with previous state result as in a dynamic programming approach. In the opposite corner, the global
solution is based on all the info and computer the result by simply take the maximum bidder and second maximum
bid. More explanations on algorithms bellow.

## Algorithms
---
For each of the following discussions, let's consider the example:

Consider 5 potential buyers (A, B, C, D, E) who compete to acquire an object with a reserve price set at 100 euros, 
bidding as follows:
 
A: 2 bids of 110 and 130 euros
B: 0 bid -> here a default bid value will take B bids place when computing max value 
C: 1 bid of 125 euros
D: 3 bids of 105, 115 and 90 euros
E: 3 bids of 132, 135 and 140 euros
 
The buyer E wins the auction at the price of 130 euros.

Global based solution is a static algorithm in witch we take the max from each potential buyers and then 
computer the winning score as the second largest score in the list, if this one si higher than the reserved price,
otherwise the highest price. In the case of witch no buyer has a good price the 'game' has no solution.

- Take the max from each potential buyer: memory = [ (A, 130), (B, -1000), (C, 125), (D, 115), (E, 140) ]

- Sort in decending order: memory = sorted(memory) = [ (E, 140), (A, 130), (C, 125), (D, 115), (B, -1000) ]

- Winner: highest price -> E
- Winning price: second highest if this is higher than reserved price, otherwise winner's price: 130 from A

---

State based transition is a dynamic programming algorithm. The overall 'game' can be represented as a matrix in
which the columns represents the rounds:
| Buyer | Initial state - State 0 |  State 1 | State 2 |
|---|---|---|---|
| A | 110  | 130  | * | 
| B |  * |  * | *  |
| C | 125 | * | *  |
| D | 105 | 115 | 90 |
| E | 132 | 135 | 140|

In each round we decinde the winner: the buyer with the highest price and the winnig price from the logic above.
At each round, we compare the current potential winner with the potential winner from the early round and make
a decision based on their performance to keep the winning bid always first.

0) E wins with C bid: 125
1) E wins with A bid: 130 -> compare with previous state solution 
	=> E ~ E (same winner) -> take the bigger bid from those different that E
	=> (A, C) != E so we take max from them: (A, 130)
2) E wins with E bid: 140 but we heve the previous round solution 
	=> we take max from (A, -) as E can't take its own bid if there are another available

Solution: E: 130

## Testing
### Testcases
Basically the testcase focus on different scenarios from simple example like scenarios to no buyers
and even speedy like games where all potential buyers bid only one round with high amounts. 
I personally prefer the global based solution as it is more clean in implementation, but
in a real world scenario with a high density data stream of buyers the state based solution fits better.

For more details about the testcases take a look on _assets_ folder



# Documentation

[Nash equilibrium applied in this problem](https://homepages.cwi.nl/~apt/stra/ch7.pdf)

[Ebay strategy](https://web.stanford.edu/~alroth/papers/eBay.ai.pdf)

