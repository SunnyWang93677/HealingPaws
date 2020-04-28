package com.example.stage3_project2.Appointment;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import com.example.stage3_project2.Emp_MainActivity;
import com.example.stage3_project2.R;

public class Emp_OrderTreat extends AppCompatActivity {
    ImageView addTreat;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_emp_order_treat);
        addTreat = findViewById(R.id.addTreatButton);
        addTreat.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(Emp_OrderTreat.this, Emp_MainActivity.class);
                startActivity(intent);
            }
        });
    }


}
