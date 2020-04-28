package com.example.stage3_project2.Appointment;

import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.DatePicker;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.example.stage3_project2.MainActivity;
import com.example.stage3_project2.R;

import java.text.SimpleDateFormat;
import java.util.Calendar;

public class AddAppointment extends AppCompatActivity {
    DatePicker dp;
    Button pickPets;
    RelativeLayout rlPetsInfo;
    TextView tvyourPets;
    ImageView makeAppointment;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_appointment);
        dp = (DatePicker)findViewById(R.id.AppointDatePicker);
        pickPets = (Button)findViewById(R.id.pickPets);
        rlPetsInfo = (RelativeLayout)findViewById(R.id.rlPetsInfo);
        tvyourPets = (TextView)findViewById(R.id.tvyourPets);
        makeAppointment = (ImageView)findViewById(R.id.makeAppointment);
        init();
    }

    public void init(){
        pickDate();
        pickPet();
        lanuch();
    }

    public void pickDate(){
        dp.init(2020, 3, 16, new DatePicker.OnDateChangedListener() {
            @Override
             public void onDateChanged(DatePicker view, int year,
                     int monthOfYear, int dayOfMonth) {
                                 // 获取一个日历对象，并初始化为当前选中的时间
                                 Calendar calendar = Calendar.getInstance();
                                 calendar.set(year, monthOfYear, dayOfMonth);
                                 SimpleDateFormat format = new SimpleDateFormat(
                                                 "yyyy-MM-dd-  HH:mm");
                                 Toast.makeText(AddAppointment.this,
                                                 format.format(calendar.getTime()), Toast.LENGTH_SHORT)
                                         .show();
                             }
         });

    }

    public void pickPet(){
        pickPets.setOnClickListener(new View.OnClickListener() {
            String pets="";
            @Override
            public void onClick(View v) {
                final String[] item = {"Cathy", "Bob","Dube","Billy","Thereshod","Cat","Tim","Han"};
                final boolean[] selected = {false, false, false, false, false, false, false, false};
                AlertDialog.Builder builder = new AlertDialog.Builder(AddAppointment.this);
                builder.setTitle("Choose your pets");

                builder.setMultiChoiceItems(item, selected, new DialogInterface.OnMultiChoiceClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which, boolean isChecked) {
                        Toast.makeText(AddAppointment.this, item[which] + " "+isChecked, Toast.LENGTH_SHORT).show();
                        pets = pets+ " "+item[which];
                    }
                });
                builder.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.dismiss();
                        Toast.makeText(AddAppointment.this, "OK", Toast.LENGTH_SHORT).show();

                        rlPetsInfo.setVisibility(View.VISIBLE);
//                        String n = "";
//                        if(item[0].is)
//                            n = ""+selected[0];
//                        for (int i = 1; i < selected.length; i++) {
////                            Log.e("hongliang", "" + selected[i]);
//                            n = n+", "+selected[i];
//                        }
                        tvyourPets.setText(pets);

                    }
                });
                builder.create().show();
            }
        });

    }

    public void lanuch(){
        makeAppointment.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(AddAppointment.this, MainActivity.class);
                startActivity(intent);
            }
        });
    }


}
