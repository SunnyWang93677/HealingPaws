package com.example.stage3_project2.Appointment;

import android.graphics.Color;
import android.graphics.PorterDuff;
import android.graphics.Typeface;
import android.renderscript.Sampler;
import android.support.v4.app.DialogFragment;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.text.SpannableStringBuilder;
import android.text.Spanned;
import android.text.style.StyleSpan;
import android.util.Pair;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.RadioButton;
import android.widget.RelativeLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import com.appeaser.sublimepickerlibrary.datepicker.SelectedDate;
import com.appeaser.sublimepickerlibrary.helpers.SublimeOptions;
import com.appeaser.sublimepickerlibrary.recurrencepicker.SublimeRecurrencePicker;
import com.example.stage3_project2.R;

import java.text.DateFormat;
import java.util.Calendar;

import static android.view.ViewGroup.LayoutParams.WRAP_CONTENT;

public class AddAppointment extends AppCompatActivity {
    Button pickTime;
    RelativeLayout rlDateTimeRecurrenceInfo;
    // Chosen values
    SelectedDate mSelectedDate;
    int mHour, mMinute;
    String mRecurrenceOption, mRecurrenceRule;

    // Views to display the chosen Date, Time & Recurrence options
    TextView tvYear, tvMonth, tvDay, tvHour,
            tvMinute, tvRecurrenceOption, tvRecurrenceRule,
            tvStartDate, tvEndDate;

    LinearLayout llDateHolder;

    AddAppointFragment.Callback mFragmentCallback = new AddAppointFragment.Callback() {
        @Override
        public void onCancelled() {
            rlDateTimeRecurrenceInfo.setVisibility(View.GONE);
        }

        @Override
        public void onDateTimeRecurrenceSet(SelectedDate selectedDate,
                                            int hourOfDay, int minute,
                                            SublimeRecurrencePicker.RecurrenceOption recurrenceOption,
                                            String recurrenceRule) {

            mSelectedDate = selectedDate;
            mHour = hourOfDay;
            mMinute = minute;
            mRecurrenceOption = recurrenceOption != null ?
                    recurrenceOption.name() : "n/a";
            mRecurrenceRule = recurrenceRule != null ?
                    recurrenceRule : "n/a";

            updateInfoView();

//            svMainContainer.post(new Runnable() {
//                @Override
//                public void run() {
//                    svMainContainer.scrollTo(svMainContainer.getScrollX(),
//                            cbAllowDateRangeSelection.getBottom());
//                }
//            });
        }
    };


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_appointment);
        initView();
        init();
    }


    public void initView(){
        pickTime = findViewById(R.id.pickTime);
        rlDateTimeRecurrenceInfo
                = (RelativeLayout) findViewById(R.id.rlDateTimeRecurrenceInfo);

        llDateHolder = (LinearLayout) findViewById(R.id.llDateHolder);

        // Initialize views to display the chosen Date, Time & Recurrence options
        tvYear = ((TextView) findViewById(R.id.tvYear));
        tvMonth = ((TextView) findViewById(R.id.tvMonth));
        tvDay = ((TextView) findViewById(R.id.tvDay));

        tvStartDate = ((TextView) findViewById(R.id.tvStartDate));
        tvEndDate = ((TextView) findViewById(R.id.tvEndDate));

        tvHour = ((TextView) findViewById(R.id.tvHour));
        tvMinute = ((TextView) findViewById(R.id.tvMinute));

        tvRecurrenceOption = ((TextView) findViewById(R.id.tvRecurrenceOption));
        tvRecurrenceRule = ((TextView) findViewById(R.id.tvRecurrenceRule));

        rlDateTimeRecurrenceInfo
                = (RelativeLayout) findViewById(R.id.rlDateTimeRecurrenceInfo);
    }

    public void init(){
        pickTime.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                // DialogFragment to host SublimePicker
                AddAppointFragment pickerFrag = new AddAppointFragment();
                pickerFrag.setCallback(mFragmentCallback);

                // Options
                Pair<Boolean, SublimeOptions> optionsPair = getOptions();

                if (!optionsPair.first) { // If options are not valid
                    Toast.makeText(AddAppointment.this, "No pickers activated",
                            Toast.LENGTH_SHORT).show();
                    return;
                }

                // Valid options
                Bundle bundle = new Bundle();
                bundle.putParcelable("SUBLIME_OPTIONS", optionsPair.second);
                pickerFrag.setArguments(bundle);

                pickerFrag.setStyle(DialogFragment.STYLE_NO_TITLE, 0);
                pickerFrag.show(getSupportFragmentManager(), "SUBLIME_PICKER");

            }
        });

    }


    // Validates & returns SublimePicker options
    Pair<Boolean, SublimeOptions> getOptions() {
        SublimeOptions options = new SublimeOptions();
        int displayOptions = 0;

//        if (cbDatePicker.isChecked()) {
            displayOptions |= SublimeOptions.ACTIVATE_DATE_PICKER;
//        }

//        if (cbTimePicker.isChecked()) {
//            displayOptions |= SublimeOptions.ACTIVATE_TIME_PICKER;
//        }
//
//        if (cbRecurrencePicker.isChecked()) {
//            displayOptions |= SublimeOptions.ACTIVATE_RECURRENCE_PICKER;
//        }

//        if (rbDatePicker.getVisibility() == View.VISIBLE && rbDatePicker.isChecked()) {
            options.setPickerToShow(SublimeOptions.Picker.DATE_PICKER);
//        }
//        else if (rbTimePicker.getVisibility() == View.VISIBLE && rbTimePicker.isChecked()) {
//            options.setPickerToShow(SublimeOptions.Picker.TIME_PICKER);
//        } else if (rbRecurrencePicker.getVisibility() == View.VISIBLE && rbRecurrencePicker.isChecked()) {
//            options.setPickerToShow(SublimeOptions.Picker.REPEAT_OPTION_PICKER);
//        }

        options.setDisplayOptions(displayOptions);

        // Enable/disable the date range selection feature
//        options.setCanPickDateRange(cbAllowDateRangeSelection.isChecked());

        // Example for setting date range:
        // Note that you can pass a date range as the initial date params
        // even if you have date-range selection disabled. In this case,
        // the user WILL be able to change date-range using the header
        // TextViews, but not using long-press.

        /*Calendar startCal = Calendar.getInstance();
        startCal.set(2016, 2, 4);
        Calendar endCal = Calendar.getInstance();
        endCal.set(2016, 2, 17);

        options.setDateParams(startCal, endCal);*/

        // If 'displayOptions' is zero, the chosen options are not valid
        return new Pair<>(displayOptions != 0 ? Boolean.TRUE : Boolean.FALSE, options);
    }

    // Show date, time & recurrence options that have been selected
    private void updateInfoView() {
        if (mSelectedDate != null) {
            if (mSelectedDate.getType() == SelectedDate.Type.SINGLE) {
//                llDateRangeHolder.setVisibility(View.GONE);
                llDateHolder.setVisibility(View.VISIBLE);

                tvYear.setText(applyBoldStyle("YEAR: ")
                        .append(String.valueOf(mSelectedDate.getStartDate().get(Calendar.YEAR))));
                tvMonth.setText(applyBoldStyle("MONTH: ")
                        .append(String.valueOf(mSelectedDate.getStartDate().get(Calendar.MONTH))));
                tvDay.setText(applyBoldStyle("DAY: ")
                        .append(String.valueOf(mSelectedDate.getStartDate().get(Calendar.DAY_OF_MONTH))));
            } else if (mSelectedDate.getType() == SelectedDate.Type.RANGE) {
                llDateHolder.setVisibility(View.GONE);
//                llDateRangeHolder.setVisibility(View.VISIBLE);

                tvStartDate.setText(applyBoldStyle("START: ")
                        .append(DateFormat.getDateInstance().format(mSelectedDate.getStartDate().getTime())));
                tvEndDate.setText(applyBoldStyle("END: ")
                        .append(DateFormat.getDateInstance().format(mSelectedDate.getEndDate().getTime())));
            }
        }

        tvHour.setText(applyBoldStyle("HOUR: ").append(String.valueOf(mHour)));
        tvMinute.setText(applyBoldStyle("MINUTE: ").append(String.valueOf(mMinute)));

        tvRecurrenceOption.setText(applyBoldStyle("RECURRENCE OPTION: ")
                .append(mRecurrenceOption));
        tvRecurrenceRule.setText(applyBoldStyle("RECURRENCE RULE: ").append(
                mRecurrenceRule));

        rlDateTimeRecurrenceInfo.setVisibility(View.VISIBLE);
    }

    // Applies a StyleSpan to the supplied text
    private SpannableStringBuilder applyBoldStyle(String text) {
        SpannableStringBuilder ss = new SpannableStringBuilder(text);
        ss.setSpan(new StyleSpan(Typeface.BOLD), 0, text.length(),
                Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
        return ss;
    }








}
