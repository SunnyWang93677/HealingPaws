package com.example.stage3_project2.Pets;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import com.example.stage3_project2.R;

public class ViewPets extends AppCompatActivity {
    private Button addPet;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_view_pets);
        initView();
        init();
    }

    public void initView(){
        addPet = findViewById(R.id.addPet);
    }

    public void init(){
        addPet.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                Intent intent = new Intent(ViewPets.this, AddPets.class);
                startActivity(intent);
            }
        });
    }

}
