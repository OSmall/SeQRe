package com.seqre;

import android.os.Bundle;
import android.security.keystore.KeyGenParameterSpec;
import android.security.keystore.KeyProperties;
import android.widget.EditText;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.security.KeyPair;
import java.security.KeyPairGenerator;
import android.widget.ImageView;
import android.widget.EditText;

public class RegisterActivity extends AppCompatActivity {

    TextView register_txt;
    ImageView logo_register;
    EditText email, userID, password;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        //create local variables
        register_txt = findViewById(R.id.registerText);

        //setup logo
        logo_register = findViewById(R.id.logo_register);
        logo_register.setImageResource(R.drawable.big_logo);

        //setup input texts
        email = findViewById(R.id.email);
        userID = findViewById(R.id.userID);
        password = findViewById(R.id.password);
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