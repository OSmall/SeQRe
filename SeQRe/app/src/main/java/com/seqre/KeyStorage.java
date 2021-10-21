package com.seqre;

import java.security.KeyStore;
import java.util.Enumeration;


public class KeyStorage {

    KeyStore keyStore;

    public KeyStorage() {

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
}