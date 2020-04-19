package com.example.stage3_project2.Login_Register;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.animation.ObjectAnimator;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.CardView;
import android.view.View;
import android.widget.Button;
import android.widget.RadioButton;
import android.widget.TextView;
import android.support.design.widget.TextInputEditText;

import com.example.stage3_project2.Emp_MainActivity;
import com.example.stage3_project2.MainActivity;
import com.example.stage3_project2.R;

import java.io.IOException;

import cn.pedant.SweetAlert.SweetAlertDialog;
import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

import static tools.ServerIP.LOGURL;
import static tools.ServerIP.SIGNURL;
import static tools.SharedPreferenceHelper.setLoggingStatus;

public class Login extends AppCompatActivity implements View.OnClickListener{
    private TextView Title;
    private Button logButton;
    private Button signButton;
    private TextInputEditText userNameForm;
    private TextInputEditText passWordForm;
    private SharedPreferences sharedPreferences;
    private CardView cardView;
    private String username;
    private RadioButton loginEmployee;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        logButton = (Button) findViewById(R.id.log_Button);
        signButton = (Button) findViewById(R.id.Sign_Button);
        userNameForm = (TextInputEditText) findViewById(R.id.username_Password);
        passWordForm = (TextInputEditText) findViewById(R.id.password_EditText);
        loginEmployee = (RadioButton) findViewById(R.id.loginEmployee);
        cardView = (CardView) findViewById(R.id.logSignCard);
        Title = (TextView) findViewById(R.id.textView);
        logButton.setOnClickListener(this);
        signButton.setOnClickListener(this);

    }

    @Override
    public void onClick(View v) {
        String userName = userNameForm.getText().toString();
        username = userName;
        String passWord = passWordForm.getText().toString();


        switch (v.getId())
        {
            case R.id.log_Button:
                if(userName.equals("")||passWord.equals(""))
                {
                    showWarnDialog("Empty!");
                    return;
                }

                String url = LOGURL;/*在此处改变你的服务器地址*/
                getCheckFromServer(url,userName,passWord);
                break;
            case R.id.Sign_Button:
                String url2 = SIGNURL;/*在此处改变你的服务器地址*/
//                registeNameWordToServer(url2,userName,passWord);
                if(!loginEmployee.isChecked()){
                    Intent intent = new Intent(Login.this, Register.class);
                    startActivity(intent);
                }else{
                    Intent intent = new Intent(Login.this, Emp_Register.class);
                    startActivity(intent);
                }

                break;
        }

    }

    private void getCheckFromServer(String url,final String userName,String passWord)
    {
        OkHttpClient client = new OkHttpClient();
        FormBody.Builder formBuilder = new FormBody.Builder();
        formBuilder.add("username", userName);
        formBuilder.add("password", passWord);
        Request request = new Request.Builder().url(url).post(formBuilder.build()).build();
        Call call = client.newCall(request);
        call.enqueue(new Callback()
        {
            @Override
            public void onFailure(Call call, IOException e)
            {
                runOnUiThread(new Runnable()
                {
                    @Override
                    public void run()
                    {
                        showWarnDialog("Server Wrong");
                    }
                });

            }

            @Override
            public void onResponse(Call call, Response response) throws IOException
            {
                if(response.isSuccessful()){
                    System.out.println("successssssss0");
                }
                else{
                    System.out.println(response.code());
                }

                final String res = response.body().string();
                runOnUiThread(new Runnable()
                {
                    @Override
                    public void run()
                    {
                        if (res.equals("0"))
                        {
                            showWarnDialog("Please register first");
                        }
                        else if(res.equals("1"))
                        {
                            showWarnDialog("Password Wrong");
                        }
                        else//成功
                        {
                            showSuccessSweetDialog("Welcome!");
                            sharedPreferences = getSharedPreferences("UserIDAndPassword", MODE_PRIVATE);
                            SharedPreferences.Editor editor = sharedPreferences.edit();
                            editor.putString("username", userName);
                            editor.apply();
                        }

                    }
                });
            }
        });

    }


    private void showWarnDialog(String info)
    {
        SweetAlertDialog pDialog = new SweetAlertDialog(this, SweetAlertDialog.WARNING_TYPE);
        pDialog.getProgressHelper().setBarColor(Color.parseColor("#A5DC86"));
        pDialog.setTitleText(info);
        pDialog.setCancelable(true);
        pDialog.show();
    }


    private void registeNameWordToServer(String url,final String userName,String passWord)
    {
        OkHttpClient client = new OkHttpClient();
        FormBody.Builder formBuilder = new FormBody.Builder();
        formBuilder.add("username", userName);
        formBuilder.add("password", passWord);
        Request request = new Request.Builder().url(url).post(formBuilder.build()).build();
        Call call = client.newCall(request);
        call.enqueue(new Callback()
        {
            @Override
            public void onFailure(Call call, IOException e)
            {
                runOnUiThread(new Runnable()
                {
                    @Override
                    public void run()
                    {
                        showWarnDialog("Server wrong");
                    }
                });
            }

            @Override
            public void onResponse(Call call, final Response response) throws IOException
            {
                final String res = response.body().string();
                runOnUiThread(new Runnable()
                {
                    @Override
                    public void run()
                    {
                        if (res.equals("0"))
                        {
                            showWarnDialog("This id has been used");
                        }
                        else
                        {
                            showSuccessDialog(res);
                            sharedPreferences = getSharedPreferences("UserIDAndPassword", MODE_PRIVATE);
                            SharedPreferences.Editor editor = sharedPreferences.edit();
                            editor.putString("username", userName);
                            editor.apply();
                        }

                    }
                });
            }
        });

    }

    private void showSuccessSweetDialog(String info)
    {
        final SweetAlertDialog pDialog = new SweetAlertDialog(this, SweetAlertDialog.SUCCESS_TYPE);
        pDialog.getProgressHelper().setBarColor(Color.parseColor("#A5DC86"));
        pDialog.setTitleText(info);
        pDialog.setCancelable(true);
        pDialog.show();
        pDialog.setConfirmClickListener(new SweetAlertDialog.OnSweetClickListener()
        {
            @Override
            public void onClick(SweetAlertDialog sweetAlertDialog)
            {
                pDialog.dismiss();
                playAndIntent(cardView);
            }
        });
    }

    private void showSuccessDialog(String info)
    {
        final SweetAlertDialog pDialog = new SweetAlertDialog(this, SweetAlertDialog.SUCCESS_TYPE);
        pDialog.getProgressHelper().setBarColor(Color.parseColor("#A5DC86"));
        pDialog.setTitleText(info);
        pDialog.setCancelable(true);
        pDialog.show();
        pDialog.setConfirmClickListener(new SweetAlertDialog.OnSweetClickListener()
        {
            @Override
            public void onClick(SweetAlertDialog sweetAlertDialog)
            {
                pDialog.dismiss();
                playAndIntent(cardView);
            }
        });
    }

    private void playAndIntent(View view)
    {
//        DBOpenHelper dbHelper = new DBOpenHelper(this, "friends.db", null, 1,username);
//        dbHelper.getWritableDatabase();
        setLoggingStatus(this,true);
        ObjectAnimator animator = ObjectAnimator.ofFloat(view, "translationY",-1000f);
        animator.setDuration(800);
        animator.addListener(new AnimatorListenerAdapter()
        {
            @Override
            public void onAnimationEnd(Animator animation)
            {
                Intent intent;
                if(!loginEmployee.isChecked()){
                    intent = new Intent(Login.this, MainActivity.class);
                }
                else{
                    intent = new Intent(Login.this, Emp_MainActivity.class);
                }
                intent.putExtra("connectServer", true);
                startActivity(intent);
                new Thread(new Runnable()//在后台线程中关闭此活动
                {
                    @Override
                    public void run()
                    {
                        try
                        {
                            Thread.sleep(1000);
                            Login.this.finish();
                        } catch (InterruptedException e)
                        {
                            e.printStackTrace();
                        }
                    }
                }).start();
            }
        });
        animator.start();
    }








}
