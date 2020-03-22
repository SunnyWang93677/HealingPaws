package com.example.stage3_project2.Contacts;

import android.content.ComponentName;
import android.content.ContentValues;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.text.TextUtils;
import android.util.Log;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.example.Reader.MainActivity;
import com.example.Reader.R;
import com.example.Setting.BitmapUtils;
import com.example.Setting.DBHelper;
import com.example.Setting.SettingActivity;
import com.example.Setting.SettingDatabase;
import com.google.android.material.navigation.NavigationView;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import androidx.annotation.NonNull;
import androidx.appcompat.app.ActionBarDrawerToggle;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.core.view.GravityCompat;
import androidx.drawerlayout.widget.DrawerLayout;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

public class ECMainActivity extends AppCompatActivity {

    private EditText chatWith;
    private Button mStartChatBtn;

    private Statement stmt;
    Connection conn;
    ResultSet resultSet;
    private List<ContactsItem> contactorsList;
    private ContactsAdapter ContactorsListAdapter;
    private DBContacts dbContacts;
    private RecyclerView contactorsListView;
    private DrawerLayout mDrawerLayout;
    DBHelper dbHelper;
    private SQLiteDatabase dbSetting;
    SettingDatabase sd;
    private String userName;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        sd = new SettingDatabase(this, "Usertable.db",null,3);
        dbSetting = sd.getWritableDatabase();

        Cursor cursor = dbSetting.query("Usertable",null,null,null,null,null,null);
        if(cursor.moveToFirst()){
            do {
                userName = cursor.getString(cursor.getColumnIndex("userName"));
                Log.d("youyouyou",userName);
            }while(cursor.moveToNext());
        }else{
            Log.d("youyouyou","noValue");
        }
        cursor.close();

        setTheme(new DBHelper(this).getTheme("theme",userName));
        setContentView(R.layout.conversation_seek1);
        //初始化数据库
        dbHelper = new DBHelper(this);



        dbContacts = new DBContacts(this, "Contactstable.db",null,3);

        initView();

        //加载顶部菜单栏（别的活动可能也需要）
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        //抽屉布局
        mDrawerLayout = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle;
        toggle = new ActionBarDrawerToggle(this, mDrawerLayout, toolbar, R.string.navigation_drawer_open,R.string.navigation_drawer_close);
        mDrawerLayout.addDrawerListener(toggle);
        toggle.syncState();
        NavigationView naviView = findViewById(R.id.nav_view);
        View headerView = naviView.getHeaderView(0);
        de.hdodenhof.circleimageview.CircleImageView  headImage2 = headerView.findViewById(R.id.icon_image);
        byte[] data2 = dbHelper.getBitmapByName("pic",userName);
        if (data2 != null)   {
            Bitmap bitmap = BitmapUtils.getImage(data2);
            headImage2.setImageBitmap(bitmap);
        }
        TextView username = headerView.findViewById(R.id.username);
        username.setText(userName);

        //navi栏的默认选择
        naviView.setCheckedItem(R.id.nav_settings);
        //对navi栏进行事件监听

        //你们的活动加载写在这个函数里面
        naviView.setNavigationItemSelectedListener(new NavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem menuItem) {
                int id = menuItem.getItemId();
                if(id == R.id.nav_reader){
                    Intent intent = new Intent( ECMainActivity.this,com.example.Reader.MainActivity.class);
                    startActivity(intent);
                    finish();
                }else if(id == R.id.nav_settings){
                    Intent intent = new Intent();
                    intent.setComponent(new ComponentName(ECMainActivity.this, com.example.Setting.SettingActivity.class));
                    startActivity(intent);
                    finish();
                } else if(id == R.id.nav_contacts) {
                    mDrawerLayout.closeDrawer(GravityCompat.START);

                }else if(id == R.id.nav_posts) {
                    Intent intent = new Intent();
                    intent.setComponent(new ComponentName(ECMainActivity.this, com.example.Posts.PostsActivity.class));
                    startActivity(intent);
                    finish();
                }
                return true;
            }
        });
    }


    private void initView() {
        chatWith = (EditText) findViewById(R.id.ec_edit_chat_id);
        mStartChatBtn = (Button) findViewById(R.id.ec_btn_start_chat);
        contactorsListView = (RecyclerView) findViewById(R.id.contactors_list);
        SQLiteDatabase db = dbContacts.getWritableDatabase();

        mStartChatBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String chatId = chatWith.getText().toString();
                Toast.makeText(ECMainActivity.this, chatId, Toast.LENGTH_SHORT).show();
                if (!TextUtils.isEmpty(chatId)) {

                    if (chatId.equals(userName)) {
                        Toast.makeText(ECMainActivity.this, "No Chatting with yourself", Toast.LENGTH_SHORT).show();
                        return;
                    }

                    new  Thread() {
                        @Override
                        public void run() {
                            try {
                                Class.forName("com.mysql.jdbc.Driver");
                                String url = "jdbc:mysql://cdb-s1xmk5a8.bj.tencentcdb.com:10244/While_Reading";
                                conn = DriverManager.getConnection(url, "root", "jwyc990702");
                                String sql = "SELECT contact FROM contacts WHERE (contact='"+chatId+"' AND you='"+userName+"');";
                                stmt = conn.prepareStatement(sql);
                                resultSet = stmt.executeQuery(sql);

                                    if(!resultSet.next()){
                                        String sql2 = "insert into contacts(you,contact) values(" +
                                                "'"+userName+"',"+
                                                "'"+chatId+"');";
                                        stmt = conn.prepareStatement(sql2);
                                        stmt.executeUpdate(sql2);
                                    }

                            }catch (SQLException e){
                                e.printStackTrace();
                            } catch (ClassNotFoundException e) {
                                e.printStackTrace();
                            }finally {
                                try {
                                    if(resultSet != null){
                                        resultSet.close();
                                    }
                                    if(stmt !=null) {
                                        stmt.close();
                                    }
                                    if(conn !=null) {
                                        conn.close();
                                    }
                                } catch (SQLException e) {
                                    e.printStackTrace();
                                }

                            }
                        }
                    }.start();


                    //判断是否需要添加到contacts里
                    Cursor cursor = db.rawQuery("select userName from ContactsTable where userName like ?", new String[]{chatId});
                    if(!cursor.moveToFirst()){
                        ContentValues values = new ContentValues();
                        values.put("userName", chatId);
                        values.put("youName", userName);
                        db.insert("Contactstable",null,values);
                    }
                    cursor.close();

                    Intent intent = new Intent(ECMainActivity.this, ECChatActivity.class);
                    intent.putExtra("chatWith", chatId);
                    startActivity(intent);
                    finish();
                } else {
                    Toast.makeText(ECMainActivity.this, "Username should not be null", Toast.LENGTH_LONG).show();
                }
            }
        });

        contactorsList = getContactorsList();

        LinearLayoutManager layoutManager = new LinearLayoutManager(this);
        contactorsListView.setLayoutManager(layoutManager);
        ContactorsListAdapter = new ContactsAdapter(this,contactorsList);
        contactorsListView.setAdapter(ContactorsListAdapter);
    }

    public List<ContactsItem> getContactorsList(){
        List<ContactsItem> contactorsList = new ArrayList<ContactsItem>();
        SQLiteDatabase db = dbContacts.getWritableDatabase();
        Cursor cursor = db.rawQuery("select userName from ContactsTable where youName like ?", new String[]{userName});
        if(cursor.moveToFirst()) {
            do {
                String userName = cursor.getString(cursor.getColumnIndex("userName"));
                ContactsItem contactors = new ContactsItem(userName);
                contactorsList.add(contactors);
            }while(cursor.moveToNext());

        }
        cursor.close();
        return contactorsList;

    }


}
