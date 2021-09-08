package com.seqre.androidapp;

import android.security.keystore.KeyGenParameterSpec;
import android.security.keystore.KeyProperties;

import java.security.KeyPair;
import java.security.KeyStore;
import java.util.Enumeration;
import java.security.KeyPairGenerator;

public class KeyStorage {

    KeyStore keyStore;


    public KeyStorage() {
        System.out.println(KeyStore.getDefaultType());

        try {
            keyStore = KeyStore.getInstance("AndroidKeyStore");
            keyStore.load(null);

            for (Enumeration<String> e = keyStore.aliases(); e.hasMoreElements();) {
                System.out.println(e.nextElement());
            }

        } catch (Exception e) {
            e.printStackTrace();
        }

    }


    public void register() {
        try {
            KeyPairGenerator kpg;
            kpg = KeyPairGenerator.getInstance(KeyProperties.KEY_ALGORITHM_RSA, "AndroidKeyStore");
            kpg.initialize(new KeyGenParameterSpec.Builder(
                    "seQRe_main",
                    KeyProperties.PURPOSE_SIGN | KeyProperties.PURPOSE_VERIFY)
                    .setDigests(KeyProperties.DIGEST_SHA256,
                            KeyProperties.DIGEST_SHA512)
                    .build());
            KeyPair kp = kpg.generateKeyPair();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
