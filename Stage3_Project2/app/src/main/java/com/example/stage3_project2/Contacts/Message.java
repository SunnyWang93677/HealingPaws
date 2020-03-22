package com.example.stage3_project2.Contacts;
/*
** https://blog.csdn.net/weixin_43980777/article/details/101715641
 */


public class Message {
    public static final int RECEIVED = 0;
    public static final int SEND = 1;

    private String content;
    private int type;

    public Message(String content, int type) {
        this.content = content;
        this.type = type;
    }

    public String getContent() {
        return content;
    }

    public int getType() {
        return type;
    }
}
