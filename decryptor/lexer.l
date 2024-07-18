/* lexer.l: Archivo Flex (lexer) que analiza el texto cifrado y lo pasa al parser */

%{
#include "parser.tab.h"  /* Incluye el archivo de cabecera generado por Bison */
#include <openssl/aes.h>  /* Incluye las funciones de AES de OpenSSL */
#include <string.h>  /* Incluye funciones para manipulación de cadenas de caracteres */
#include <stdio.h>  /* Incluye funciones para entrada y salida estándar */

#define KEY_SIZE 32  /* Define el tamaño de la clave de encriptación (256 bits) */
#define IV_SIZE 16  /* Define el tamaño del vector de inicialización (128 bits) */

/* Declara la función de desencriptación */
void decrypt(const unsigned char *key, const unsigned char *iv, const unsigned char *ciphertext, unsigned char *plaintext);
%}

%%
.+ { yylval.str = strdup(yytext); return CIPHERTEXT; }  /* Almacena el texto cifrado y lo retorna como token CIPHERTEXT */
\n { /* ignore newlines */ }  /* Ignora los saltos de línea */
. { /* ignore other characters */ }  /* Ignora otros caracteres */
%%

/* Función requerida por Flex para indicar el final del archivo */
int yywrap(void) {
    return 1;
}