package tools;

import android.content.Context;
import android.content.SharedPreferences;

import static android.content.Context.MODE_PRIVATE;

public class SharedPreferenceHelper {



    public static void  setLoggingStatus(Context context, boolean status)
    {
        SharedPreferences sharedPreferences = context.getSharedPreferences("userLogStatus", MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();
        editor.putBoolean("LogStatus", status);
        editor.apply();
    }
}
