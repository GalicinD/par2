-- use computers;
-- SELECT t1.maker, t1.model, t1.type
-- FROM (select p.maker, p.model, p.type, (@I:=@I+1) as num
-- 	from Product p, (select @I:=0)I
--     order by p.model) t1
-- where t1.num>3 and t1.num < (@I-2);


select distinct p2.maker, count(p2.maker) as num 
FROM Product p2
group by p2.maker
having num = (select min(t3.num) 
	from (SELECT distinct p.maker, count(p.maker) as num 
		FROM Product p
		group by p.maker)t3)
or num=(select max(t4.num) 
	from (SELECT distinct p.maker, count(p.maker) as num
		FROM Product p
		group by p.maker)t4)
order by num desc, maker
;