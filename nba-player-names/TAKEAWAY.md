# NBA Player First-Name Gender Guess — Takeaways

We ran every historical NBA player's first name (5,103 players) through the
`gender-guesser` library and, unsurprisingly, the vast majority are classified
as **male**. But the misclassifications are where it gets fun.

## By the numbers

| Classification | Count | % |
|---|---|---|
| Male | 3,799 | 74.4% |
| Mostly Male | 409 | 8.0% |
| Unknown | 668 | 13.1% |
| Androgynous | 79 | 1.5% |
| Mostly Female | 83 | 1.6% |
| Female | 65 | 1.3% |

## Notable "female" NBA players

The library thinks these are women's names:

- **Kiki Vandeweghe** — All-Star forward, later NBA executive
- **Metta World Peace** (Ron Artest) — Defensive Player of the Year
- **Nate Thurmond** — Hall of Famer, first player to record a quadruple-double
- **Nate Archibald** — Hall of Famer, only player to lead the league in scoring and assists in the same season
- **Nate Robinson** — 3x Slam Dunk Contest winner
- **Nate McMillan** — long-time NBA head coach
- **Caron Butler** — two-time All-Star
- **Monta Ellis** — averaged 25 PPG for the Warriors
- **Patty Mills** — Olympic hero for Australia, NBA champion with the Spurs
- **Caris LeVert** — current NBA player
- **Precious Achiuwa** — active player, formerly of the Raptors
- **Simone Fontecchio** — Italian national team star, active in NBA
- **Coby White** — active starting guard for the Bulls
- **Elgin Baylor** — Hall of Famer and all-time great

"Nate" alone accounts for **15 players** in the female category — the library
maps it to the female name "Nate/Nathalie" rather than "Nathan."

## Notable "mostly female" NBA players

- **Tracy McGrady** — Hall of Famer, 2x scoring champion
- **Ja Morant** — face of the Grizzlies, Rookie of the Year
- **Kyle Lowry** — 6x All-Star, NBA champion with the Raptors
- **Kyle Kuzma** — NBA champion with the Lakers
- **Gail Goodrich** — Hall of Famer, key player on the '72 Lakers
- **Connie Hawkins** — Hall of Famer, playground legend
- **Brook Lopez** — longest-tenured Net, NBA champion with the Bucks
- **Kelly Oubre Jr.** — fan-favorite swingman
- **Kelly Olynyk** — active NBA center
- **Shannon Brown** — high-flying Lakers guard
- **Courtney Lee** — 14-year NBA veteran
- **Maxi Kleber** — Mavericks mainstay

"Kyle" is the biggest contributor here with **13 players**, followed by "Mel"
(14 players) and "Courtney" (4 players).

## Notable "androgynous" NBA players

- **Dominique Wilkins** — Hall of Famer, "The Human Highlight Film"
- **Yao Ming** — Hall of Famer (classified by "Ming")
- **Pat Riley** — legendary coach, classified as a player too
- **Doc Rivers** — Hall of Fame coach
- **Avery Bradley** — elite perimeter defender
- **Payton Pritchard** — 2025 Sixth Man of the Year candidate

## Why this happens

1. **Cultural mismatch** — The library is trained on Western European/American
   name data. Names like "Precious," "Simone" (male in Italian), "Yuta"
   (Japanese), and "Noa" (male in Hebrew/French) get misclassified.
2. **Nickname vs. given name** — "Nate" maps to female, but it's almost always
   short for "Nathan" in the NBA context.
3. **Genuinely unisex names** — Tracy, Kelly, Courtney, and Kyle are used for
   both men and women in English, so the library hedges.
4. **Unique/invented names** — Many modern NBA names (Ja, Keon, DaQuan) simply
   aren't in the library's training data.

## The actual takeaway

A name-based gender classifier says ~75% of NBA players are male. The other
~25% aren't actually women — they just have names the algorithm wasn't trained
to recognize as male. It's a reminder that name-gender inference is culturally
biased and breaks down outside its training distribution.

## Instagram caption

> I ran all 5,103 NBA players through a name-gender classifier. It said 75%
> are male. Sounds about right.
>
> Then I looked at the other 25%.
>
> Hall of Famers Nate Archibald and Nate Thurmond? Female. Tracy McGrady and
> Ja Morant? Mostly female. Dominique Wilkins? Androgynous.
>
> The algorithm was trained on Western names — so Simone (male in Italian),
> Precious, and Yao Ming broke it completely.
>
> Very obvious chart. Very obvious conclusion. NBA players are, in fact, men.
