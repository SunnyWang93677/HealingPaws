package com.example.stage3_project2.Contacts;

import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.os.Handler;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.TextView;

import com.example.Reader.R;
import com.example.Setting.BitmapUtils;
import com.example.Setting.SettingDatabase;
import com.hyphenate.EMMessageListener;
import com.hyphenate.chat.EMClient;
import com.hyphenate.chat.EMConversation;
import com.hyphenate.chat.EMMessage;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

/*
** https://blog.csdn.net/weixin_43980777/article/details/101715641
 */

public class ECChatActivity extends AppCompatActivity implements EMMessageListener {
    Handler handler = new Handler(){
        @Override
        public void handleMessage(android.os.Message msg) {
            super.handleMessage(msg);
            switch (msg.what){
                case 0:
                    adapter.notifyDataSetChanged();
                    break;
                case 1:
                    if (portraitByte != null) {
                        Bitmap bitmap = BitmapUtils.getImage(portraitByte);
                        if(bitmap != null){
                            if(getUserNameFromP.equals(chatWith)){
                                contactorImage.setImageBitmap(bitmap);
                            }
                            else if(getUserNameFromP.equals(you)){
                                youImage.setImageBitmap(bitmap);
                            }
                        }else{
                            Log.d("Fail portrait","Fail to set bitmap in conversation");
                        }


                    }else{
                        Log.d("Fail portrait","Fail to set portrait in conversation");
                    }
                    break;
            }
        }
    };

    private ImageButton backFromChatting;
    // 聊天信息输入框
    private EditText inputEdit;
    // 发送按钮
    private Button sendBt;

    private EMMessageListener messageListener;
    private String chatWith;
    private EMConversation mConversation;
    private RecyclerView mRecyclerView;
    private List mList = new ArrayList();
    private MessageAdapter adapter;
    private TextView chatWith_name;
    private DBContacts dbHelper;
    private SQLiteDatabase db;
    private Statement stmt;
    Connection conn;
    ResultSet resultSet;
    private String you;
    SettingDatabase sd;
    private SQLiteDatabase dbSetting;
    int currentMsgId = 0;
    ImageView youImage;
    ImageView contactorImage;
    byte[] portraitByte;
    String getUserNameFromP;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.conversation);

        chatWith = getIntent().getStringExtra("chatWith");
        messageListener = this;
        youImage = findViewById(R.id.you);
        contactorImage = findViewById(R.id.contactor);
        sd = new SettingDatabase(this,"Usertable.db",null,3);
        dbSetting = sd.getWritableDatabase();
        dbHelper = new DBContacts(this,"Messagetable.db",null,3);
        db = dbHelper.getWritableDatabase();
        //

//        getCurrentMsgId();//获得message数据库的最大id
        getYou();//获得用户名字
        initView();
        initConversation();
    }

    private void initView() {
        inputEdit = (EditText) findViewById(R.id.message_edit);
        sendBt = (Button) findViewById(R.id.send_bt);
        mRecyclerView = (RecyclerView) findViewById(R.id.mRecyclerView);
        backFromChatting = (ImageButton) findViewById(R.id.backFromChatting);
        chatWith_name = (TextView) findViewById(R.id.chatWith_name);
        LinearLayoutManager layoutManager = new LinearLayoutManager(this);
        mRecyclerView.setLayoutManager(layoutManager);

        backFromChatting.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(ECChatActivity.this, ECMainActivity.class);
                startActivity(intent);
                finish();
            }
        });

        setMessage();//放上聊天记录
//        setPortrait();

        sendBt.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String content = inputEdit.getText().toString();
                if (!TextUtils.isEmpty(content)) {
                    Message msg = new Message(content, Message.SEND);
                    mList.add(msg);
                    new  Thread(){
                        @Override
                        public  void run(){
                            try {//插入发送的消息
                                Class.forName("com.mysql.jdbc.Driver");
                                String url = "jdbc:mysql://cdb-s1xmk5a8.bj.tencentcdb.com:10244/While_Reading";
                                conn = DriverManager.getConnection(url, "root", "jwyc990702");
                                int id = currentMsgId+1;
                                String sql = "insert into messageTable(id,receiveUserName,sendUserName,Message,type) values(" +
                                        id+","+
                                        "'"+chatWith+"',"+
                                        "'"+you+"',"+
                                        "'"+content+"',"+ Message.SEND+");";
                                stmt = conn.prepareStatement(sql);
                                stmt.executeUpdate(sql);
                                handler.sendEmptyMessage(0);
                            } catch (SQLException e) {
                                e.printStackTrace();
                            } catch (ClassNotFoundException e) {
                                e.printStackTrace();
                            } finally {
                                try {

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

                    adapter = new MessageAdapter((List<Message>) mList);
                    mRecyclerView.setAdapter(adapter);
                    //当有新消息时，刷新RecyclerView中的显示
                    adapter.notifyItemInserted(mList.size() - 1);
                    //使用RecyclerView加载新聊天页面
                    mRecyclerView.scrollToPosition(mList.size() - 1);
                    inputEdit.setText("");
                    EMMessage message = EMMessage.createTxtSendMessage(content, chatWith);
                    EMClient.getInstance().chatManager().sendMessage(message);
                }
            }
        });
    }


    private void initConversation() {
        mConversation = EMClient.getInstance().chatManager().getConversation(chatWith, null, true);
        chatWith_name.setText(chatWith);
    }

    @Override
    protected void onResume() {
        super.onResume();
        EMClient.getInstance().chatManager().addMessageListener(messageListener);
    }

    @Override
    protected void onStop() {
        super.onStop();
    }



    @Override
    public void onMessageReceived(List<EMMessage> messages) {
        //收到消息
        String result = messages.get(0).getBody().toString();
        String received = result.substring(5, result.length() - 1);
        System.out.print("onReceived "+result);
        Log.d("onReceived", result);
        final Message message = new Message(received, Message.RECEIVED);
        new  Thread(){
            @Override
            public  void run(){
                try {//插入收到的消息
                    Class.forName("com.mysql.jdbc.Driver");
                    String url = "jdbc:mysql://cdb-s1xmk5a8.bj.tencentcdb.com:10244/While_Reading";
                    conn = DriverManager.getConnection(url, "root", "jwyc990702");
                    int id = currentMsgId+1;
                    System.out.print("id id "+id);
                    String sql = "insert into messageTable(id,sendUserName,receiveUserName,Message,type) values(" +
                            id+
                            "'"+chatWith+"',"+
                            "'"+you+"',"+
                            "'"+received+"',"+ Message.RECEIVED+");";
                    stmt = conn.prepareStatement(sql);
                    stmt.executeUpdate(sql);
                    handler.sendEmptyMessage(0);
                } catch (SQLException e) {
                    e.printStackTrace();
                } catch (ClassNotFoundException e) {
                    e.printStackTrace();
                } finally {
                    try {

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

        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                mList.add(message);
                adapter = new MessageAdapter((List<Message>) mList);
                mRecyclerView.setAdapter(adapter);
                mRecyclerView.scrollToPosition(mList.size() - 1);
            }
        });
    }

    @Override
    public void onCmdMessageReceived(List<EMMessage> list) {

    }

    @Override
    public void onMessageRead(List<EMMessage> messages) {

    }

    @Override
    public void onMessageDelivered(List<EMMessage> messages) {

    }

    @Override
    public void onMessageRecalled(List<EMMessage> messages) {

    }

    @Override
    public void onMessageChanged(EMMessage message, Object change) {

    }

    private void setPortrait(){
        new  Thread() {
            @Override
            public void run() {
                try {
                    Class.forName("com.mysql.jdbc.Driver");
                    String url = "jdbc:mysql://cdb-s1xmk5a8.bj.tencentcdb.com:10244/While_Reading";
                    conn = DriverManager.getConnection(url, "root", "jwyc990702");
                    String sql = "SELECT img, userName FROM portrait WHERE (userName='"+chatWith+
                            "') OR (userName='"+you+"');";
                    stmt = conn.prepareStatement(sql);
                    resultSet = stmt.executeQuery(sql);
                    if(resultSet != null){
                        while(resultSet.next()){
                            portraitByte = resultSet.getBytes(1);
                            Log.d("uploadImageToDB","uploadImageToDB "+portraitByte.toString());
                            String userName = resultSet.getString(2);
                            getUserNameFromP = userName;
                        }
                        handler.sendEmptyMessage(1);
                        if(resultSet.next()==false){

                        }
                    }else{
                        Log.d("setPortrait()","setPortrait() null");
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
    }

    private void setMessage(){
        new  Thread() {
                @Override
                public void run() {
                try {
                    Class.forName("com.mysql.jdbc.Driver");
                    String url = "jdbc:mysql://cdb-s1xmk5a8.bj.tencentcdb.com:10244/While_Reading";
                    conn = DriverManager.getConnection(url, "root", "jwyc990702");
                    String sql = "SELECT Message,type,receiveUserName FROM messageTable WHERE (receiveUserName='"+chatWith+"' AND sendUserName='"+you+
                            "') OR (sendUserName='"+chatWith+"' AND receiveUserName='"+you+"');";
                    stmt = conn.prepareStatement(sql);
                    resultSet = stmt.executeQuery(sql);
                    if(resultSet != null){
                        while(resultSet.next()){
                            String content = resultSet.getString(1);
                            int type = resultSet.getInt(2);
                            String receiver = resultSet.getString(3);
                            if(receiver.equals(you)){
                                type = 0;
                            }
                            Message message = new Message(content,type);
                            mList.add(message);
                        }
                        handler.sendEmptyMessage(0);
                        if(resultSet.next()==false){

                        }
                    }else{
                        Log.d("setMessage()","setMessage() null");
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
        adapter = new MessageAdapter((List<Message>) mList);
        mRecyclerView.setAdapter(adapter);
        mRecyclerView.scrollToPosition(mList.size() - 1);

    }

    public void getYou(){
        Cursor cursor = dbSetting.query("Usertable",null,null,null,null,null,null);
        if(cursor.moveToFirst()){
            do {
                you = cursor.getString(cursor.getColumnIndex("userName"));
                Log.d("youyouyou",you);
            }while(cursor.moveToNext());
        }else{
            Log.d("youyouyou","noValue");
        }
        cursor.close();

    }




}