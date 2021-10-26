package com.seqre;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.util.SparseArray;
import android.view.SurfaceHolder;
import android.view.SurfaceView;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import com.google.android.gms.vision.CameraSource;
import com.google.android.gms.vision.Detector;
import com.google.android.gms.vision.barcode.Barcode;
import com.google.android.gms.vision.barcode.BarcodeDetector;

import java.io.IOException;
import android.util.Base64;
import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;

import java.io.UnsupportedEncodingException;
import java.math.BigInteger;
import java.security.InvalidKeyException;
import java.security.KeyFactory;
import java.security.spec.*;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.PrivateKey;
import java.util.Arrays;


public class ScanQRCodeActivity extends AppCompatActivity {

    //QR scanning code referenced from https://www.deepcrazyworld.com/create-a-qr-code-scanner-android-app/
    //Original Author: DeepCrazyWorld
    //Refactored to fit purpose of QR authentication


    //local variables
    SurfaceView surfaceView;
    TextView txtBarcodeValue;
    private BarcodeDetector barcodeDetector;
    private CameraSource cameraSource;
    private static final int REQUEST_CAMERA_PERMISSION = 201;
    Button btnAction;
    String QRdata = "";

    //decryption variables
    Cipher cipher;
    PrivateKey privateKey;
    byte[] decryptedBytes;
    String decrypted;

    //constructor
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        //set activity view
        setContentView(R.layout.activity_scan_barcode);

        //create local variables
        txtBarcodeValue = findViewById(R.id.txtBarcodeValue);
        surfaceView = findViewById(R.id.surfaceView);
        btnAction = findViewById(R.id.btnAction);

        //create button listener
        btnAction.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if (QRdata.length() > 0) {
                    startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(QRdata)));
                }
            }
        });
        try {
            //setup encryption
            //create key
            String key = "MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC8nRTnRduk1ADfsqUVVW8J5yQ8P7UF4DKv/B+p867wrfyIcZAR6eMb0PWh7SermSeNnJArAL279PnkQEaQswv7sJ/ecAJMrB50ouojHNwS0vKetcXjbEhgR39TBjcOZePIa/PhJu3e+mi+3EzVZ9RqAJmMC951r9k49m3PTyXjrQ9Hpg4WzJenxtdYhEfs9Av/XOkzR2IaT1JGpuaLGn1hjv9ZzW6Qb0KoRle6ibhhD88cr+IAKRVq0YgXYZyIfzIsPRse4tAMz3ax/EQq02agKCmdTujlYZ0/evJZip0HdncqF/AtzV1Ji1WI/un8Z05onkpAWfqjyxg81L9e9itBAgMBAAECggEAXXiDCXHnPbIKlNFVWlMyaffwTyNLNJQ8ylXp4zFuOrwecAfHW/lKoVhWwl5i0HlfzqAOGiGN5X2r8V+hGMiCYcLQF03u9cw+c5Lg8XG15mY/8kMmxGO/ImeMQ7rKwgngbkyBWc0PCPeTvTIzqXaBH98YOP0Qy8XPopkNJjWVE1SvqjpI3DisjSLoJcaJdqHWB7J06GebeXTr/7sTaKfKUkcu4zxmIiBETnxemtrn/EY9TkFjztDyaHaQOurUq6V8PO0G0l07IV3UXMgA0eFw1Q1Pm0EkkVj2+py5WFLPuJHt/KSeWNVnkmetBjZZn6I+gwSSmkiWnDOQjGs7QkjogQKBgQDveXeZp+O8m/ZUIDFiGM8zdhT3jy7eesPuJZKTy309/TZW/3G62FB7IU9ujogqpJk97/iaX8qDsiqKlXCP5VPA/gAVZSKdN4ua2Wm6eXk7sAb5rZQ6uulIrd4MDK+m7+6UqLuVckoVP4O8+EouQsLtLeEKcnKeDxNCROEhh93vuQKBgQDJoRxxcyNeEQltmfrHtZD4Lefy8VJzIAm3bH0FrYnlmMRqKJxrm7GTPwKJVGoU4EdC1j34qQy52L2/rujOyhdPzcv+JczkmtWOfBRAX3ghZYbhA8qiq3F4X5QihzbeOrRF9Ypc/bnKuoDsl0zs3QDCO/3rFDxTShZmt+8ED6gLyQKBgAno5OIe6HWtnovsqR5+GFTw1f1Il4/tVJ5OP7qN+SjPiagf+fzZZrsxra/NhiT9mrnNbGQ3ApJglRIXDQlnXAfoeuhnvv7yhXxq8s0cqb+mkSNT44Zqpay0RTQKclpeI2lTci/FAvvOHQ182NUBPj/CXkWoZsXTqeBcKVTR4oVBAoGBAIgEsr5p8Nr9XUHd1UqyVqjFtyqx13AolcVyX2jcKCGGDEKdQOBq+MEfiaOBGcsZfZk+FDJSQG6DI4ZTBWSy+kTwzQOXFoDFXvmvBK5keRL2faYAO8u/Il4VBEbCtqX2LjTfrsaKt7JmXKC+dLt5X5CojePvE78QRMponMo9kZzZAoGBAN0M47HBV0IaADwnD8X9PRZZXAI9yhmaU2bCmXCo8xMTel705v+yp4AGPUMLuShEv2r8CMwj1IZABjEs8Utv06dbQ3HHqUSqa/akbGFTc9luRjv69QbywGXgA7Y9SKKYmIx85xGNQmTby7n60apphRm0JQwi6LGLS7CvBxGFukBJ";
            byte[] pkcs8EncodedBytes = Base64.decode(key, Base64.DEFAULT);

            // extract the private key
            PKCS8EncodedKeySpec keySpec = new PKCS8EncodedKeySpec(pkcs8EncodedBytes);
            KeyFactory kf = KeyFactory.getInstance("RSA");
            PrivateKey privKey = kf.generatePrivate(keySpec);

            //create cipher
            cipher = Cipher.getInstance("RSA");
            cipher.init(Cipher.DECRYPT_MODE, privKey);

        }
        catch (Exception e){
            Toast.makeText(getApplicationContext(), "Key initialization failed - ", Toast.LENGTH_SHORT).show();
            e.printStackTrace();
        }


    }


    private void initialiseDetectorsAndSources() {

        Toast.makeText(getApplicationContext(), "Barcode scanner started", Toast.LENGTH_SHORT).show();

        //initialize barcode / camera componenets
        barcodeDetector = new BarcodeDetector.Builder(this)
                .setBarcodeFormats(Barcode.ALL_FORMATS)
                .build();

        cameraSource = new CameraSource.Builder(this, barcodeDetector)
                .setRequestedPreviewSize(1920, 1080)
                .setAutoFocusEnabled(true) //you should add this feature
                .build();

        //initialize camera surface
        surfaceView.getHolder().addCallback(new SurfaceHolder.Callback() {
            @Override
            public void surfaceCreated(SurfaceHolder holder) {
                try {
                    if (ActivityCompat.checkSelfPermission(ScanQRCodeActivity.this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
                        cameraSource.start(surfaceView.getHolder());
                    } else {
                        ActivityCompat.requestPermissions(ScanQRCodeActivity.this, new
                                String[]{Manifest.permission.CAMERA}, REQUEST_CAMERA_PERMISSION);
                    }

                } catch (IOException e) {
                    e.printStackTrace();
                }
            }


            //required overrides
            @Override
            public void surfaceChanged(SurfaceHolder holder, int format, int width, int height) {
            }

            @Override
            public void surfaceDestroyed(SurfaceHolder holder) {
                cameraSource.stop();
            }
        });


        //process for barcodeDetector
        barcodeDetector.setProcessor(new Detector.Processor<Barcode>() {
            @Override
            public void release() {
                Toast.makeText(getApplicationContext(), "barcode scanner has stopped", Toast.LENGTH_SHORT).show();
            }

            //detection handling
            @Override
            public void receiveDetections(Detector.Detections<Barcode> detections) {
                SparseArray<Barcode> barcodes = detections.getDetectedItems();
                if (barcodes.size() != 0) {
                    txtBarcodeValue.post(new Runnable() {
                        @Override
                        public void run() {
                            // create QRdata value
                            QRdata = barcodes.valueAt(0).displayValue;

                            // try decryption
                            try {
                                // decode QRData
                                byte[] decodedData = Base64.decode(QRdata, Base64.DEFAULT);

                                //decrypt
                                decryptedBytes = cipher.doFinal(decodedData);
                                decrypted = new String(decryptedBytes);

                                // update display data
                                txtBarcodeValue.setText(decrypted);
                                btnAction.setText("AUTHENTICATE MANUALLY");

                            } catch(Exception e){
                                Toast.makeText(getApplicationContext(), "Decryption failed", Toast.LENGTH_SHORT).show();
                                txtBarcodeValue.setText(QRdata);
                            }


                        }
                    });

                }
            }
        });
    }


    @Override
    protected void onPause() {
        super.onPause();
        cameraSource.release();
    }

    @Override
    protected void onResume() {
        super.onResume();
        initialiseDetectorsAndSources();


    }
}
