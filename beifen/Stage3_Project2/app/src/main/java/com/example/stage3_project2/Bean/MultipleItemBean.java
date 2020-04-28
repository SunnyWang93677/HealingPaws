package com.example.stage3_project2.Bean;

public class MultipleItemBean extends TestBean {
    public MultipleItemBean(String title, String content) {
        super(title, content);
    }

    public MultipleItemBean(String title, String content, int itemType) {
        super(title, content);
        this.itemType = itemType;
    }

    private int itemType;

    public int getItemType() {
        return itemType;
    }

    public void setItemType(int itemType) {
        this.itemType = itemType;
    }
}
