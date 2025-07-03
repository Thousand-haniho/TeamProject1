--------------------------------------------------------------------------
/* 3차 팀 프로젝트 (농업교육기관) */

create table plant_edu_spot(	
	idx number primary key,
	faclt varchar2(100) not null, 
	addr varchar2(200) not null, 
	latitude number(20,10) not null, 
	longitude number(20,10) not null
);

desc plant_edu_spot;
select * from plant_edu_spot where faclt='상호명';
select count(*) from plant_edu_spot;
select * from plant_edu_spot;

delete from plant_edu_spot;
drop table plant_edu_spot;

--------------------------------------------------------------------------
/* 3차 팀 프로젝트 (전국 꽃집) */

create table flowershop_spot(	
	idx number primary key, 
	sigun varchar2(100) not null, 
	faclt varchar2(100) not null, 
	addr varchar2(200) not null, 
	latitude number(20,10) not null, 
	longitude number(20,10) not null
);

desc flowershop_spot;
select * from flowershop_spot where faclt='상호명';
select count(*) from flowershop_spot where sigun='인천광역시';
select count(*) from flowershop_spot;

select * from flowershop_spot;

delete from flowershop_spot;
drop table flowershop_spot;
