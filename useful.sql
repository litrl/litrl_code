--get the average scores for clickbait

select url, avg(cbscore)* 100 as avgClickbaitScore, avg(ncbscore) * 100 as avgNotClickbaitScore, count(*) as LinkCount from clickbait group by URL;