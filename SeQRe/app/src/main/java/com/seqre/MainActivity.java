package com.seqre;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import androidx.appcompat.app.AppCompatActivity;
import android.widget.ImageView;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    Button btnStart, btnSettings, btnRegister;
    ImageView logo;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //setup logo
        logo = findViewById(R.id.logoView);
        logo.setImageResource(R.drawable.big_logo);

        //register main buttons
        btnStart = findViewById(R.id.start_button);
        btnSettings = findViewById(R.id.settings_button);
        btnRegister = findViewById(R.id.register_button);


        //click listeners for main buttons
        btnStart.setOnClickListener(this);
        btnSettings.setOnClickListener(this);
        btnRegister.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        switch (v.getId()) {
            case R.id.start_button:
                startActivity(new Intent(MainActivity.this, ScanQRCodeActivity.class));
                break;
            case R.id.register_button:
                startActivity(new Intent(MainActivity.this, RegisterActivity.class));
                break;
            case R.id.settings_button:
                startActivity(new Intent(MainActivity.this, SettingsActivity.class));
                break;
        }
    }
}