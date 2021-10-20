package com.seqre;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {

    Button btnTakePicture;
    TextView txtResult;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initViews();
    }

    private void initViews() {
        txtResult = findViewById(R.id.txtResultsBody);
        btnTakePicture = findViewById(R.id.camera_capture_button);
        btnTakePicture.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) {
        if (v.getId() == R.id.camera_capture_button) {
            startActivity(new Intent(MainActivity.this, QRCodeActivity.class));
        }
    }
}