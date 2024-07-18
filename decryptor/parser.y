/* parser.y: Archivo Bison (parser) que parsea el texto cifrado y lo desencripta */

%{
#include <stdio.h>  /* Incluye funciones para entrada y salida estándar */
#include <stdlib.h>  /* Incluye funciones de utilidad estándar */
#include <string.h>  /* Incluye funciones para manipulación de cadenas de caracteres */
#include <openssl/aes.h>  /* Incluye las funciones de AES de OpenSSL */
#include "parser.tab.h"  /* Incluye el archivo de cabecera generado por Bison */

#define KEY_SIZE 32  /* Define el tamaño de la clave de encriptación (256 bits) */
#define IV_SIZE 16  /* Define el tamaño del vector de inicialización (128 bits) */

/* Declara la función de desencriptación */
void decrypt(const unsigned char *key, const unsigned char *iv, const unsigned char *ciphertext, unsigned char *plaintext);

/* Declara la función lexer y la función de manejo de errores */
int yylex(void);
void yyerror(const char *s);
%}

/* Declara la unión para los valores del token */
%union {
    char *str;
}

/* Declara el token CIPHERTEXT con tipo de valor char * */
%token <str> CIPHERTEXT

/* Declara el tipo de valor de la regla 'line' como char * */
%type <str> line

%%
input:
    | input line  /* Permite múltiples líneas de entrada */
    ;

line:
    CIPHERTEXT {
                /* Define la clave y el vector de inicialización */
                unsigned char key[KEY_SIZE] = "mysecretkey1234567890123456";  /* 32 bytes */
                unsigned char iv[IV_SIZE] = "myiv1234567890";                 /* 16 bytes */
                unsigned char ciphertext[1024] = {0};  /* Buffer para el texto cifrado */
                unsigned char plaintext[1024] = {0};  /* Buffer para el texto desencriptado */

                /* Convierte el texto cifrado hexadecimal a binario */
                int value;
                int len = strlen($1) / 2;
                for (int i = 0; i < len; i++) {
                    sscanf($1 + 2*i, "%02x", &value);
                    ciphertext[i] = (unsigned char)value;
                }

                /* Desencripta el texto cifrado */
                decrypt(key, iv, ciphertext, plaintext);

                /* Asegura la terminación nula del texto desencriptado */
                plaintext[1023] = '\0';

                /* Imprime la contraseña desencriptada */
                printf("%s\n", plaintext);
                free($1);  /* Libera la memoria asignada para el texto cifrado */
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