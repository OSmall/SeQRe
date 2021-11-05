package com.seqre;

import android.os.Bundle;
import android.view.View;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.RadioButton;
import androidx.appcompat.app.AppCompatActivity;


public class SettingsActivity extends AppCompatActivity {

    TextView settings_txt;
    ImageView logo_settings;
    EditText set_email, set_userID, set_password;
    RadioButton biometric_yes, biometric_no;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        //create local variables
        settings_txt = findViewById(R.id.settingsText);

        //setup logo
        logo_settings = findViewById(R.id.logo_register);
        logo_settings.setImageResource(R.drawable.big_logo);

        //setup radiogroup
        biometric_yes = findViewById(R.id.biometric_yes);
        biometric_no = findViewById(R.id.biometric_no);

        //setup input texts
        set_email = findViewById(R.id.email);
        set_userID = findViewById(R.id.userID);
        set_password = findViewById(R.id.password);
    }

    public void onRadioButtonClicked(View view) {
        // Is the button now checked?
        boolean checked = ((RadioButton) view).isChecked();

        // Check which radio button was clicked
        switch(view.getId()) {
            case R.id.biometric_yes:
                if (checked)
                    // Pirates are the best
                    break;
            case R.id.biometric_no:
                if (checked)
                    // Ninjas rule
                    break;
        }
    }
}
