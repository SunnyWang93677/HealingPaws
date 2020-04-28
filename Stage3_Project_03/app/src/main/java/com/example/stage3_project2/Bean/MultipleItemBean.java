package com.example.stage3_project2.Bean;

public class MultipleItemBean extends TestBean {
    public MultipleItemBean(String title, String content, String status) {
        super(title, content);
        this.status = status;
    }

    public MultipleItemBean(String title, String content,String status, int itemType) {
        super(title, content);
        this.status = status;
        this.itemType = itemType;
    }
    private String status;

    private int itemType;

    public String getStatus(){
        return status;
    }

    public int getItemType() {
        return itemType;
    }

    public void setItemType(int itemType) {
        this.itemType = itemType;
    }
}
