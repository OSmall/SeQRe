package com.seqre.androidapp.ui.home;

import android.content.Intent;
import android.view.View;
import android.widget.TextView;

import androidx.lifecycle.LiveData;
import androidx.lifecycle.MutableLiveData;
import androidx.lifecycle.ViewModel;

import com.seqre.androidapp.MainActivity;
import com.seqre.androidapp.QRScanning;
import com.seqre.androidapp.R;


public class HomeViewModel extends ViewModel{

    private MutableLiveData<String> mText;

    public HomeViewModel() {
        mText = new MutableLiveData<>();
        mText.setValue("This is home fragment");
    }


    public LiveData<String> getText() {
        return mText;
    }
}