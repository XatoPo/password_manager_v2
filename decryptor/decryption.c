/* decryption.c: Archivo de código en C que realiza la desencriptación de textos cifrados usando la librería OpenSSL */

#include <openssl/evp.h>  /* Incluye las funciones de OpenSSL para encriptación/desencriptación */
#include <string.h>  /* Incluye funciones para manipulación de cadenas de caracteres */
#include <stdio.h>  /* Incluye funciones para entrada y salida estándar */

#define KEY_SIZE 32  /* Define el tamaño de la clave de encriptación (256 bits) */
#define IV_SIZE 16  /* Define el tamaño del vector de inicialización (128 bits) */

/* Función para desencriptar un texto cifrado */
void decrypt(const unsigned char *key, const unsigned char *iv, const unsigned char *ciphertext, unsigned char *plaintext) {
    EVP_CIPHER_CTX *ctx;  /* Puntero al contexto de cifrado */
    int len;  /* Variable para almacenar el tamaño parcial del texto desencriptado */
    int plaintext_len;  /* Variable para almacenar el tamaño total del texto desencriptado */

    /* Crea un nuevo contexto de cifrado */
    if (!(ctx = EVP_CIPHER_CTX_new())) {
        fprintf(stderr, "Failed to create EVP_CIPHER_CTX\n");
        return;
    }

    /* Inicializa el contexto para desencriptar usando AES-256-CBC */
    if (1 != EVP_DecryptInit_ex(ctx, EVP_aes_256_cbc(), NULL, key, iv)) {
        fprintf(stderr, "Failed to initialize decryption\n");
        EVP_CIPHER_CTX_free(ctx);
        return;
    }

    /* Desencripta el texto cifrado */
    if (1 != EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, strlen((char *)ciphertext))) {
        fprintf(stderr, "Failed to decrypt\n");
        EVP_CIPHER_CTX_free(ctx);
        return;
    }
    plaintext_len = len;  /* Almacena el tamaño parcial del texto desencriptado */

    /* Finaliza la desencriptación */
    if (1 != EVP_DecryptFinal_ex(ctx, plaintext + len, &len)) {
        fprintf(stderr, "Failed to finalize decryption\n");
        EVP_CIPHER_CTX_free(ctx);
        return;
    }
    plaintext_len += len;  /* Suma el tamaño final al tamaño total del texto desencriptado */

    /* Añade un terminador nulo al final del texto desencriptado */
    plaintext[plaintext_len] = '\0';

    /* Libera el contexto de cifrado */
    EVP_CIPHER_CTX_free(ctx);
}