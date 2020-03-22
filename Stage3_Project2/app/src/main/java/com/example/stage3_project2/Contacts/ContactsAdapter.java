package com.example.stage3_project2.Contacts;

import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Handler;
import android.support.v7.widget.RecyclerView;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import com.example.Reader.R;
import com.example.Setting.SettingDatabase;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.List;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AlertDialog;
import androidx.recyclerview.widget.RecyclerView;

public class ContactsAdapter extends RecyclerView.Adapter<ContactsAdapter.ViewHolder>{

    Handler handler = new Handler() {
        @Override
        public void handleMessage(android.os.Message msg) {
            super.handleMessage(msg);
            switch (msg.what) {
                case 0:
                    notifyDataSetChanged();
                    break;
            }
        }
    };

    private Statement stmt;
    Connection conn;
    ResultSet resultSet;
    private List<ContactsItem> contactsItemList;
    Context context;
    private SQLiteDatabase dbSetting;
    private String userName;



    public ContactsAdapter(Context context, List<ContactsItem> contactsItems) {
        this.contactsItemList = contactsItems;
        this.context = context;
    }

    class ViewHolder extends RecyclerView.ViewHolder {
        private View view;
        private TextView contactName;
        public ViewHolder(View view) {
            super(view);
            this.view = view;
            contactName = (TextView) view.findViewById(R.id.contactName);
        }
    }

    @NonNull
    @Override
    public ContactsAdapter.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View view = View.inflate(parent.getContext(), R.layout.contacts_item, null);
        ContactsAdapter.ViewHolder holder = new ContactsAdapter.ViewHolder(view);
        return holder;
    }

    @Override
    public void onBindViewHolder(@NonNull ContactsAdapter.ViewHolder holder, int position) {
        dbHelper = new DBContacts(context, "Contactstable.db", null, 3);
        final SQLiteDatabase db = dbHelper.getWritableDatabase();

        sd = new SettingDatabase(context, "Usertable.db",null,3);
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

        ContactsItem contactsItem = contactsItemList.get(position);
        ViewHolder viewHolder = (ViewHolder) holder;
        viewHolder.contactName.setText(contactsItem.getUserName());
        holder.itemView.setOnClickListener(new View.OnClickListener(){

            @Override
            public void onClick(View v) {
                final int position = holder.getAdapterPosition();
                final ContactsItem contactsItem1 = contactsItemList.get(position);
                Intent intent = new Intent(context, ECChatActivity.class);
                intent.putExtra("chatWith", contactsItem1.getUserName());
                context.startActivity(intent);
            }

        });
        holder.itemView.setOnLongClickListener(new View.OnLongClickListener() {
            @Override
            public boolean onLongClick(View v) {
                final int position = holder.getAdapterPosition();
                final ContactsItem contactsItem1 = contactsItemList.get(position);
                //dialog
                AlertDialog.Builder dialog = new AlertDialog.Builder(context);
                dialog.setTitle("Warning");
                dialog.setMessage("Do you want to delete this user?");
                dialog.setCancelable(false);
                dialog.setPositiveButton("OK", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        String name = String.valueOf( contactsItem1.getUserName());
                        new  Thread(){
                            @Override
                            public  void run(){
                                try {//插入发送的消息
                                    Class.forName("com.mysql.jdbc.Driver");
                                    String url = "jdbc:mysql://cdb-s1xmk5a8.bj.tencentcdb.com:10244/While_Reading";
                                    conn = DriverManager.getConnection(url, "root", "jwyc990702");
                                    String sql = "delete from contacts where you = ('" +
                                            userName+ "' and contact = '"+name+"');";
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

                        db.delete("Contactstable","userName = ?",new String[]{ name });
                        contactsItemList.remove(position);
                        notifyDataSetChanged();
                    }

                });
                dialog.setNegativeButton("Cancel", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {

                    }
                });
                dialog.show();
                return true;
            }
        });

    }

    @Override
    public int getItemCount() {
        return contactsItemList.size();
    }
}
