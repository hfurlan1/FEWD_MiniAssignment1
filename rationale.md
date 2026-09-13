# Rationale

I chose this dataset because I am a huge NBA fan and I'm very interested in sports
analytics. The NBA is a great league to track this kind of thing because it is a
single, closed league (unlike a sport like soccer, which is split across many
competing leagues and countries), so its stats are consistent and easy to compare
season over season. This dataset, the top 50 scorers of the 2026 season, can help
answer a question like: which teams and players are getting the most efficient
scoring production, and is there a relationship between shooting efficiency (FG%)
and total points scored?

One limitation of the data is that it only includes the top 50 scorers, so it is
not representative of the full league. Only 27 of the 30 teams appear at all, and
role players, bench players, and defensive specialists are excluded entirely. Any
conclusions from this app apply only to high-volume scorers, not to the league as
a whole.

The summary metrics (the top scorer's name, points per game, and FG%) are
meaningful because they are recalculated from the filtered subset rather than the
full dataset, so they directly answer "who stands out among the players I'm
currently looking at, and how efficient is he?" rather than being a static,
unchanging number.

I chose a bar chart for the top 20 players by points per game because it
summarizes each player's total points and games played into a single average
statistic and ranks them, making it easy to compare scoring production across
players at a glance. I chose a scatter chart for points per game vs. FG% because
it shows the relationship between two continuous variables at the individual
player level, which is better suited to spotting patterns or outliers (like a
low-volume, high-efficiency scorer) than a bar chart would be.
