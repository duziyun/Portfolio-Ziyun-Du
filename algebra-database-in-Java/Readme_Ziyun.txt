{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf400
{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 AppleSymbols;\f2\fnil\fcharset0 ArialUnicodeMS;
\f3\froman\fcharset0 TimesNewRomanPSMT;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 I:for project/\uc0\u960 , type a list of attributes with or without relation name\
   \uc0\u960 (pname,part.color,proj.jnum) (part
\f1 \uc0\u10799 
\f0  proj)\
\
II: for select/\uc0\u963 , use "and" between different conditions\
  \uc0\u963 (sname="Smith" and status>10) (supplier)\
 \uc0\u963 (part.city=proj.city and color="Red" and weight<17) (part
\f1 \uc0\u10799 
\f0  proj)\
\
III: for 
\f1 \uc0\u8904 
\f0 , use  "and" between different conditions, in  below example, even both supplier and proj have attribute "city", you don't have to wirte "supplier.city=proj.city", but remember to rename attributes when you use "Set H=" or it will cause ambigous attributes error.\
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0
\cf0 supplier
\f1 \uc0\u8904 
\f0 (supplier.city=proj.city and status=30 and supplier.sname="Blake") proj\
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0
\cf0 it also works: supplier
\f1 \uc0\u8904 
\f0 (city=city and status=30 and supplier.sname="Blake") proj\
\
IV:for group-by function(count,sum,min,max,avg), it supports both"count(*)" and "count(attributename)", please add "()" outside all functions.\
\uc0\u947 (snum,pnum)
\f2 \uc0\u8497 
\f0 (count(*),sum(qty),min(qty))(spj)\
\
V: for mutiple lines of query\
Please use "Set H=" for each line of query, but for the last line, you don't have to use "Set H=". The project will always return the result of last line.\
for example:\
\pard\pardeftab720\ri0\partightenfactor0
\cf0 Set empWithMaleDep = \uc0\u960 (essn) ( \u963 (sex='M') (dependent)  )\
Set empWithOnlyFemDep(ssn) = \uc0\u960 (ssn)(employee) \u8722   empWithMaleDep
\f3 \

\f0 \uc0\u960 (fname,lname) ( employee 
\f1 \uc0\u8904 
\f0 (ssn=ssn) empWithOnlyFemDep )\
\
}