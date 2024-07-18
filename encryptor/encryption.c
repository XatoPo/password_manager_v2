/* encryption.c: Archivo de código en C que realiza la encriptación de textos usando la librería OpenSSL */

#include <openssl/evp.h>  /* Incluye las funciones de OpenSSL para encriptación/desencriptación */
#include <openssl/rand.h>  /* Incluye funciones para generación de números aleatorios */
#include <string.h>  /* Incluye funciones para manipulación de cadenas de caracteres */
#include <stdio.h>  /* Incluye funciones para entrada y salida estándar */

#define KEY_SIZE 32  /* Define el tamaño de la clave de encriptación (256 bits) */
#define IV_SIZE 16  /* Define el tamaño del vector de inicialización (128 bits) */

/* Función para encriptar un texto plano */
void encrypt(const unsigned char *key, const unsigned char *iv, const unsigned char *plaintext, unsigned char *ciphertext) {
    EVP_CIPHER_CTX *ctx;  /* Puntero al contexto de cifrado */
    int len;  /* Variable para almacenar el tamaño parcial del texto encriptado */
    int ciphertext_len;  /* Variable para almacenar el tamaño total del texto encriptado */

    /* Crea un nuevo contexto de cifrado */
    if (!(ctx = EVP_CIPHER_CTX_new())) {
        fprintf(stderr, "Failed to create EVP_CIPHER_CTX\n");
        return;
    }

    /* Inicializa el contexto para encriptar usando AES-256-CBC */
    if (1 != EVP_EncryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv)) {
        fprintf(stderr, "Failed to initialize encryption\n");
        EVP_CIPHER_CTX_free(ctx);
        return;
    }

    /* Encripta el texto plano */
    if (1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, strlen((char *)plaintext))) {
        fprintf(stderr, "Failed to encrypt\n");
        EVP_CIPHER_CTX_free(ctx);
        return;
    }
    ciphertext_len = len;  /* Almacena el tamaño parcial del texto encriptado */

    /* Finaliza la encriptación */
    if (1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len)) {
        fprintf(stderr, "Failed to finalize encryption\n");
        EVP_CIPHER_CTX_free(ctx);
        return;
    }
    ciphertext_len += len;  /* Suma el tamaño final al tamaño total del texto encriptado */

    /* Libera el contexto de cifrado */
    EVP_CIPHER_CTX_free(ctx);
}
