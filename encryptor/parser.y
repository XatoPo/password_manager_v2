/* parser.y: Archivo Bison (parser) que parsea el texto plano y lo encripta */

%{
#include <stdio.h>  /* Incluye funciones para entrada y salida estándar */
#include <stdlib.h>  /* Incluye funciones de utilidad estándar */
#include <string.h>  /* Incluye funciones para manipulación de cadenas de caracteres */
#include <openssl/aes.h>  /* Incluye las funciones de AES de OpenSSL */
#include "parser.tab.h"  /* Incluye el archivo de cabecera generado por Bison */

#define KEY_SIZE 32  /* Define el tamaño de la clave de encriptación (256 bits) */
#define IV_SIZE 16  /* Define el tamaño del vector de inicialización (128 bits) */

/* Declara la función de encriptación */
void encrypt(const unsigned char *key, const unsigned char *iv, const unsigned char *plaintext, unsigned char *ciphertext);

/* Declara la función lexer y la función de manejo de errores */
int yylex(void);
void yyerror(const char *s);
%}

/* Declara la unión para los valores del token */
%union {
    char *str;
}

/* Declara el token PASSWORD con tipo de valor char * */
%token <str> PASSWORD

/* Declara el tipo de valor de la regla 'line' como char * */
%type <str> line

%%
input:
    | input line  /* Permite múltiples líneas de entrada */
    ;

line:
    PASSWORD {
                /* Define la clave y el vector de inicialización */
                unsigned char key[KEY_SIZE] = "mysecretkey1234567890123456";  /* 32 bytes */
                unsigned char iv[IV_SIZE] = "myiv1234567890";                 /* 16 bytes */
                unsigned char ciphertext[1024] = {0};  /* Buffer para el texto encriptado */
                
                /* Encripta el texto plano */
                encrypt(key, iv, (unsigned char*)$1, ciphertext);

                /* Imprime el texto encriptado en formato hexadecimal */
                for (int i = 0; i < strlen((char *)ciphertext); i++) {
                    printf("%02x", ciphertext[i]);
                }
                printf("\n");
                free($1);  /* Libera la memoria asignada para el texto plano */
             }
    ;
%%

/* Función principal */
int main(int argc, char **argv) {
    return yyparse();
}

/* Función de manejo de errores */
void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}