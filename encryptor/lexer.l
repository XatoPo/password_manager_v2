/* lexer.l: Archivo Flex (lexer) que analiza el texto plano y lo pasa al parser */

%{
#include "parser.tab.h"  /* Incluye el archivo de cabecera generado por Bison */
#include <openssl/aes.h>  /* Incluye las funciones de AES de OpenSSL */
#include <openssl/rand.h>  /* Incluye funciones para generación de números aleatorios */
#include <string.h>  /* Incluye funciones para manipulación de cadenas de caracteres */
#include <stdio.h>  /* Incluye funciones para entrada y salida estándar */

#define KEY_SIZE 32  /* Define el tamaño de la clave de encriptación (256 bits) */
#define IV_SIZE 16  /* Define el tamaño del vector de inicialización (128 bits) */

/* Declara la función de encriptación */
void encrypt(const unsigned char *key, const unsigned char *iv, const unsigned char *plaintext, unsigned char *ciphertext);
%}

%%
[^\n]+ { yylval.str = strdup(yytext); return PASSWORD; }  /* Almacena el texto plano y lo retorna como token PASSWORD */
\n { /* ignore newlines */ }  /* Ignora los saltos de línea */
. { /* ignore other characters */ }  /* Ignora otros caracteres */
%%

/* Función requerida por Flex para indicar el final del archivo */
int yywrap(void) {
    return 1;
}
